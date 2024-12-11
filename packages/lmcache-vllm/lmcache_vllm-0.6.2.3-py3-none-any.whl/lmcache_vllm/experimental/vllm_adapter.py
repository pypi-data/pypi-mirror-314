from typing import TYPE_CHECKING, List, Optional, Tuple
from types import SimpleNamespace
from enum import Enum
import os
import torch
import dataclasses
from copy import deepcopy
from torch.nn.utils.rnn import pad_sequence
from dataclasses import dataclass
from torch import nn
import torch.distributed as dist
from vllm.attention.backends.utils import compute_slot_mapping

if TYPE_CHECKING:
    from vllm.worker.model_runner import ModelInputForGPUWithSamplingMetadata

from vllm import _custom_ops as ops
from vllm.sequence import SequenceGroupMetadata
from vllm.config import ModelConfig, ParallelConfig, CacheConfig
from vllm.utils import get_kv_cache_torch_dtype

from lmcache.logging import init_logger
from lmcache.experimental.cache_engine import LMCacheEngine, LMCacheEngineBuilder
from lmcache.experimental.gpu_connector import GPUConnectorInterface
from lmcache.experimental.memory_management import MemoryObj, MemoryFormat
from lmcache.config import LMCacheEngineConfig, LMCacheEngineMetadata
from lmcache.utils import _lmcache_nvtx_annotate
from lmcache_vllm.lmcache_utils import ENGINE_NAME
from lmcache_vllm.vllm_adapter import lmcache_get_config


logger = init_logger(__name__)

@dataclass
class VLLMGPUConnectorMetadata:
    kv_caches: List[torch.Tensor]
    start_layer: int
    end_layer: int

    # How many tokens hits the vLLM's prefix cache
    # Say there are N tokens in total and prefix_offset = M,
    # Then the length of the slot_mapping is N - M
    prefix_offset: int

    # The slot mapping for the "non-hit" sequence
    slot_mapping: torch.Tensor

    # for reshape_and_cache function call
    kv_cache_dtype: torch.dtype
    k_scale: float
    v_scale: float

class VLLMGPUConnector(GPUConnectorInterface):
    def __init__(self):
        pass

    def from_gpu(self, memory_obj: MemoryObj, start: int, end: int, **kwargs):
        """Expect a kwarg 'metadata' which is the VLLMGPUConnectorMetadata.
        Copy the KV caches to the memory obj with a KV_BLOB format

        :raises ValueError: If 'metadata' is not provided in kwargs
        :raises AssertionError: If the memory object does not have a tensor.
        """
        assert memory_obj.tensor is not None
        
        if 'metadata' not in kwargs:
            raise ValueError("metadata is not provided in kwargs")

        metadata: VLLMGPUConnectorMetadata = kwargs['metadata']

def init_lmcache_engine(
        model_config: ModelConfig,
        parallel_config: ParallelConfig,
        cache_config: CacheConfig,
    ) -> Optional[LMCacheEngine]:
    """Initialize the LMCache engine by the given model config and parallel 
    config. This function will check the environment variable 
    `LMCACHE_CONFIG_FILE` to load the configuration file. If that environment
    variable is not set, this function will return None.

    :param model_config: The model configuration in vLLM.
    :type model_config: ModelConfig
    :param parallel_config: The parallel configuration in vLLM.
    :type parallel_config: ParallelConfig
    :param cache_config: The KV cache configuration in vLLM.
    :type cache_config: CacheConfig

    :return: The initialized LMCache engine or None (if the environment variable
        `LMCACHE_CONFIG_FILE` is not set).
    :rtype: Optional[LMCacheEngine]
    """
    if LMCacheEngineBuilder.get(ENGINE_NAME) is not None:
        return 

    config = lmcache_get_config()
    
    kv_dtype = get_kv_cache_torch_dtype(cache_config.cache_dtype, model_config.dtype)

    # construct kv shape (for mem pool)
    num_layer = model_config.get_num_layers(parallel_config)
    chunk_size = config.chunk_size
    num_kv_head = model_config.get_num_kv_heads(parallel_config)
    head_size = model_config.get_head_size()
    kv_shape = (num_layer, 2, chunk_size, num_kv_head, head_size)
    
    # Change current device.
    torch.cuda.device(parallel_config.rank)
    metadata = LMCacheEngineMetadata(
            model_config.model,
            parallel_config.world_size,
            parallel_config.rank,
            "vllm",
            kv_dtype,
            kv_shape)
    
    connector = VLLMGPUConnector()
    engine = LMCacheEngineBuilder.get_or_create(
            ENGINE_NAME,
            config,
            metadata,
            connector)

    return engine

@_lmcache_nvtx_annotate
def lmcache_retrieve_kv(
    model_executable,
    model_name: str,
    model_input: "ModelInputForGPUWithSamplingMetadata",
    kv_caches: List[torch.Tensor],
    retrieve_status: RetrieveStatus,
) -> Tuple["ModelInputForGPUWithSamplingMetadata", bool]:
    """Retrieve the KV caches from LMCache for the current model_input. And 
    rebuild the model_input to reflect the changes in KV if necessary.

    :param model_executable: The model executable for the current request.
    :type model_executable: torch.nn.Module

    :param model_input: The model input for the current request.
    :type model_input: ModelInputForGPUWithSamplingMetadata

    :param kv_caches: The paged memory to put KV to
    :type kv_caches: List[torch.Tensor]

    :param retrieve_status: Indicate whether and how KV cache of each req is retrieved
    :type retrieve_status: List[RetrieveStatus]
    
    :return: The rebuilt model_input to reflect the changes in KV.
    :return: The boolean value to indicate whether the entire execute_model should be skipped
    """
    engine = LMCacheEngineBuilder.get(ENGINE_NAME)
    assert engine is not None, "LMCache engine is not initialized."

    query_start_loc = model_input.attn_metadata.query_start_loc
    slot_mapping = model_input.attn_metadata.slot_mapping.flatten()
    seq_lens = model_input.attn_metadata.seq_lens


    model_input_subset = create_model_input_subset(
        model_name, model_executable)
    attn_layers = model_input_subset.attn_layers
    start_layer = model_input_subset.start_layer
    end_layer = model_input_subset.end_layer
    
    # The following metadata are needed to rebuilt the model input
    full_tokens_list = []
    num_computed_tokens_list = []
    lmc_num_computed_tokens_list= []
    
    start_pos_list = []
    is_prefill_list = []
     
    next_start_pos = 0
    num_request_not_found = 0
    temp_block_table_list = []
    
    # idx is on a sequence, not a sequence group.
    idx = 0

    seq_group_metadata_list = model_input.seq_group_metadata_list

    for seq_group_metadata in seq_group_metadata_list:
        request_id = seq_group_metadata.request_id
        seq_ids = model_input.request_ids_to_seq_ids[request_id]
        for seq_id in seq_ids:
            seq_data = seq_group_metadata.seq_data[seq_id]
            is_prefill_list.append(seq_group_metadata.is_prompt)
            if retrieve_status == RetrieveStatus.CHUNK_PREFILL:
                total_seq_len = seq_lens[idx]
            else:
                total_seq_len = seq_data.get_len()
            
            full_token_tensor = torch.tensor(seq_data.get_token_ids()[:total_seq_len], device="cpu")
            full_tokens_list.append(full_token_tensor)
            
            vllm_num_required_tokens = (query_start_loc[idx + 1] - query_start_loc[idx]).item()
            
            start_pos = next_start_pos
            end_pos = start_pos + vllm_num_required_tokens
            next_start_pos = end_pos
            start_pos_list.append(start_pos)
            
            # TODO(Jiayi): is deepcopy avoidable here?
            temp_block_table = deepcopy(seq_group_metadata.block_tables[seq_id])
            temp_block_table_list.append(temp_block_table)

            # number of tokens computed by vllm (e.g., chunk prefill, prefix caching)
            vllm_num_computed_tokens = total_seq_len - vllm_num_required_tokens
            
            # construct token mesk to indicate what tokens should be retrieved
            # from lmc. Tokens computed in vllm already shoudl be skipped
            token_mask = torch.ones_like(full_token_tensor, dtype=torch.bool)
            token_mask[:vllm_num_computed_tokens] = False
            
            # call lmcache retrieve
            kv_tuple, ret_token_mask = engine.retrieve(full_token_tensor, token_mask)
            #ret_token_mask = engine.retrieve(
            #        full_token_tensor, 
            #        token_mask,
            #        kvcaches = kvcaches)
            lmc_num_computed_tokens = torch.sum(ret_token_mask).item()
            
            # total number of computed tokens (vllm + lmc)
            num_computed_tokens = vllm_num_computed_tokens + lmc_num_computed_tokens
            
            # TODO(Jiayi): currently we do not skip anything if chunked prefill
            # is batched with any decode or other chunked prefills.
            # This is not done as I assume the performance benefit is marginal.
            if retrieve_status == RetrieveStatus.CHUNK_PREFILL:
                if num_computed_tokens != total_seq_len:
                    return model_input, False
            else:
                # Avoid the error when prefix is exactly the same as the retrieved
                # However, in chunk prefill, the entire prefill should be skipped
                if num_computed_tokens == total_seq_len:
                    lmc_num_computed_tokens -= 1
                    num_computed_tokens -= 1
            
            num_computed_tokens_list.append(num_computed_tokens)
            lmc_num_computed_tokens_list.append(lmc_num_computed_tokens)
            
            
            # No cache found, move on
            if lmc_num_computed_tokens == 0:
                num_request_not_found += 1
                idx += 1
                continue
            
            
            # Inject the lmc retrieved kv cache
            logger.debug(f"Injected token number: {lmc_num_computed_tokens}")
            for i in range(start_layer, end_layer):
                layer_idx = i - start_layer
                kv_cache = kv_caches[layer_idx]
                attn_layer = attn_layers[i]
                key_cache, value_cache = kv_cache[0], kv_cache[1]
                ops.reshape_and_cache_flash(
                    kv_tuple[layer_idx][0].to(key_cache.device),
                    kv_tuple[layer_idx][1].to(value_cache.device),
                    key_cache,
                    value_cache,
                    slot_mapping[start_pos:start_pos + lmc_num_computed_tokens],
                    attn_layer.attn.kv_cache_dtype,
                    attn_layer.attn._k_scale,
                    attn_layer.attn._v_scale,
                )
            
            idx += 1
            
    
    seq_cnt = len(query_start_loc) - 1
    assert idx == seq_cnt
    assert len(lmc_num_computed_tokens_list) == seq_cnt
    assert len(num_computed_tokens_list) == seq_cnt
    
    if retrieve_status == RetrieveStatus.CHUNK_PREFILL and \
        num_request_not_found == 0:
        return model_input, True
            
    # Some of the request can be skipped for a bit
    # TODO(Jiayi): need e2e test full prefill and partial prefill
    # in a single batch
    if num_request_not_found < seq_cnt:
        rebuilt_model_input = build_partial_prefill_input(
            model_input,
            full_tokens_list,
            num_computed_tokens_list,
            start_pos_list,
            slot_mapping,
            lmc_num_computed_tokens_list,
            is_prefill_list,
            seq_group_metadata_list,
            temp_block_table_list,
            device=kv_cache[0].device,
        )
        logger.debug("Rebuilt the input!")
        return rebuilt_model_input, False
    
    logger.debug("Returning the original input!")
    return model_input, False

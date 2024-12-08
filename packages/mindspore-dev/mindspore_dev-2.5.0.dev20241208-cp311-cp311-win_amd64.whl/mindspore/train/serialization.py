# Copyright 2020-2024 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Model and parameters serialization."""
from __future__ import absolute_import
from __future__ import division

import binascii
import copy
import json
import os
import re
import shutil
import stat
import threading
from threading import Thread, RLock
from multiprocessing import Pool
import multiprocessing as mp
from collections import defaultdict, OrderedDict
from io import BytesIO

import math
import sys
import time
import google
import numpy as np

from safetensors.numpy import save_file, load_file
from safetensors import safe_open

from mindspore.train.checkpoint_pb2 import Checkpoint
from mindspore.train.mind_ir_pb2 import ModelProto as mindir_model
from mindspore.train.print_pb2 import Print

import mindspore
import mindspore.nn as nn
from mindspore import context
from mindspore import log as logger
from mindspore.log import vlog_print
from mindspore._checkparam import check_input_data, check_input_dataset
from mindspore import _checkparam as Validator
from mindspore.common import dtype as mstype
from mindspore.common.api import _cell_graph_executor as _executor
from mindspore.common.api import _MindsporeFunctionExecutor
from mindspore.common.api import _get_parameter_layout
from mindspore.common.api import _generate_branch_control_input
from mindspore.common.initializer import initializer, One
from mindspore.common.parameter import Parameter, _offload_if_config
from mindspore.common.tensor import Tensor
from mindspore._c_expression import Tensor as Tensor_
from mindspore.common._utils import is_shape_unknown
from mindspore.common.file_system import FileSystem, _register_basic_file_system, _register_mindio_file_system
from mindspore.communication.management import get_rank, get_group_size
from mindspore.experimental import MapParameter
from mindspore.ops import Cast
from mindspore.parallel._cell_wrapper import get_allgather_cell, _single_parameter_broadcast
from mindspore.parallel._tensor import _load_tensor, _get_tensor_strategy, _get_tensor_slice_index
from mindspore.parallel._tensor import _reshape_param_data, _reshape_param_data_with_weight
from mindspore.parallel._utils import _infer_rank_list, _remove_repeated_slices, _is_in_auto_parallel_mode, \
    _get_device_num
from mindspore.parallel._auto_parallel_context import _get_auto_parallel_context
from mindspore.parallel._parallel_serialization import _convert_to_list, _convert_to_layout, _build_searched_strategy, \
    _restore_group_info_list, _get_param_list_when_first_dim_sharded
from mindspore.parallel._ps_context import _set_checkpoint_load_status, _store_warm_up_ptr_by_tensor, \
    _store_warm_up_ptr_by_tensor_list, _cache_enable
from mindspore.parallel.checkpoint_transform import sync_pipeline_shared_parameters
from mindspore.parallel.transform_safetensors import _load_parallel_checkpoint, _get_device_num_from_strategy, \
    _extract_pipeline_stage_num
from mindspore.train._utils import read_proto, get_parameter_redundancy, _progress_bar, _load_and_transform
from mindspore._c_expression import load_mindir, _encrypt, _decrypt, _is_cipher_file, dynamic_obfuscate_mindir, \
    split_mindir, split_dynamic_mindir
from mindspore.common.generator import Generator
from ..ops.operations._opaque_predicate_registry import add_opaque_predicate, clean_funcs


tensor_to_ms_type = {"Int8": mstype.int8, "UInt8": mstype.uint8, "Int16": mstype.int16, "UInt16": mstype.uint16,
                     "Int32": mstype.int32, "UInt32": mstype.uint32, "Int64": mstype.int64, "UInt64": mstype.uint64,
                     "Float16": mstype.float16, "Float32": mstype.float32, "Float64": mstype.float64,
                     "Bool": mstype.bool_, "str": mstype.string, "BFloat16": mstype.bfloat16, "Int4": mstype.qint4x2}

tensor_to_np_type = {"Int8": np.int8, "UInt8": np.uint8, "Int16": np.int16, "UInt16": np.uint16,
                     "Int32": np.int32, "UInt32": np.uint32, "Int64": np.int64, "UInt64": np.uint64,
                     "Float16": np.float16, "Float32": np.float32, "Float64": np.float64, "Bool": np.bool_, "str": "U"}

np_type_convert = {"int32": np.int32, "float32": np.float32, "float16": np.float16, "float64": np.float64}

mindir_to_tensor_type = {1: mstype.float32, 2: mstype.uint8, 3: mstype.int8, 4: mstype.uint16,
                         5: mstype.int16, 6: mstype.int32, 7: mstype.int64, 10: mstype.float16,
                         11: mstype.float64, 12: mstype.uint32, 13: mstype.uint64}

_ckpt_mutex = RLock()

# unit is KB
SLICE_SIZE = 512 * 1024
PROTO_LIMIT_SIZE = 1024 * 1024 * 2
TOTAL_SAVE = 1024 * 1024
PARAMETER_SPLIT_SIZE = 1024 * 1024 * 1024
ENCRYPT_BLOCK_SIZE = 64 * 1024
INT_64_MAX = 9223372036854775807

cpu_cast = Cast().set_device("CPU")

_ckpt_fs = FileSystem()


def init_ckpt_file_system(fs: FileSystem):
    """Initialize checkpoint file system"""
    if _register_mindio_file_system(fs):
        return
    _register_basic_file_system(fs)


# Initialize checkpoint file system
init_ckpt_file_system(_ckpt_fs)


def _get_cur_rank_dp(parameter_layout_dict):
    """ Get dp and tp from layout dict. """
    pp_num = _get_auto_parallel_context("pipeline_stages")
    dev_num = _get_device_num()
    global_rank = get_rank()
    pipe_size = dev_num // pp_num
    initial_rank = (global_rank // pipe_size) * pipe_size
    parameter_redundancy_dict = get_parameter_redundancy(
        parameter_layout_dict, initial_rank)
    value_len = sys.maxsize
    min_value = ()
    for key, value in parameter_redundancy_dict.items():
        if "accu_grads" in key or "inputs" in key:
            continue
        for item in value:
            if len(item) < value_len and global_rank in item:
                value_len = len(item)
                min_value = item
    return min_value


def get_ckpt_path_with_strategy(cur_ckpt_path, cur_strategy_path):
    """
    Find available checkpoint file path from all backup checkpoint files of current rank.
    It suppose that checkpoint path contains substring 'rank_{rank_id}' which is used to
    distinguish between different path.If cur_ckpt_path doesn't have 'rank_{rank_id}' substring, will return
    cur_ckpt_path itself when cur_ckpt_path is exist, otherwise return None.

    Note:
       This API must be called after the communication is initialized because the cluster information
       needs to be obtained internally.

    Args:
        cur_ckpt_path (str): the checkpoint file path which cur rank needs.
        cur_strategy_path (str): strategy file path for current rank.

    Returns:
        - new_ckpt_file (String), if found available checkpoint file , return it.
        - None, if not found available checkpoint, return None.

    Examples:
        >>> import mindspore as ms
        >>> from mindspore.communication import init
        >>> from mindspore import get_ckpt_path_with_strategy
        >>> ms.set_context(mode=ms.GRAPH_MODE)
        >>> ms.set_auto_parallel_context(parallel_mode=ms.ParallelMode.DATA_PARALLEL, gradients_mean=True)
        >>> init()
        >>> ckpt_file= "./rank_5/iteration-1_40.ckpt"
        >>> strategy_file = "./src_pipeline_strategys/src_strategy_5.ckpt"
        >>> ckpt_file_new = get_ckpt_path_with_strategy(ckpt_file, strategy_file)
        >>> print(ckpt_file_new)
    """
    dp = _get_cur_rank_dp(cur_strategy_path)
    pattern = r'rank_\d+'
    for i in dp:
        new_ckpt_path = re.sub(pattern, f"rank_{str(i)}", cur_ckpt_path)
        if not os.path.isfile(new_ckpt_path):
            continue
        return new_ckpt_path
    return None


class ParamDictFuture:
    def __init__(self, executor, param_dict_future):
        self.executor = executor
        self.param_dict_future = param_dict_future

    def result(self):
        param_dict = self.param_dict_future.result()
        self.executor.shutdown()
        return param_dict


def _special_process_par(par, new_par):
    """
    Processes the special condition.

    Like (12,2048,1,1)->(12,2048), this case is caused by GE 4 dimensions tensor.
    """
    par_shape_len = len(par.data.shape)
    new_par_shape_len = len(new_par.data.shape)
    if new_par_shape_len <= par_shape_len:
        return False

    for i in range(new_par_shape_len - par_shape_len):
        if new_par.data.shape[par_shape_len + i] != 1:
            return False

    if new_par.data.dtype == mstype.bfloat16:
        new_val = cpu_cast(new_par.data, mstype.float32).asnumpy()
    else:
        new_val = new_par.data.asnumpy()

    new_val = new_val.reshape(par.data.shape)
    par.set_data(Tensor(new_val, par.data.dtype))
    return True


def _update_param(param, new_param, strict_load):
    """Updates param's data from new_param's data."""
    if isinstance(param.data, Tensor) and isinstance(new_param.data, Tensor):
        if param.data.shape != new_param.data.shape:
            if not _special_process_par(param, new_param):
                logger.critical("Failed to combine the net and the parameters for param %s.", param.name)
                msg = (f"For 'load_param_into_net', {param.name} in the argument 'net' should have the same shape "
                       f"as {param.name} in the argument 'parameter_dict'. But got its shape {param.data.shape} in"
                       f" the argument 'net' and shape {new_param.data.shape} in the argument 'parameter_dict'."
                       f"May you need to check whether the checkpoint you loaded is correct or the batch size and "
                       f"so on in the 'net' and 'parameter_dict' are same.")
                raise RuntimeError(msg)

        if param.data.dtype != new_param.data.dtype:
            if _type_convert(param, new_param, strict_load):
                if new_param.data.dtype == mstype.bfloat16:
                    new_tensor = cpu_cast(new_param.data, param.data.dtype)
                else:
                    new_tensor = Tensor(new_param.data.asnumpy(), param.data.dtype)
                param.set_data(new_tensor, param.sliced)
                return

            logger.critical("Failed to combine the net and the parameters for param %s.", param.name)
            msg = (f"For 'load_param_into_net', {param.name} in the argument 'net' should have the same type as "
                   f"{param.name} in the argument 'parameter_dict'. but got its type {param.data.dtype} in the "
                   f"argument 'net' and type {new_param.data.dtype} in the argument 'parameter_dict'."
                   f"May you need to check whether the checkpoint you loaded is correct.")
            raise RuntimeError(msg)

        param.set_data(new_param.data, param.sliced)
        return

    if isinstance(param.data, Tensor) and not isinstance(new_param.data, Tensor):
        if param.data.shape != (1,) and param.data.shape != ():
            logger.critical("Failed to combine the net and the parameters for param %s.", param.name)
            msg = (f"For 'load_param_into_net', {param.name} in the argument 'parameter_dict' is "
                   f"scalar, then the shape of {param.name} in the argument 'net' should be "
                   f"(1,) or (), but got shape {param.data.shape}."
                   f"May you need to check whether the checkpoint you loaded is correct.")
            raise RuntimeError(msg)
        param.set_data(initializer(new_param.data, param.data.shape, param.data.dtype))

    elif isinstance(new_param.data, Tensor) and not isinstance(param.data, Tensor):
        logger.critical("Failed to combine the net and the parameters for param %s.", param.name)
        msg = (f"For 'load_param_into_net', {param.name} in the argument 'parameter_dict' is Tensor, "
               f"then {param.name} in the argument 'net' also should be Tensor, but got {type(param.data)}."
               f"May you need to check whether the checkpoint you loaded is correct.")
        raise RuntimeError(msg)

    else:
        param.set_data(type(param.data)(new_param.data))


def _type_convert(param, new_param, strict_load):
    """Whether to convert parameter's type during load checkpoint into network."""
    float_type = (mstype.float16, mstype.float32, mstype.float64, mstype.bfloat16)
    int_type = (mstype.int8, mstype.int16, mstype.int32, mstype.int64)
    if not strict_load and ({param.data.dtype, new_param.data.dtype}.issubset(float_type) or
                            {param.data.dtype, new_param.data.dtype}.issubset(int_type)):
        logger.warning(f"The type of {new_param.name}:{new_param.data.dtype} in 'parameter_dict' is different from "
                       f"the type of it in 'net':{param.data.dtype}, then the type convert from "
                       f"{new_param.data.dtype} to {param.data.dtype} in the network. May consume additional memory "
                       f"and time")
        return True
    return False


def _save_weight(checkpoint_dir, model_name, iteration, params):
    """Save model weight into checkpoint."""
    logger.debug(f"Checkpoint dir is: '{checkpoint_dir}'")
    exist_ckpt_file_list = []
    if os.path.exists(checkpoint_dir):
        for exist_ckpt_name in os.listdir(checkpoint_dir):
            file_prefix = os.path.join(model_name, "_iteration_")
            if exist_ckpt_name.startswith(file_prefix):
                exist_ckpt_file_list.append(exist_ckpt_name)

        param_dict = OrderedDict()
        for key in params.keys():
            value = params[key]
            weight_type = value[0]
            weight_shape = value[1]
            weight_data = value[2]
            weight_size = value[3]
            weight_np = np.array(weight_data, dtype=weight_type.lower())
            logger.debug(f"weight_type: '{weight_type}', weight_shape: '{weight_shape}', weight_size: "
                         f"'{weight_size}', weight_np.nbytes: '{weight_np.nbytes}'")

            param_dict[key] = [weight_shape, weight_type, weight_np]
        ckpt_file_save_name = model_name + "_iteration_" + iteration + ".ckpt"
        ckpt_file_save_path = os.path.join(checkpoint_dir, ckpt_file_save_name)

        _exec_save(ckpt_file_save_path, param_dict)

        for exist_ckpt_name in exist_ckpt_file_list:
            os.remove(os.path.join(checkpoint_dir, exist_ckpt_name))
        logger.info(f"Save weight to checkpoint file path '{ckpt_file_save_path}' success.")
    else:
        logger.warning(f"Checkpoint dir: '{checkpoint_dir}' is not existed.")


def _exec_save(ckpt_file_name, data_list, enc_key=None, enc_mode="AES-GCM", map_param_inc=False, crc_check=False,
               format="ckpt"):
    """Execute the process of saving checkpoint into file."""
    try:
        with _ckpt_mutex:
            file_name_list = list(os.path.splitext(ckpt_file_name))
            file_name_list[1] = file_name_list[1].replace(f".{format}", ".tmp")
            tmp_name = ''.join(file_name_list)
            if os.path.exists(ckpt_file_name):
                os.chmod(ckpt_file_name, stat.S_IWUSR)
                os.remove(ckpt_file_name)
            if os.path.exists(tmp_name):
                os.chmod(tmp_name, stat.S_IWUSR)
                os.remove(tmp_name)
            if format == "ckpt":
                ckpt_save_time_start = time.time()
                with _ckpt_fs.create(tmp_name, *_ckpt_fs.create_args) as f:
                    plain_data = None
                    if enc_key is not None:
                        plain_data = BytesIO()

                    crc_num = 0
                    for name, value in data_list.items():
                        if name == "random_op":
                            _write_random_seed(name, value, f)
                            continue
                        if value[0] == "mapparameter":
                            _write_mapparameter(name, value, f, map_param_inc)
                            continue
                        if value[0] == "offload_parameter":
                            new_value = value[1:]
                            new_value[2] = value[3]
                            _write_parameter_bytes_data(name, new_value, f, enc_key, plain_data)
                            _offload_if_config(value[3])
                            continue
                        if value[1] == "str":
                            crc_num = _write_parameter_data(name, value, f, enc_key, plain_data, crc_num, crc_check)
                            continue
                        if isinstance(value[2], np.ndarray):
                            crc_num = _write_parameter_data(name, value, f, enc_key, plain_data, crc_num, crc_check)
                            continue
                        if isinstance(value[2], Tensor) and hasattr(value[2], "slice_num") and value[2].slice_num > 1:
                            _write_hugeparameter(name, value, f)
                            continue

                        crc_num = _write_parameter_bytes_data(name, value, f, enc_key, plain_data, crc_num, crc_check)

                    if enc_key is not None:
                        plain_data.seek(0)
                        max_block_size = ENCRYPT_BLOCK_SIZE * 1024
                        block_data = plain_data.read(max_block_size)
                        while block_data:
                            f.write(_encrypt(block_data, len(block_data), enc_key, len(enc_key), enc_mode))
                            block_data = plain_data.read(max_block_size)
                    if crc_check:
                        f.write('crc_num'.encode() + crc_num.to_bytes(10, byteorder='big'))
                ckpt_save_time_end = time.time()
                cost_time = ckpt_save_time_end - ckpt_save_time_start
                vlog_print("1", "ME", __file__, sys._getframe().f_lineno, f"Save ckpt cost time:{cost_time}.")
            elif format == "safetensors":
                save_dict = {}
                for name, value in data_list.items():
                    save_dict[name] = value[2].asnumpy()
                safetensors_save_time_start = time.time()
                save_file(save_dict, tmp_name)
                safetensors_save_time_end = time.time()
                cost_time = safetensors_save_time_end - safetensors_save_time_start
                vlog_print("1", "ME", __file__, sys._getframe().f_lineno, f"Save safetensors cost time:{cost_time}.")
            if not os.path.exists(tmp_name):
                logger.warning(f"Rename failed, can't find {tmp_name}, it is possible that multiple processes have "
                               f"simultaneously modified a file.")
            else:
                os.rename(tmp_name, ckpt_file_name)
            os.chmod(ckpt_file_name, stat.S_IRUSR)
    except BaseException as e:
        logger.critical("Failed to save the checkpoint file %s. Maybe don't have the permission to write files, "
                        "or the disk space is insufficient and so on.", ckpt_file_name)
        raise e


def _write_random_seed(name, value, f):
    """Write random op into protobuf file."""
    checkpoint_list = Checkpoint()
    param_value = checkpoint_list.value.add()
    param_value.tag = name
    param_tensor = param_value.tensor
    param_tensor.dims.extend(0)
    param_tensor.tensor_type = "random_op"
    param_tensor.tensor_content = value
    f.write(checkpoint_list.SerializeToString())


def _write_parameter_data(name, value, f, enc_key, plain_data, crc_num=0, crc_check=False):
    """Write parameter data into protobuf file."""
    data_size = value[2].nbytes / 1024
    if data_size > SLICE_SIZE:
        slice_count = math.ceil(data_size / SLICE_SIZE)
        param_slice_list = np.array_split(value[2], slice_count)
    else:
        param_slice_list = [value[2]]

    for param_slice in param_slice_list:
        checkpoint_list = Checkpoint()
        param_value = checkpoint_list.value.add()
        param_value.tag = name
        param_tensor = param_value.tensor
        param_tensor.dims.extend(value[0])
        param_tensor.tensor_type = value[1]
        param_tensor.tensor_content = param_slice.tobytes()

        if enc_key is None:
            output_data = checkpoint_list.SerializeToString()
            if crc_check:
                crc_num = binascii.crc32(output_data, crc_num)
            f.write(output_data)
        else:
            plain_data.write(checkpoint_list.SerializeToString())

    return crc_num


def _write_parameter_bytes_data(name, value, f, enc_key, plain_data, crc_num=0, crc_check=False):
    """Write parameter bytes data into protobuf file."""
    bytes_value = value[2].get_bytes()
    chunk_size = 1024 * SLICE_SIZE

    for i in range(0, len(bytes_value), chunk_size):
        checkpoint_list = Checkpoint()
        param_value = checkpoint_list.value.add()
        param_value.tag = name
        param_tensor = param_value.tensor
        param_tensor.dims.extend(value[0])
        param_tensor.tensor_type = value[1]
        param_tensor.tensor_content = bytes_value[i:i + chunk_size]

        if enc_key is None:
            output_data = checkpoint_list.SerializeToString()
            if crc_check:
                crc_num = binascii.crc32(output_data, crc_num)
            f.write(output_data)
        else:
            plain_data.write(checkpoint_list.SerializeToString())

    return crc_num


def _write_mapparameter(name, value, f, map_param_inc=False):
    """Write map parameter into protobuf file."""
    while True:
        logger.info("Checkpoint save map_parameter.")
        data_map_slice = value[1].export_slice_data(map_param_inc)
        checkpoint_list = Checkpoint()
        param_value = checkpoint_list.value.add()
        param_value.tag = name
        map_tensor = param_value.maptensor
        for numpy_data in data_map_slice[:3]:
            tensor_pro = map_tensor.tensor.add()
            tensor_pro.dims.extend(numpy_data.shape)
            tensor_pro.tensor_type = str(numpy_data.dtype)
            tensor_pro.tensor_content = numpy_data.reshape(-1).tobytes()
        f.write(checkpoint_list.SerializeToString())
        if data_map_slice[3]:
            break


def _write_hugeparameter(name, value, f):
    """Write huge parameter into protobuf file."""
    slice_num = value[2].slice_num
    offset = 0
    max_size = value[0][0]
    for param_slice in range(slice_num):
        checkpoint_list = Checkpoint()
        param_value = checkpoint_list.value.add()
        param_value.tag = name
        param_tensor = param_value.tensor
        param_tensor.dims.extend(value[0])
        param_tensor.tensor_type = value[1]
        param_key = value[3]
        numpy_data = value[2].asnumpy_of_slice_persistent_data(param_key, param_slice)
        if offset + numpy_data.shape[0] > max_size:
            numpy_data = numpy_data[:max_size - offset]
        param_tensor.tensor_content = numpy_data.tobytes()
        f.write(checkpoint_list.SerializeToString())
        offset += numpy_data.shape[0]


def _check_save_obj_and_ckpt_file_name(save_obj, ckpt_file_name, format):
    """Check save_obj and ckpt_file_name for save_checkpoint."""
    if format not in ["safetensors", "ckpt"]:
        raise ValueError(f"For 'save_checkpoint', the format must be "
                         f"'safetensors' or 'ckpt', but got {format}.")
    if not isinstance(save_obj, (nn.Cell, list, dict)):
        raise TypeError("For 'save_checkpoint', the parameter 'save_obj' must be nn.Cell, list or dict, "
                        "but got {}.".format(type(save_obj)))
    if not isinstance(ckpt_file_name, str):
        raise TypeError("For 'save_checkpoint', the parameter {} for checkpoint file name is invalid,"
                        "'ckpt_file_name' must be "
                        "string, but got {}.".format(ckpt_file_name, type(ckpt_file_name)))
    ckpt_file_name = os.path.realpath(ckpt_file_name)
    if os.path.isdir(ckpt_file_name):
        raise IsADirectoryError("For 'save_checkpoint', the parameter `ckpt_file_name`: {} is a directory, "
                                "it must be a file name.".format(ckpt_file_name))
    if not ckpt_file_name.endswith(format):
        ckpt_file_name += f".{format}"
    return ckpt_file_name


def _check_format_and_other_params(format, enc_key, enc_mode, crc_check=False, async_save=False, map_param_inc=False,
                                   global_step_num=None):
    param_not_default = (enc_key is not None or enc_mode != "AES-GCM" or crc_check or async_save
                         or map_param_inc or global_step_num is not None)
    if format == "safetensors" and param_not_default:
        raise ValueError("For 'save_checkpoint', when format is 'safetensors', other param must be default.")


def save_checkpoint(save_obj, ckpt_file_name, integrated_save=True,
                    async_save=False, append_dict=None, enc_key=None, enc_mode="AES-GCM", choice_func=None,
                    crc_check=False, format="ckpt", **kwargs):
    r"""
    Save checkpoint to a specified file.

    Note:
        The `enc_mode` and `crc_check` parameters are mutually exclusive and cannot be configured simultaneously.

    Args:
        save_obj (Union[Cell, list, dict]): The object to be saved. The data type can be :class:`mindspore.nn.Cell`,
            list, or dict. If a list, it can be the returned value of `Cell.trainable_params()`, or a list of dict
            elements(each element is a dictionary, like [{"name": param_name, "data": param_data},...], the type of
            `param_name` must be string, and the type of `param_data` must be parameter or Tensor); If dict,
            it can be the returned value of `mindspore.load_checkpoint()`.
        ckpt_file_name (str): Checkpoint file name. If the file name already exists, it will be overwritten.
        integrated_save (bool): Whether to integrated save in automatic model parallel scene. Default: ``True`` .
        async_save (bool): Whether to open an independent thread to save the checkpoint file. Default: ``False`` .
        append_dict (dict): Additional information that needs to be saved. The key of dict must be str, the value
                            of dict must be one of int, float, bool, string, Parameter or Tensor. Default: ``None`` .
        enc_key (Union[None, bytes]): Byte type key used for encryption. If the value is ``None`` , the encryption
                                      is not required. Default: ``None`` .
        enc_mode (str): This parameter is valid only when enc_key is not set to ``None`` . Specifies the encryption
                        mode, currently supports ``"AES-GCM"`` and ``"AES-CBC"`` and ``"SM4-CBC"`` .
                        Default: ``"AES-GCM"`` .
        choice_func (function) : A function for saving custom selected parameters. The input value of `choice_func` is
                                 a parameter name in string type, and the returned value is a bool.
                                 If returns ``True`` , the Parameter that matching the custom condition will be saved.
                                 If returns ``False`` , the Parameter that not matching the custom condition will not
                                 be saved. Default: ``None`` .
        crc_check (bool) : Whether to perform crc32 calculation when saving checkpoint and save the calculation
            result to the file. Default: ``False`` .
        format (str): Format of the output file, can be "ckpt" or "safetensors". Default: "ckpt".
        kwargs (dict): Configuration options dictionary.

    Raises:
        TypeError: If the parameter `save_obj` is not :class:`mindspore.nn.Cell` , list or dict type.
        TypeError: If the parameter `integrated_save` or `async_save` is not bool type.
        TypeError: If the parameter `ckpt_file_name` is not string type.

    Examples:
        >>> import mindspore as ms
        >>>
        >>> # Define the network structure of LeNet5. Refer to
        >>> # https://gitee.com/mindspore/docs/blob/master/docs/mindspore/code/lenet.py
        >>> net = LeNet5()
        >>> ms.save_checkpoint(net, "./lenet.ckpt",
        ...                    choice_func=lambda x: x.startswith("conv") and not x.startswith("conv1"))
        >>> param_dict1 = ms.load_checkpoint("./lenet.ckpt")
        >>> print(param_dict1)
        {'conv2.weight': Parameter (name=conv2.weight, shape=(16, 6, 5, 5), dtype=Float32, requires_grad=True)}
        >>> params_list = net.trainable_params()
        >>> ms.save_checkpoint(params_list, "./lenet_list.ckpt",
        ...                    choice_func=lambda x: x.startswith("conv") and not x.startswith("conv2"))
        >>> param_dict2 = ms.load_checkpoint("./lenet_list.ckpt")
        >>> print(param_dict2)
        {'conv1.weight': Parameter (name=conv1.weight, shape=(6, 1, 5, 5), dtype=Float32, requires_grad=True)}
        >>> ms.save_checkpoint(param_dict2, "./lenet_dict.ckpt")
        >>> param_dict3 = ms.load_checkpoint("./lenet_dict.ckpt")
        >>> print(param_dict3)
        {'conv1.weight': Parameter (name=conv1.weight, shape=(6, 1, 5, 5), dtype=Float32, requires_grad=True)}

    Tutorial Examples:
        - `Saving and Loading the Model - Saving and Loading the Model Weight
          <https://mindspore.cn/tutorials/en/master/beginner/save_load.html#saving-and-loading-the-model-weight>`_
    """
    ckpt_file_name = _check_save_obj_and_ckpt_file_name(save_obj, ckpt_file_name, format)
    integrated_save = Validator.check_bool(integrated_save)
    async_save = Validator.check_bool(async_save)
    append_dict = _check_append_dict(append_dict)
    enc_key = Validator.check_isinstance('enc_key', enc_key, (type(None), bytes))
    enc_mode = Validator.check_isinstance('enc_mode', enc_mode, str)
    crc_check = Validator.check_isinstance('crc_check', crc_check, bool)
    map_param_inc = kwargs.get('incremental', False)
    logger.info("Execute the process of saving checkpoint files.")
    global_step_num = kwargs.get('global_step_num', None)
    _check_format_and_other_params(format, enc_key, enc_mode, crc_check, async_save, map_param_inc, global_step_num)

    if append_dict and "__exception_save__" in append_dict:
        s1 = mindspore.hal.Stream()
        with mindspore.hal.StreamCtx(s1):
            save_obj = _convert_save_obj_to_param_list(save_obj, integrated_save, append_dict, choice_func)
        s1.synchronize()
    else:
        save_obj = _convert_save_obj_to_param_list(save_obj, integrated_save, append_dict, choice_func)

    if append_dict:
        if "__exception_save__" in append_dict:
            del append_dict["__exception_save__"]
        append_info_list = []
        for k_name, value in append_dict.items():
            if isinstance(value, Generator):
                value = value.get_state()
            elif not isinstance(value, str):
                value = Tensor(value)
            append_info_list.append({"name": k_name, "data": value})
        save_obj.extend(append_info_list)

    data_list = OrderedDict()
    data_list_np = OrderedDict()
    with _ckpt_mutex:
        for param in save_obj:
            if param["name"] == "random_op":
                if os.getenv("AITURBO") == "1":
                    data_list_np["random_op"] = []
                    data_list_np["random_op"].append(param["data"])
                    if crc_check:
                        bytes_value = bytes(data_list_np[key][0])
                        data_list_np[key].append(binascii.crc32(bytes_value))
                else:
                    data_list["random_op"] = param["data"]
                continue
            key = param["name"]
            data_list[key] = []
            data_list_np[key] = []
            if isinstance(param["data"], MapParameter):
                data_list[param["name"]].append("mapparameter")
                data_list[param["name"]].append(param["data"])
                continue
            if isinstance(param["data"], list):
                if param["data"][0] == "persistent_data":
                    _save_param_list_data(data_list, key, param)
                elif param["data"][0] == "offload_parameter":
                    data_list[key].append("offload_parameter")
                    _save_param_list_data(data_list, key, param)

            if isinstance(param["data"], str):
                if os.getenv("AITURBO") == "1":
                    data_list_np[key].append(np.array(param["data"]))
                    if crc_check:
                        bytes_value = data_list_np[key][0].tobytes()
                        data_list_np[key].append(binascii.crc32(bytes_value))
                else:
                    data_list[key].append([0])
                    data_list[key].append('str')
                    data = np.array(param["data"])
                    data_list[key].append(data)
            else:
                if isinstance(param["data"], Parameter):
                    param["data"].init_data()
                if os.getenv("AITURBO") == "1":
                    data_list_np[key].append(param["data"].asnumpy())
                    if crc_check:
                        bytes_value = data_list_np[key][0].tobytes()
                        data_list_np[key].append(binascii.crc32(bytes_value))
                else:
                    dims = []
                    for dim in param['data'].shape:
                        dims.append(dim)
                    data_list[key].append(dims)
                    tensor_type = str(param["data"].dtype)
                    data_list[key].append(tensor_type)
                    data = param["data"]
                    data_list[key].append(data)

    if os.getenv("AITURBO") == "1":
        from aiturbo.checkpoint import aiturbo_mindspore as aiturbo
        ckpt_name = os.path.basename(ckpt_file_name)
        aiturbo.save_ckpt(ckpt_name, global_step_num, data_list_np, crc_check)
    elif async_save:
        data_copy = copy.deepcopy(data_list)
        thr = Thread(target=_exec_save,
                     args=(ckpt_file_name, data_copy, enc_key, enc_mode, map_param_inc, crc_check, format),
                     name="asyn_save_ckpt")
        thr.start()
    else:
        _exec_save(ckpt_file_name, data_list, enc_key, enc_mode, map_param_inc, crc_check, format)

    logger.info("Saving checkpoint process is finished.")


def _convert_list_to_param_list(save_obj, choice_func):
    """Convert a list of Parameter to param_list."""
    param_list = []
    if not save_obj:
        return param_list
    if isinstance(save_obj[0], dict):
        for param in save_obj:
            if isinstance(param, dict) and "name" in param and "data" in param:
                if not isinstance(param["name"], str):
                    raise TypeError(f"For save_checkpoint, when save_obj is a list of dict items, the name in dict "
                                    f"should be string, but got {type(param['name'])}.")
                if not isinstance(param["data"], Tensor):
                    raise TypeError(f"For save_checkpoint, when save_obj is a list of dict items, the data in dict "
                                    f"should be parameter, but got {type(param['data'])}.")
                if choice_func is not None and not choice_func(param["name"]):
                    continue
                each_param = {"name": param["name"], "data": param["data"]}
                param_list.append(each_param)
            else:
                raise TypeError(f"For save_checkpoint, save_obj should be a list of dict items, and the dict should "
                                f"have key values 'name' and 'value', but got {type(param)} and {param}.")
    else:
        for param in save_obj:
            if isinstance(param, Parameter):
                if choice_func is not None and not choice_func(param.name):
                    continue
                each_param = {"name": param.name, "data": param}
                param_list.append(each_param)
            else:
                raise TypeError(f"For save_checkpoint, when save_obj is made up by list of Parameter,"
                                f"the param should be parameter, but got {type(param)}")
    return param_list


def _convert_dict_to_param_dict(save_obj, choice_func):
    """Convert a dict of Parameter to param_list."""
    param_list = []
    for (key, value) in save_obj.items():
        if isinstance(key, str) and isinstance(value, (Parameter, str)):
            if choice_func is not None and not choice_func(key):
                continue
            each_param = {"name": key, "data": value}
            param_list.append(each_param)
        else:
            raise TypeError(f"For save_checkpoint, when save_obj is made up by dict, the key should be str and"
                            f"value should be Parameter, but got the type of key is {type(key)} and"
                            f"the type of value is {type(value)}")
    return param_list


def _convert_cell_param_and_names_to_dict(save_obj, choice_func):
    """Convert cell.parameters_and_names to OrderedDict."""
    param_dict = OrderedDict()
    for _, param in save_obj.parameters_and_names():
        not_sliced = not param.sliced
        is_graph_mode = context.get_context('mode') == context.GRAPH_MODE
        # All parameters are initialized immediately under PyNative mode, skip this judgement.
        judgment = not_sliced or param.has_init
        if is_graph_mode and _is_in_auto_parallel_mode() and judgment:
            continue
        if choice_func is not None and not choice_func(param.name):
            continue
        # Add suffix for cache_enabled parameter, and then parameter can carry key info.
        # Notice that suffix needs be removed when loading into net.
        if param.cache_enable:
            param_dict[param.name + ".__param_key__" + str(param.key)] = param
        else:
            param_dict[param.name] = param
    return param_dict


def _convert_cell_to_param_list(save_obj, integrated_save, append_dict, choice_func):
    """Convert nn.Cell to param_list."""
    sync_pipeline_shared_parameters(save_obj)
    param_list = []
    parameter_layout_dict = save_obj.parameter_layout_dict
    if _is_in_auto_parallel_mode() and not parameter_layout_dict:
        parameter_layout_dict = _get_parameter_layout()
    if not _is_in_auto_parallel_mode():
        save_obj.init_parameters_data()
    param_dict = _convert_cell_param_and_names_to_dict(save_obj, choice_func)
    if append_dict and "random_op" in append_dict:
        phase = 'train' + '.' + str(save_obj.create_time) + '.' + str(id(save_obj)) + '.' + save_obj.arguments_key
        if phase in save_obj.compile_cache and _executor.has_compiled(phase):
            random_byte = _executor._graph_executor.get_random_status(phase)
            param_list.append({"name": "random_op", "data": random_byte})
            append_dict.pop("random_op")
    for (key, value) in param_dict.items():
        each_param = {"name": key}
        if isinstance(value, MapParameter):
            each_param["data"] = value
            param_list.append(each_param)
            continue

        if value.data.is_persistent_data():
            # list save persistent_data: [Tensor, shape, type, param.key]
            param_data = ["persistent_data", value.data, value.param_info.origin_shape, str(value.dtype), value.key]
        elif value.data.offload_file_path() != "":
            # list save offload data: [Param, shape, type, param.key]
            param_data = ["offload_parameter"]
            param_tensor = value.data
            if key in parameter_layout_dict:
                param_tensor = _get_merged_param_data(save_obj, parameter_layout_dict, key, param_tensor,
                                                      integrated_save)
            param_data.append(param_tensor)
            param_data.append(param_tensor.shape)
            param_data.append(str(param_tensor.dtype))
            param_data.append(value.key)
        else:
            param_data = value.data
            if append_dict and "__exception_save__" in append_dict:
                param_data = Tensor(Tensor_.move_to(value, "CPU", False))

            # in automatic model parallel scenario, some parameters were split to all the devices,
            # which should be combined before saving
            if key in parameter_layout_dict:
                if not append_dict or "__exception_save__" not in append_dict:
                    param_data = Tensor(value.data)
                param_data = _get_merged_param_data(save_obj, parameter_layout_dict, key, param_data,
                                                    integrated_save)

        each_param["data"] = param_data
        param_list.append(each_param)
    return param_list


def _convert_save_obj_to_param_list(save_obj, integrated_save, append_dict, choice_func):
    """Convert a save_obj to param_list."""
    if isinstance(save_obj, list):
        return _convert_list_to_param_list(save_obj, choice_func)

    if isinstance(save_obj, dict):
        return _convert_dict_to_param_dict(save_obj, choice_func)

    return _convert_cell_to_param_list(save_obj, integrated_save, append_dict, choice_func)


def _save_param_list_data(data_list, key, param):
    """Save persistent data into save_obj."""
    dims = []
    # persistent_data shape can not be ()
    for dim in param['data'][2]:
        dims.append(dim)
    data_list[key].append(dims)
    data_list[key].append(param['data'][3])
    data_list[key].append(param['data'][1])
    data_list[key].append(param['data'][4])


def _check_append_dict(append_dict):
    """Check the argument append_dict for save_checkpoint."""
    if append_dict is None:
        return append_dict
    if not isinstance(append_dict, dict):
        raise TypeError("For 'save_checkpoint', the argument 'append_dict' must be dict, but got "
                        "{}.".format(type(append_dict)))
    for key, value in append_dict.items():
        if not isinstance(key, str) or not isinstance(value, (int, float, bool, str, Parameter, Tensor, Generator)):
            raise TypeError(f"For 'save_checkpoint', the type of dict 'append_info' must be key: string, "
                            f"value: int, float, bool or Generator, but got key: {type(key)}, value: {type(value)}")
    return append_dict


def _check_load_obfuscate(**kwargs):
    if 'obf_func' in kwargs.keys():
        customized_func = _check_customized_func(kwargs.get('obf_func'))
        clean_funcs()
        add_opaque_predicate(customized_func.__name__, customized_func)
        return True
    return False


def load(file_name, **kwargs):
    """
    Load MindIR.

    The returned object can be executed by a `GraphCell`, see class :class:`mindspore.nn.GraphCell` for more details.

    Args:
        file_name (str): MindIR file name.

        kwargs (dict): Configuration options dictionary.

            - dec_key (bytes): Byte-type key used for decryption. The valid length is 16, 24, or 32.
            - dec_mode (Union[str, function]): Specifies the decryption mode, to take effect when dec_key is set.

              - Option: 'AES-GCM', 'AES-CBC', 'SM4-CBC' or customized decryption. Default: ``'AES-GCM'``.
              - For details of using the customized decryption, please check the `tutorial
                <https://mindspore.cn/mindarmour/docs/en/master/model_encrypt_protection.html>`_.

            - obf_func (function): A python function used for loading obfuscated MindIR model, which can refer to
              `obfuscate_model()
              <https://www.mindspore.cn/docs/en/master/api_python/mindspore/mindspore.obfuscate_model.html>`_.

    Returns:
        GraphCell, a compiled graph that can executed by `GraphCell`.

    Raises:
        ValueError: MindIR file does not exist or `file_name` is not a string.
        RuntimeError: Failed to parse MindIR file.

    Examples:
        >>> import numpy as np
        >>> import mindspore as ms
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor
        >>> from mindspore import context
        >>> context.set_context(mode=context.GRAPH_MODE)
        >>>
        >>> net = nn.Conv2d(1, 1, kernel_size=3, weight_init="ones")
        >>> input_tensor = Tensor(np.ones([1, 1, 3, 3]).astype(np.float32))
        >>> ms.export(net, input_tensor, file_name="net", file_format="MINDIR")
        >>> graph = ms.load("net.mindir")
        >>> net = nn.GraphCell(graph)
        >>> output = net(input_tensor)
        >>> print(output)
        [[[[4. 6. 4.]
           [6. 9. 6.]
           [4. 6. 4.]]]]

    Tutorial Examples:
        - `Saving and Loading the Model - Saving and Loading MindIR
          <https://mindspore.cn/tutorials/en/master/beginner/save_load.html#saving-and-loading-mindir>`_
    """
    if not isinstance(file_name, str):
        raise ValueError("For 'load', the argument 'file_name' must be string, but "
                         "got {}.".format(type(file_name)))
    if not file_name.endswith(".mindir"):
        raise ValueError("For 'load', the argument 'file_name'(MindIR file) should end with '.mindir', "
                         "please input the correct 'file_name'.")
    if not os.path.exists(file_name):
        raise ValueError("For 'load', the argument 'file_name'(MindIR file) does not exist, "
                         "please check whether the 'file_name' is correct.")
    file_name = os.path.realpath(file_name)

    # set customized functions for dynamic obfuscation
    obfuscated = _check_load_obfuscate(**kwargs)

    logger.info("Execute the process of loading mindir.")
    if 'dec_key' in kwargs.keys():
        dec_key = Validator.check_isinstance('dec_key', kwargs.get('dec_key'), bytes)
        dec_mode = "AES-GCM"
        dec_func = None
        if 'dec_mode' in kwargs.keys():
            if callable(kwargs.get('dec_mode')):
                dec_mode = "Customized"
                dec_func = kwargs.get('dec_mode')
            else:
                dec_mode = Validator.check_isinstance('dec_mode', kwargs.get('dec_mode'), str)
        graph = load_mindir(file_name, dec_key=dec_key, key_len=len(dec_key), dec_mode=dec_mode,
                            decrypt=dec_func, obfuscated=obfuscated)
    else:
        graph = load_mindir(file_name, obfuscated=obfuscated)

    if graph is None:
        if _is_cipher_file(file_name):
            raise RuntimeError("Load MindIR failed. The file may be encrypted and decrypt failed, you "
                               "can check whether the values of the arguments 'dec_key' and 'dec_mode'"
                               " are the same as when exported MindIR file, or check the file integrity.")
        raise RuntimeError("Load MindIR failed.")
    return graph


def export_split_mindir(file_name, device_num=8, rank_id=0, dynamic=True, sapp=True):
    """
    Auto Split MindIR.

    The returned object can be executed by a `GraphCell`, see class :class:`mindspore.nn.GraphCell` for more details.

    Args:
        file_name (str): MindIR file name.
        device_num (int): device number. Default: '8'.
        rank_id (int): rank id. Default: '0'.
        dynamic (bool): Indicates whether the model is a dynamic shape mindir model. Default: 'True'.
        sapp (bool): Indicates whether to automatically generate split strategy through SAPP. Default: 'True'.

    Raises:
        ValueError: MindIR file does not exist or `file_name` is not a string.
        RuntimeError: Failed to split MindIR file.

    Examples:
        >>> import mindspore as ms
        >>> context.set_context(mode=context.GRAPH_MODE)
        >>>
        >>> ms.export_split_mindir("net.mindir", device_num=8, rank_id=0)

    """
    if not isinstance(file_name, str):
        raise ValueError("For 'Split MindIR', the argument 'file_name' must be string, but "
                         "got {}.".format(type(file_name)))
    if not file_name.endswith(".mindir"):
        raise ValueError("For 'Split MindIR', the argument 'file_name'(MindIR file) should end with '.mindir', "
                         "please input the correct 'file_name'.")
    if not os.path.exists(file_name):
        raise ValueError("For 'Split MindIR', the argument 'file_name'(MindIR file) does not exist, "
                         "please check whether the 'file_name' is correct.")
    file_name = os.path.realpath(file_name)

    logger.info("Execute the process of export and split mindir.")
    dynamic = True
    if dynamic:
        graph = split_dynamic_mindir(file_name, device_num, rank_id, sapp)
    else:
        graph = split_mindir(file_name)

    if graph is None:
        if _is_cipher_file(file_name):
            raise RuntimeError("Export and split MindIR failed. The file may be encrypted and decrypt failed, you "
                               "can check whether the values of the arguments 'dec_key' and 'dec_mode'"
                               " are the same as when exported MindIR file, or check the file integrity.")
        raise RuntimeError("Export and split MindIR failed.")
    return graph


def _check_param_type(param_config, key, target_type, requested):
    """check type of parameters"""
    if key in param_config:
        if not isinstance(param_config[key], target_type):
            raise TypeError("The type of {} must be {}, but got {}.".format(key, target_type, type(param_config[key])))
        if key == 'obf_random_seed':
            if param_config[key] > INT_64_MAX or param_config[key] <= 0:
                raise ValueError(
                    "'obf_random_seed' must be in (0, INT_64_MAX({})], but got {}.".format(INT_64_MAX,
                                                                                           param_config[key]))
        return param_config[key]
    if requested:
        raise ValueError("The parameter {} is requested, but not got.".format(key))
    if key == "obf_random_seed":
        return 0
    return None


def _check_customized_func(customized_func):
    """ check customized function of dynamic obfuscation """
    if not callable(customized_func):
        raise TypeError(
            "'customized_func' must be a function, but not got {}.".format(type(customized_func)))
    # test customized_func
    try:
        func_result = customized_func(1.0, 1.0)
    except Exception as ex:
        raise TypeError("customized_func must be a function with two inputs, but got exception: {}".format(ex))
    else:
        if not isinstance(func_result, bool):
            raise TypeError("Return value of customized_func must be boolean, but got: {}".format(type(func_result)))
    return customized_func


def _check_obfuscate_params(obf_config):
    """Check obfuscation parameters, including obf_random_seed, obf_ratio, customized_func"""
    if 'obf_random_seed' not in obf_config.keys() and 'customized_func' not in obf_config.keys():
        raise ValueError(
            "At least one of 'obf_random_seed' or 'customized_func' must be set in obf_config, but got None of them.")
    obfuscate_type = _check_param_type(obf_config, "type", str, False)
    if obfuscate_type not in (None, "dynamic"):
        raise ValueError("Only 'dynamic' type is supported by now, but got {}.".format(obfuscate_type))
    if ('obf_ratio' in obf_config) and isinstance(obf_config['obf_ratio'], str):
        if obf_config['obf_ratio'] not in ["small", "medium", "large"]:
            raise ValueError("'obf_ratio' can only be 'small', 'medium', 'large' or float, but got {}.".format(
                obf_config['obf_ratio']))
        ratio_dict = {"small": 0.1, "medium": 0.3, "large": 0.6}
        obf_config['obf_ratio'] = ratio_dict.get(obf_config['obf_ratio'])
    obf_ratio = _check_param_type(obf_config, "obf_ratio", float, True)
    if (obf_ratio <= 0) or (obf_ratio > 1):
        raise ValueError("'obf_ratio' must be in (0, 1] if it is a float, but got {}.".format(obf_config['obf_ratio']))
    customized_funcs = []
    if 'customized_func' in obf_config.keys():
        device_target = context.get_context('device_target')
        if device_target in ["GPU", "Ascend"]:
            raise ValueError(
                "Customized func mode only support 'device_target'='CPU, but got {}.".format(device_target))
        customized_funcs.append(_check_customized_func(obf_config['customized_func']))
    obf_random_seed = _check_param_type(obf_config, "obf_random_seed", int, False)
    return obf_ratio, customized_funcs, obf_random_seed


def obfuscate_model(obf_config, **kwargs):
    """
    Obfuscate a model of MindIR format. Obfuscation means changing the struct of a network without affecting its
    predict correctness. The obfuscated model can prevent attackers from stealing the model.

    Args:
        obf_config (dict): obfuscation config.

            - type (str): The type of obfuscation, only 'dynamic' is supported until now.
            - original_model_path (str): The path of MindIR format model that need to be obfuscated. If the original
              model is encrypted, then enc_key and enc_mode should be provided.
            - save_model_path (str): The path to save the obfuscated model.
            - model_inputs (list(Tensor)): The inputs of the original model, the values of Tensor can be random, which
              is the same as using :func:`mindspore.export`.
            - obf_ratio (Union(float, str)): The ratio of nodes in original model that would be obfuscated. `obf_ratio`
              should be in range of (0, 1] or in ["small", "medium", "large"]. "small", "medium" and "large" are
              correspond to 0.1, 0.3, and 0.6 respectively.
            - customized_func (function): A python function used for customized function mode, which used for control
              the switch branch of obfuscation structure. The outputs of customized_func should be boolean and const (
              Reference to 'my_func()' in
              `tutorials <https://www.mindspore.cn/mindarmour/docs/en/master/dynamic_obfuscation_protection.html>`_).
              This function needs to ensure that its result is constant for any input. Users can refer to opaque
              predicates. If customized_func is set, then it should be passed to :func:`mindspore.load` interface
              when loading obfuscated model.
            - obf_random_seed (int): Obfuscation random seed, which should be in (0, 9223372036854775807]. The
              structure of obfuscated models corresponding to different random seeds is different. If
              `obf_random_seed` is set, then it should be passed to :class:`mindspore.nn.GraphCell`
              interface when loading
              obfuscated model. It should be noted that at least one of `customized_func` or `obf_random_seed` should
              be set, and the latter mode would be applied if both of them are set.

        kwargs (dict): Configuration options dictionary.

            - enc_key (bytes): Byte type key used for encryption. The valid length is 16, 24, or 32.
            - enc_mode (str): Specifies the encryption mode, to take effect when dec_key is set.
              Options: ``'AES-GCM'`` | ``'AES-CBC'`` | ``'SM4-CBC'``. Default: ``'AES-GCM'``.

    Raises:
        TypeError: If `obf_config` is not a dict.
        ValueError: If `enc_key` is passed and `enc_mode` is not in ["AES-GCM", "AES-CBC", "SM4-CBC"].
        ValueError: If `original_model_path` is not provided in `obf_config`.
        ValueError: If the model saved in `original_model_path` has been obfuscated.
        ValueError: If `save_model_path` is not provided in `obf_config`.
        ValueError: If `obf_ratio` is not provided in `obf_config`.
        ValueError: If both `customized_func` and `obf_random_seed` are not provided in `obf_config`.
        ValueError: If `obf_random_seed` is not in (0, 9223372036854775807].
        ValueError: If `original_model_path` does not exist or `original_model_path` does not end with '.mindir'.

    Examples:
        >>> import mindspore as ms
        >>> import mindspore.nn as nn
        >>> import numpy as np
        >>> # Download ori_net.mindir
        >>> # https://gitee.com/mindspore/mindspore/blob/master/tests/ut/python/mindir/ori_net.mindir
        >>> input1 = ms.Tensor(np.ones((1, 1, 32, 32)).astype(np.float32))
        >>> obf_config = {'original_model_path': "./net.mindir",
        ...          'save_model_path': "./obf_net",
        ...          'model_inputs': [input1, ],
        ...          'obf_ratio': 0.1, 'obf_random_seed': 173262358423}
        >>> ms.obfuscate_model(obf_config)
        >>> obf_func = ms.load("obf_net.mindir")
        >>> obf_net = nn.GraphCell(obf_func, obf_random_seed=173262358423)
        >>> print(obf_net(input1).asnumpy())
    """
    if not isinstance(obf_config, dict):
        raise TypeError("'obf_config' must be a dict, but got {}.".format(type(obf_config)))
    file_path = _check_param_type(obf_config, "original_model_path", str, True)
    if not file_path.endswith(".mindir"):
        raise ValueError("For 'obfuscate_model', the argument 'file_path'(MindIR file) should end with '.mindir', "
                         "please input the correct 'file_path'.")
    if not os.path.exists(file_path):
        raise ValueError("For 'obfuscate_model', the argument 'file_path'(MindIR file) does not exist, "
                         "please check whether the 'file_path' is correct.")
    saved_path = _check_param_type(obf_config, "save_model_path", str, True)
    model_inputs = _check_param_type(obf_config, "model_inputs", list, True)
    for item in model_inputs:
        if not isinstance(item, Tensor):
            raise TypeError("The item in 'model_inputs' must be Tensor, but got {}.".format(type(item)))
        if -1 in item.shape:
            raise ValueError(
                "Dynamic shape input is not supported now, but got the shape of inputs: {}.".format(item.shape))
    obf_ratio, customized_funcs, obf_random_seed = _check_obfuscate_params(obf_config)
    if customized_funcs and obf_random_seed > 0:
        logger.warning("Although 'customized_func' and 'obf_random_seed' are set, the 'obf_random_seed' mode would be"
                       " applied, remember to set 'obf_random_seed' when loading obfuscated model.")

    if obf_random_seed == 0:  # apply customized_func mode
        clean_funcs()
        for func in customized_funcs:
            add_opaque_predicate(func.__name__, func)
        branch_control_input = 0
    else:  # apply password mode
        branch_control_input = _generate_branch_control_input(obf_random_seed)

    if 'enc_key' in kwargs.keys():
        enc_key = Validator.check_isinstance('enc_key', kwargs.get('enc_key'), bytes)
        enc_mode = "AES-GCM"
        if 'enc_mode' in kwargs.keys():
            enc_mode = Validator.check_isinstance('enc_mode', kwargs.get('enc_mode'), str)
            if enc_mode not in ["AES-GCM", "AES-CBC", "SM4-CBC"]:
                raise ValueError(
                    "Only MindIR files that encrypted with 'AES-GCM', 'AES-CBC' or 'SM4-CBC' is supported for"
                    "obfuscate_model(), but got {}.".format(enc_mode))
        obf_graph = dynamic_obfuscate_mindir(file_name=file_path, obf_ratio=obf_ratio,
                                             branch_control_input=branch_control_input, dec_key=enc_key,
                                             key_len=len(enc_key),
                                             dec_mode=enc_mode)
    else:
        obf_graph = dynamic_obfuscate_mindir(file_name=file_path, obf_ratio=obf_ratio,
                                             branch_control_input=branch_control_input)

    obf_net = nn.GraphCell(obf_graph)
    if obf_random_seed != 0:
        append_y_tensor = Tensor(np.ones((1, 1)).astype(np.int32))
        model_inputs += [append_y_tensor]
    export(obf_net, *model_inputs, file_name=saved_path, file_format="MINDIR", **kwargs)


def _load_into_param_dict(ckpt_file_name, parameter_dict, specify_prefix, filter_prefix, choice_func, dec_key,
                          dec_mode, crc_check, format):
    """load parameter into parameter_dict"""
    ckpt_file_name = _check_ckpt_file_name(ckpt_file_name, format)
    if format == "safetensors":
        with safe_open(ckpt_file_name, framework='np') as f:
            sf_load_time_start = time.time()
            for k in f.keys():
                parameter_dict[k] = Parameter(Tensor.from_numpy(f.get_tensor(k)))
            sf_load_time_end = time.time()
            cost_time = sf_load_time_end - sf_load_time_start
            vlog_print("1", "ME", __file__, sys._getframe().f_lineno, f"Load safetensors cost time:{cost_time}.")
        return
    checkpoint_list = _parse_ckpt_proto(ckpt_file_name, dec_key, dec_mode, crc_check)
    try:
        param_data_list = []
        map_data_list = [[], [], []]
        map_shape_list = [0, 0, 0]
        if specify_prefix:
            logger.warning("For load_checkpoint, this parameter `specity_prefix` will be deprecated, "
                           "please use `choice_func` instead.")
        if filter_prefix:
            logger.warning("For load_checkpoint, this parameter `filter_prefix` will be deprecated, "
                           "please use `choice_func` instead.")
        for element_id, element in enumerate(checkpoint_list.value):
            if element.tag == "random_op":
                parameter_dict["random_op"] = element.tensor.tensor_content
                continue
            if not _whether_load_param(specify_prefix, filter_prefix, element.tag):
                continue
            if specify_prefix is None and filter_prefix is None and \
                    choice_func is not None and not choice_func(element.tag):
                continue
            if element.tensor.ByteSize() == 0:
                _load_map_parameter(checkpoint_list, element, element_id, map_data_list, map_shape_list,
                                    parameter_dict)
                if element.tag in parameter_dict:
                    map_data_list = [[], [], []]
                    map_shape_list = [0, 0, 0]
                continue
            data = element.tensor.tensor_content
            data_type = element.tensor.tensor_type
            np_type = tensor_to_np_type.get(data_type)
            ms_type = tensor_to_ms_type[data_type]
            if data_type == 'str':
                str_length = int(len(data) / 4)
                np_type = np_type + str(str_length)
            param_data_list.append(data)
            if (element_id == len(checkpoint_list.value) - 1) or \
                    (element.tag != checkpoint_list.value[element_id + 1].tag):
                new_data = b"".join(param_data_list)
                param_data_list.clear()
                dims = element.tensor.dims
                if data_type == 'str':
                    str_value = np.frombuffer(new_data, np_type)
                    parameter_dict[element.tag] = str(str_value[0])
                else:
                    if dims == [0]:
                        dims = []
                    param_data = Tensor_.convert_bytes_to_tensor(new_data, tuple(dims), ms_type)
                    parameter = Parameter(param_data, name=element.tag)
                    parameter_dict[element.tag] = parameter
                    _offload_if_config(parameter)

        logger.info("Loading checkpoint files process is finished.")

    except BaseException as e:
        logger.critical("Failed to load the checkpoint file '%s'.", ckpt_file_name)
        raise ValueError(e.__str__() + "\nFor 'load_checkpoint', "
                                       "failed to load the checkpoint file {}.".format(ckpt_file_name)) from e


def load_checkpoint(ckpt_file_name, net=None, strict_load=False, filter_prefix=None,
                    dec_key=None, dec_mode="AES-GCM", specify_prefix=None, choice_func=None,
                    crc_check=False, remove_redundancy=False, format="ckpt"):
    """
    Load checkpoint info from a specified file.

    Note:
        - `specify_prefix` and `filter_prefix` do not affect each other.
        - If none of the parameters are loaded from checkpoint file, it will throw ValueError.
        - `specify_prefix` and `filter_prefix` are in the process of being deprecated,
          `choice_func` is recommended instead.
          And using either of those two args will override `choice_func` at the same time.
        - When loading a checkpoint that has removed redundancy, the network should be compiled.

    Args:
        ckpt_file_name (str): Checkpoint file name.
        net (Cell): The network where the parameters will be loaded. Default: ``None`` .
        strict_load (bool): Whether to strict load the parameter into net. If ``False`` , it will load parameter
                            into net when parameter name's suffix in checkpoint file is the same as the
                            parameter in the network. When the types are inconsistent perform type conversion
                            on the parameters of the same type, such as float32 to float16. Default: ``False`` .
        filter_prefix (Union[str, list[str], tuple[str]]): Deprecated(see `choice_func`). Parameters starting with the
            filter_prefix will not be loaded. Default: ``None`` .
        dec_key (Union[None, bytes]): Byte type key used for decryption. If the value is ``None`` , the decryption
                                      is not required. Default: ``None`` .
        dec_mode (str): This parameter is valid only when dec_key is not set to ``None`` . Specifies the decryption
                        mode, currently supports ``"AES-GCM"`` and ``"AES-CBC"`` and ``"SM4-CBC"`` .
                        Default: ``"AES-GCM"`` .
        specify_prefix (Union[str, list[str], tuple[str]]): Deprecated(see `choice_func`). Parameters starting with the
            specify_prefix will be loaded. Default: ``None`` .
        choice_func (Union[None, function]) : Input value of the function is a Parameter name of type string,
            and the return value is a bool. If returns ``True`` , the Parameter
            that matches the custom condition will be loaded. If returns ``False`` , the Parameter that
            matches the custom condition will be removed. Default: ``None`` .
        crc_check (bool) : Whether to perform crc32 validation when loading checkpoint. Default: ``False`` .
        remove_redundancy (bool): Whether to enable loading of checkpoint saved with redundancy removal.
            Redundancy removal refers to eliminating redundant data in data parallelism mode. Default: ``False`` , means
            redundant-free loading is not enabled.
        format (str): Format of the input file, can be "ckpt" or "safetensors". Default: "ckpt".

    Returns:
        Dict, key is parameter name, value is a Parameter or string. When the `append_dict` parameter of
        :func:`mindspore.save_checkpoint` and the `append_info` parameter of :class:`mindspore.train.CheckpointConfig`
        are used to save the checkpoint, `append_dict` and `append_info` are dict types, and their value are string,
        then the return value obtained by loading checkpoint is string, and in other cases the return value is
        Parameter.

    Raises:
        ValueError: Checkpoint file's format is incorrect.
        ValueError: Parameter's dict is None after load checkpoint file.
        TypeError: The type of `specify_prefix` or `filter_prefix` is incorrect.

    Examples:
        >>> import mindspore as ms
        >>>
        >>> ckpt_file_name = "./checkpoint/LeNet5-1_32.ckpt"
        >>> param_dict = ms.load_checkpoint(ckpt_file_name,
        ...                                 choice_func=lambda x: x.startswith("conv") and not x.startswith("conv1"))
        >>> print(param_dict["conv2.weight"])
        Parameter (name=conv2.weight, shape=(16, 6, 5, 5), dtype=Float32, requires_grad=True)
        >>> def func(param_name):
        ...     whether_load = False
        ...     if param_name.startswith("conv"):
        ...         whether_load = True
        ...     if param_name.startswith("conv1"):
        ...         whether_load = False
        ...     return whether_load
        >>> param_dict1 = ms.load_checkpoint(ckpt_file_name, choice_func=func)
        >>> print(param_dict1["conv2.weight"])
        Parameter (name=conv2.weight, shape=(16, 6, 5, 5), dtype=Float32, requires_grad=True)
        >>> def func(param_name):
        ...     whether_load = False
        ...     if param_name.startswith("conv1"):
        ...         whether_load = True
        ...     return whether_load
        >>> param_dict2 = ms.load_checkpoint(ckpt_file_name, choice_func=func)
        >>> print(param_dict2)
        {'conv1.weight': Parameter (name=conv1.weight, shape=(6, 1, 5, 5), dtype=Float32, requires_grad=True)}

    Tutorial Examples:
        - `Saving and Loading the Model - Saving and Loading the Model Weight
          <https://mindspore.cn/tutorials/en/master/beginner/save_load.html#saving-and-loading-the-model-weight>`_
    """
    vlog_print("1", "ME", __file__, sys._getframe().f_lineno, "Begin load checkpoint.")
    specify_prefix = _check_prefix(specify_prefix)
    filter_prefix = _check_prefix(filter_prefix)
    dec_key = Validator.check_isinstance('dec_key', dec_key, (type(None), bytes))
    dec_mode = Validator.check_isinstance('dec_mode', dec_mode, str)
    crc_check = Validator.check_isinstance('crc_check', crc_check, bool)
    remove_redundancy = Validator.check_isinstance('remove_redundancy', remove_redundancy, bool)
    _check_format_and_other_params(format, dec_key, dec_mode, crc_check)
    logger.info("Execute the process of loading checkpoint files.")

    parameter_dict = {}

    if os.getenv("AITURBO") == "1":
        rank_id = get_rank()
        from aiturbo.checkpoint import aiturbo_mindspore as aiturbo
        ckpt_path = os.path.dirname(ckpt_file_name)
        ckpt_name = os.path.basename(ckpt_file_name)
        np_dict = aiturbo.load_ckpt(ckpt_path, ckpt_name, rank_id, crc_check)
        for key, value in np_dict.items():
            if crc_check and len(value) != 2:
                raise ValueError(f"When loading a checkpoint from AITurbo, if CRC check is enabled, "
                                 f"the length of the value must be 2, but got {len(value)}.")
            if isinstance(value, str):
                if crc_check and value[1] != binascii.crc32(np.array(value[0]).tobytes()):
                    raise ValueError(f"When loading a checkpoint from AITurbo, the value of the string has not "
                                     f"passed the CRC check and has been corrupted.")
                parameter_dict[key] = value[0]
            else:
                if crc_check and value[1] != binascii.crc32(value[0].tobytes()):
                    raise ValueError(f"When loading a checkpoint from AITurbo, the value of the parameter has not "
                                     f"passed the CRC check and has been corrupted.")
                parameter_dict[key] = Parameter(Tensor(value[0]), name=key)
    else:
        _load_into_param_dict(ckpt_file_name, parameter_dict, specify_prefix, filter_prefix, choice_func, dec_key,
                              dec_mode, crc_check, format)

    if not parameter_dict:
        raise ValueError(f"The loaded parameter dict is empty after filter or specify, please check whether "
                         f"'filter_prefix' or 'specify_prefix' are set correctly.")

    if _warm_up_host_cache_enabled(parameter_dict):
        (is_worker, net_dict, warm_up_dict) = _warm_up_host_cache(parameter_dict, net)
    if net is not None:
        load_param_into_net(net, parameter_dict, strict_load, remove_redundancy)
    if _warm_up_host_cache_enabled(parameter_dict):
        _warm_up_host_cache_post_process(is_worker, net_dict, warm_up_dict)

    vlog_print("1", "ME", __file__, sys._getframe().f_lineno, "Load checkpoint is finished.")
    return parameter_dict


def load_checkpoint_async(ckpt_file_name, net=None, strict_load=False, filter_prefix=None, dec_key=None,
                          dec_mode="AES-GCM", specify_prefix=None, choice_func=None):
    """
    Load checkpoint info from a specified file asyncly.

    .. warning::
        This is an experimental API that is subject to change or deletion.

    Note:
        - `specify_prefix` and `filter_prefix` do not affect each other.
        - If none of the parameters are loaded from checkpoint file, it will throw ValueError.
        - `specify_prefix` and `filter_prefix` are in the process of being deprecated,
          `choice_func` is recommended instead.
          And using either of those two args will override `choice_func` at the same time.

    Args:
        ckpt_file_name (str): Checkpoint file name.
        net (Cell, optional): The network where the parameters will be loaded. Default: ``None`` .
        strict_load (bool, optional): Whether to strict load the parameter into net. If ``False`` , it will load
                                      parameter into net when parameter name's suffix in checkpoint file is the
                                      same as the parameter in the network. When the types are inconsistent
                                      perform type conversion on the parameters of the same type, such as float32
                                      to float16. Default: ``False`` .
        filter_prefix (Union[str, list[str], tuple[str]], optional): Deprecated(see `choice_func`). Parameters
            starting with the `filter_prefix` will not be loaded. Default: ``None`` .
        dec_key (Union[None, bytes], optional): Byte type key used for decryption. If the value is ``None`` ,
                                                the decryption is not required. Default: ``None`` .
        dec_mode (str, optional): This parameter is valid only when dec_key is not set to ``None`` . Specifies
                                  the decryption mode, currently supports ``"AES-GCM"`` and ``"AES-CBC"``
                                  and ``"SM4-CBC"`` . Default: ``"AES-GCM"`` .
        specify_prefix (Union[str, list[str], tuple[str]], optional): Deprecated(see `choice_func`). Parameters
            starting with the specify_prefix will be loaded. Default: ``None`` .
        choice_func (Union[None, function], optional): Input value of the function is a Parameter name of type
            string, and the return value is a bool. If returns ``True`` , the Parameter
            that matches the custom condition will be loaded. If returns ``False`` , the Parameter that
            matches the custom condition will be removed. Default: ``None`` .

    Returns:
        A custom inner class, calling its `result` method yields the :func:`mindspore.load_checkpoint` result.

    Raises:
        ValueError: Checkpoint file's format is incorrect.
        ValueError: Parameter's dict is None after load checkpoint file.
        TypeError: The type of `specify_prefix` or `filter_prefix` is incorrect.

    Examples:
        >>> import mindspore
        >>> from mindspore import nn
        >>> from mindspore.train import Model
        >>> from mindspore.amp import FixedLossScaleManager
        >>> from mindspore import context
        >>> from mindspore import load_checkpoint_async
        >>> from mindspore import load_param_into_net
        >>> context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")
        >>> # Create the dataset taking MNIST as an example. Refer to
        >>> # https://gitee.com/mindspore/docs/blob/master/docs/mindspore/code/mnist.py
        >>> dataset = create_dataset()
        >>> # Define the network structure of LeNet5. Refer to
        >>> # https://gitee.com/mindspore/docs/blob/master/docs/mindspore/code/lenet.py
        >>> ckpt_file = "./checkpoint/LeNet5-1_32.ckpt"
        >>> net = LeNet5()
        >>> loss = nn.SoftmaxCrossEntropyWithLogits(sparse=True, reduction="mean")
        >>> loss_scale_manager = FixedLossScaleManager()
        >>> optim = nn.Momentum(params=net.trainable_params(), learning_rate=0.1, momentum=0.9)
        >>> model = Model(net, loss_fn=loss, optimizer=optim, metrics=None,
        ...               loss_scale_manager=loss_scale_manager)
        >>> pd_future = load_checkpoint_async(ckpt_file)
        >>> model.build(train_dataset=dataset, epoch=2)
        >>> param_dict = pd_future.result()
        >>> load_param_into_net(net, param_dict)
        >>> model.train(2, dataset)
        >>> print("param dict len: ", len(param_dict), flush=True)
    """
    from concurrent.futures import ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=2)
    param_dict_future = executor.submit(load_checkpoint, ckpt_file_name, net, strict_load, filter_prefix,
                                        dec_key, dec_mode, specify_prefix, choice_func)
    return ParamDictFuture(executor, param_dict_future)


def _load_map_parameter(checkpoint_list, element, element_id, map_data_list,
                        map_shape_list, parameter_dict):
    """load map parameter."""
    logger.info("Checkpoint load map_parameter.")
    if (element_id != len(checkpoint_list.value) - 1) and \
            element.tag == checkpoint_list.value[element_id + 1].tag:
        for index, tensor in enumerate(element.maptensor.tensor):
            data = tensor.tensor_content
            data_type = tensor.tensor_type
            np_type = np_type_convert.get(data_type)
            element_data = np.frombuffer(data, np_type)
            map_data_list[index].append(element_data)
            map_shape_list[index] += tensor.dims[0]
    else:
        map_array = []
        for index, tensor in enumerate(element.maptensor.tensor):
            data = tensor.tensor_content
            data_type = tensor.tensor_type
            np_type = np_type_convert.get(data_type)
            element_data = np.frombuffer(data, np_type)
            map_data_list[index].append(element_data)
            new_data = b"".join(map_data_list[index])
            param_data = np.frombuffer(new_data, np_type)
            dims = tensor.dims
            dims[0] += map_shape_list[index]
            param_data = param_data.reshape(list(dims))
            map_array.append(param_data)
        parameter_dict[element.tag] = map_array


def _check_ckpt_file_name(ckpt_file_name, format):
    """Check function load_checkpoint's ckpt_file_name."""
    if not isinstance(ckpt_file_name, str):
        raise TypeError("For 'load_checkpoint', the argument 'ckpt_file_name' must be string, "
                        "but got {}.".format(type(ckpt_file_name)))

    if format not in ['ckpt', 'safetensors']:
        raise ValueError("For 'load_checkpoint', the checkpoint file should end with '.ckpt' or '.safetensors', please "
                         "input the correct 'ckpt_file_name'.")
    if not ckpt_file_name.endswith(format):
        raise ValueError(f"For 'load_checkpoint', the checkpoint file format must same with 'format', but got "
                         f"file_name:'{ckpt_file_name}', format:'{format}'")

    ckpt_file_name = os.path.realpath(ckpt_file_name)
    if not os.path.exists(ckpt_file_name):
        raise ValueError("For 'load_checkpoint', the checkpoint file: {} does not exist, please check "
                         "whether the 'ckpt_file_name' is correct.".format(ckpt_file_name))

    return ckpt_file_name


def _check_prefix(prefix):
    """Check the correctness of the parameters."""
    if prefix is None:
        return prefix
    if not isinstance(prefix, (str, list, tuple)):
        raise TypeError("For 'load_checkpoint', the type of 'specify_prefix' or 'filter_prefix' must be string, "
                        "list[string] or tuple[string], but got {}.".format(str(type(prefix))))
    if isinstance(prefix, str):
        prefix = (prefix,)
    if not prefix:
        raise ValueError("For 'load_checkpoint', the argument 'specify_prefix' or 'filter_prefix' can't be empty when"
                         " 'specify_prefix' or 'filter_prefix' is list or tuple.")
    for index, pre in enumerate(prefix):
        if not isinstance(pre, str):
            raise TypeError("For 'load_checkpoint', when 'specify_prefix' or 'filter_prefix' is list or tuple, "
                            "the element in it must be string, but got "
                            f"{str(type(pre))} at index {index}.")
        if pre == "":
            raise ValueError("For 'load_checkpoint', the value of 'specify_prefix' or 'filter_prefix' "
                             "can't include ''.")
    return prefix


def _parse_ckpt_proto(ckpt_file_name, dec_key, dec_mode, crc_check):
    """Parse checkpoint protobuf."""
    checkpoint_list = Checkpoint()
    try:
        if dec_key is None:
            with _ckpt_fs.open(ckpt_file_name, *_ckpt_fs.open_args) as f:
                ckpt_load_time_start = time.time()
                pb_content = f.read()
                ckpt_load_time_end = time.time()
                cost_time = ckpt_load_time_end - ckpt_load_time_start
                vlog_print("1", "ME", __file__, sys._getframe().f_lineno, f"Load ckpt cost time:{cost_time}.")

        else:
            pb_content = _decrypt(ckpt_file_name, dec_key, len(dec_key), dec_mode)
            if pb_content is None:
                raise ValueError("For 'load_checkpoint', failed to decrypt the checkpoint file.")
        if crc_check and pb_content[-17:-10] != b"crc_num":
            logger.warning("For 'load_checkpoint', the ckpt file do not contain the crc code, please check the file.")
        if pb_content[-17:-10] == b"crc_num":
            crc_num_bytes = pb_content[-10:]
            pb_content = pb_content[:-17]
            if crc_check:
                crc_num = int.from_bytes(crc_num_bytes, byteorder='big')
                cal_crc_num = binascii.crc32(pb_content, 0)
                if cal_crc_num != crc_num:
                    raise ValueError("For 'load_checkpoint', the crc check is failed, "
                                     "please check whether the ckpt file is damaged.")
        checkpoint_list.ParseFromString(pb_content)
    except google.protobuf.message.DecodeError as e:
        raise ValueError(f"Failed to read the checkpoint file {ckpt_file_name}. "
                         f"The file may be corrupted, and the content cannot be parsed.") from e
    except BaseException as e:
        if _is_cipher_file(ckpt_file_name):
            err_info = "Failed to read the checkpoint file {}. The file may be encrypted or tempered with, " \
                       "please pass in the correct 'dec_key' or check the file integrity.".format(ckpt_file_name)
        else:
            err_info = "Failed to read the checkpoint file {}. May not have permission to read it, please check" \
                       " the correct of the file.".format(ckpt_file_name)
        logger.error(err_info)
        raise ValueError(err_info) from e
    return checkpoint_list


def _whether_load_param(specify_prefix, filter_prefix, param_name):
    """Checks whether the load the parameter after `specify_prefix` or `filter_prefix`."""
    whether_load = True
    if specify_prefix:
        whether_load = False
        for prefix in specify_prefix:
            if param_name.startswith(prefix):
                whether_load = True
                break
    if filter_prefix:
        for prefix in filter_prefix:
            if param_name.startswith(prefix):
                whether_load = False
                break
    return whether_load


def _check_load_param_into_net(net, parameter_dict):
    """check load_param_into_net"""
    if not isinstance(net, nn.Cell):
        logger.critical("Failed to combine the net and the parameters.")
        msg = ("For 'load_param_into_net', the argument 'net' should be a Cell, but got {}.".format(type(net)))
        raise TypeError(msg)
    if not isinstance(parameter_dict, dict):
        logger.critical("Failed to combine the net and the parameters.")
        msg = ("For 'load_param_into_net', the argument 'parameter_dict' should be a dict, "
               "but got {}.".format(type(parameter_dict)))
        raise TypeError(msg)
    if "random_op" in parameter_dict.keys():
        net._add_attr("random_op_snapshot", parameter_dict["random_op"])
        parameter_dict.pop("random_op")


def load_param_into_net(net, parameter_dict, strict_load=False, remove_redundancy=False):
    """
    Load parameters into network, return parameter list that are not loaded in the network.

    Note:
        - When loading a parameter dict that has removed redundancy, the network should be compiled.

    Args:
        net (Cell): The network where the parameters will be loaded.
        parameter_dict (dict): The dictionary generated by load checkpoint file,
                               it is a dictionary consisting of key: parameters's name, value: parameter.
        strict_load (bool): Whether to strict load the parameter into net. If ``False`` , it will load parameter
                            into net when parameter name's suffix in checkpoint file is the same as the
                            parameter in the network. When the types are inconsistent perform type conversion
                            on the parameters of the same type, such as float32 to float16. Default: ``False`` .
        remove_redundancy (bool): Whether to enable loading of checkpoint saved with redundancy removal.
            Redundancy removal refers to eliminating redundant data in data parallelism mode. Default: ``False`` , means
            redundant-free loading is not enabled.

    Returns:
        - param_not_load (List), the parameter name in model which are not loaded into the network.
        - ckpt_not_load (List), the parameter name in checkpoint file which are not loaded into the network.

    Raises:
        TypeError: Argument is not a Cell, or parameter_dict is not a Parameter dictionary.

    Examples:
        >>> import mindspore as ms
        >>>
        >>> # Define the network structure of LeNet5. Refer to
        >>> # https://gitee.com/mindspore/docs/blob/master/docs/mindspore/code/lenet.py
        >>> net = LeNet5()
        >>> ckpt_file_name = "./checkpoint/LeNet5-1_32.ckpt"
        >>> param_dict = ms.load_checkpoint(ckpt_file_name, filter_prefix="conv1")
        >>> param_not_load, _ = ms.load_param_into_net(net, param_dict)
        >>> print(param_not_load)
        ['conv1.weight']

    Tutorial Examples:
        - `Saving and Loading the Model - Saving and Loading the Model Weight
          <https://mindspore.cn/tutorials/en/master/beginner/save_load.html#saving-and-loading-the-model-weight>`_
    """
    _check_load_param_into_net(net, parameter_dict)
    for key, value in parameter_dict.items():
        if not isinstance(key, str) or not isinstance(value, (Parameter, str, list)):
            logger.critical("Load parameters into net failed.")
            msg = ("For 'parameter_dict', the element in the argument 'parameter_dict' should be a "
                   "'str' and 'Parameter' , but got {} and {}.".format(type(key), type(value)))
            raise TypeError(msg)

    strict_load = Validator.check_bool(strict_load)
    remove_redundancy = Validator.check_isinstance('remove_redundancy', remove_redundancy, bool)
    logger.info("Execute the process of loading parameters into net.")
    param_not_load = []
    ckpt_not_load = list(parameter_dict.keys())
    for _, param in net.parameters_and_names():
        if param.name in parameter_dict:
            if isinstance(param, MapParameter):
                param.import_data(parameter_dict[param.name])
                continue
            # Add has attr protection when load server checkpoint file on worker.
            if not hasattr(parameter_dict[param.name], "data"):
                continue
            new_param = parameter_dict[param.name]
            _update_param(param, new_param, strict_load)
            if hasattr(param, "init_param") and not param.init_param:
                param.init_param = True
            ckpt_not_load.remove(param.name)
        else:
            param_not_load.append(param.name)

    if param_not_load and not strict_load:
        _load_dismatch_prefix_params(net, parameter_dict, param_not_load, strict_load)

    logger.info("Loading parameters into net is finished.")
    if param_not_load:
        logger.warning("For 'load_param_into_net', "
                       "{} parameters in the 'net' are not loaded, because they are not in the "
                       "'parameter_dict', please check whether the network structure is consistent "
                       "when training and loading checkpoint. Another possibility is that "
                       "the redundant loading is not enabled, but the loaded checkpoint is saved with "
                       "redundancy removed. ".format(len(param_not_load)))
        logger.warning("{} are not loaded.".format(param_not_load))
    if remove_redundancy:
        parallel_mode = context.get_auto_parallel_context("parallel_mode")
        if parallel_mode == "stand_alone":
            raise TypeError(f"The deduplication feature for loading checkpoint can only be used "
                            f"in parallel scenarios, but got {parallel_mode}.")
        if not net.compile_cache and not net.parameter_layout_dict:
            raise ValueError("When loading a parameter dict that has removed redundancy, "
                             "the network should be compiled.")
        param_layout = net.parameter_layout_dict
        rank_id = get_rank()
        device_num = _get_device_num()
        stage_num = _get_auto_parallel_context("pipeline_stages")
        chunk_size = device_num // stage_num
        initial_rank = (rank_id // chunk_size) * chunk_size
        _single_parameter_broadcast(net, param_layout, rank_id, initial_rank)

    return param_not_load, ckpt_not_load


def _warm_up_host_cache_enabled(parameter_dict):
    """Warm up host cache enabled."""
    if _cache_enable():
        return True
    for key in parameter_dict.keys():
        if key.find(".__param_key__") != -1:
            return True
    return False


def _warm_up_host_cache(parameter_dict, net):
    """Warm up host cache."""
    ms_role = os.getenv("MS_ROLE")
    is_worker = ms_role == "MS_WORKER"
    param_key_dict = {}
    # Traverse key, value in parameter_dict, warm up param key and record param key into param_key_dict.
    if is_worker:
        net.init_parameters_data()
        net_dict = {}
        for name, value in net.parameters_and_names():
            net_dict[name] = value
        for param_name, value in parameter_dict.items():
            pos = param_name.find(".__param_key__")
            if pos != -1:
                net_param_name = param_name[:pos]
                param_key_dict[param_name] = net_param_name
                net_value = None
                if net_param_name not in net_dict:
                    logger.warning("net param name : %s is not in net", net_param_name)
                else:
                    net_value = net_dict.get(net_param_name, None)
                pos += len(".__param_key__")
                param_key = int(param_name[pos:])
                value_is_map_parameter = isinstance(value, list) and len(value) == 3
                if value_is_map_parameter and (net_value is None or isinstance(net_value, Parameter)):
                    key_tensor = Tensor.from_numpy(value[0])
                    value_tensor = Tensor.from_numpy(value[1])
                    status_tensor = Tensor.from_numpy(value[2])
                    _store_warm_up_ptr_by_tensor_list(param_key, key_tensor, value_tensor, status_tensor)
                elif not isinstance(value, list) and isinstance(net_value, Parameter):
                    _store_warm_up_ptr_by_tensor(param_key, value)
                else:
                    logger.warning("Unknown matches parameter type %s and net_value %s", type(value), type(net_value))
    else:
        for param_name, value in parameter_dict.items():
            pos = param_name.find(".__param_key__")
            if pos != -1:
                net_param_name = param_name[:pos]
                param_key_dict[param_name] = net_param_name
    # Split param key from parameter_dict since worker cannot load param key.
    warm_up_dict = {}
    for key, value in param_key_dict.items():
        if is_worker:
            warm_up_dict[value] = parameter_dict.pop(key)
        else:
            parameter_dict[value] = parameter_dict.pop(key)
    return (is_worker, parameter_dict, warm_up_dict)


def _warm_up_host_cache_post_process(is_worker, net_dict, warm_up_dict):
    """Warm up host cache post process."""
    if is_worker:
        net_dict.update(warm_up_dict)
    _set_checkpoint_load_status(True)


def _load_dismatch_prefix_params(net, parameter_dict, param_not_load, strict_load):
    """When some net parameter did not load, try to continue loading."""
    prefix_name = ""
    longest_name = param_not_load[0]
    while prefix_name != longest_name and param_not_load:
        logger.debug("Count: {} parameters has not been loaded, try to continue loading.".format(len(param_not_load)))
        prefix_name = longest_name
        for net_param_name in param_not_load:
            for dict_name in parameter_dict:
                if dict_name.endswith(net_param_name):
                    prefix_name = dict_name[:-len(net_param_name)]
                    break
            if prefix_name != longest_name:
                break

        if prefix_name != longest_name:
            logger.warning(f"For 'load_param_into_net', remove parameter prefix name: {prefix_name},"
                           f" continue to load.")
            for _, param in net.parameters_and_names():
                new_param_name = prefix_name + param.name
                if param.name in param_not_load and new_param_name in parameter_dict:
                    new_param = parameter_dict[new_param_name]
                    _update_param(param, new_param, strict_load)
                    if hasattr(param, "init_param") and not param.init_param:
                        param.init_param = True
                    param_not_load.remove(param.name)


def _save_graph(network, file_name):
    """
    Saves the graph of network to a file.

    Args:
        network (Cell): Obtain a pipeline through network for saving graph.
        file_name (str): Graph file name into which the graph will be saved.
    """
    logger.info("Execute the process of saving graph.")

    file_name = os.path.realpath(file_name)
    graph_pb = network.get_func_graph_proto()
    if graph_pb:
        with open(file_name, "wb") as f:
            os.chmod(file_name, stat.S_IRUSR | stat.S_IWUSR)
            f.write(graph_pb)


def _reshape_tensor(tensor, dst_shape):
    """reshape tensor to dst shape"""
    np_tensor = tensor.asnumpy()
    np_tensor = np_tensor.reshape(dst_shape)
    return Tensor(np_tensor, tensor.dtype)


def _check_param_for_integrate_save(pipeline_stages, uniform_split):
    """check whether current settings and parameters are supported in integrated save checkpoint mode"""
    if pipeline_stages > 1:
        raise RuntimeError("Pipeline Parallel don't support Integrated save checkpoint now.")
    if uniform_split == 0:
        raise RuntimeError("For 'save_checkpoint' and in automatic model parallel scene, when set "
                           "'integrated_save' to True, the checkpoint will be integrated save, it "
                           "is only supports uniform split tensor now.")


def _get_merged_param_data(net, parameter_layout_dict, param_name, param_data, integrated_save):
    """
    Gets the merged data(tensor) from tensor slice, by device arrangement and tensor map.

    Args:
        net (Cell): MindSpore network.
        param_name (str): The parameter name, which to be combined.
        param_data (Tensor): The parameter data on the local device, which was a slice of the whole parameter data.
        integrated_save (bool): Whether to integrated save in automatic model parallel scene.
    Returns:
        Tensor, the combined tensor which with the whole data value.
    """
    layout = parameter_layout_dict[param_name]
    if len(layout) < 8:
        logger.info("The layout dict does not contain the key %s", param_name)
        return param_data

    dev_mat = layout[0]
    tensor_map = layout[1]
    uniform_split = layout[4]
    opt_shard_group = layout[5]
    before_reshape_slice_shape = layout[2]
    before_reshape_full_shape = layout[6]
    after_reshape_slice_shape = layout[7]
    do_reshape = False
    if before_reshape_full_shape and after_reshape_slice_shape \
            and after_reshape_slice_shape != before_reshape_slice_shape:
        do_reshape = True

    allgather_net = None
    mp_weight = False
    for dim in tensor_map:
        if dim != -1:
            mp_weight = True
            break
    if param_name in net.parallel_parameter_merge_net_dict:
        allgather_net = net.parallel_parameter_merge_net_dict[param_name]
    else:
        logger.info("Need to create allgather net for %s", param_name)
        if integrated_save:
            _check_param_for_integrate_save(context.get_auto_parallel_context("pipeline_stages"), uniform_split)
            # while any dim is not equal to -1, means param is split and needs to be merged
            # pipeline parallel need to be supported here later
            if mp_weight:
                allgather_net = get_allgather_cell(opt_shard_group, bool(opt_shard_group), do_reshape,
                                                   tuple(after_reshape_slice_shape))
                object.__setattr__(allgather_net, "keep_input_unchanged", True)
            elif opt_shard_group:
                allgather_net = get_allgather_cell(opt_shard_group, False, do_reshape,
                                                   tuple(after_reshape_slice_shape))
        elif opt_shard_group and context.get_auto_parallel_context("optimizer_weight_shard_aggregated_save"):
            allgather_net = get_allgather_cell(opt_shard_group, False, do_reshape,
                                               tuple(after_reshape_slice_shape))
        net.parallel_parameter_merge_net_dict[param_name] = allgather_net
    if allgather_net:
        param_data = allgather_net(param_data)
    if mp_weight and integrated_save:
        param_data = _reshape_param_data(param_data, dev_mat, tensor_map)
        if do_reshape:
            param_data = _reshape_tensor(param_data, before_reshape_full_shape)
    return param_data


def export(net, *inputs, file_name, file_format, **kwargs):
    """
    Export the MindSpore network into an offline model in the specified format.

    Note:
        1. When exporting AIR, ONNX format, the size of a single tensor can not exceed 2GB.
        2. When `file_name` does not have a suffix, the system will automatically add one
           according to the `file_format`.
        3. Exporting functions decorated with :func:`mindspore.jit` to mindir format is supported.
        4. When exporting a function decorated with :func:`mindspore.jit`, the function should not involve
           class properties in calculations.
        5. AIR format is deprecated, and will be removed in a future version, please use other format or use
           MindSpore Lite to do offline inference.

    Args:
        net (Union[Cell, function]): MindSpore network.
        inputs (Union[Tensor, Dataset, List, Tuple, Number, Bool]): It represents the inputs
             of the `net`, if the network has multiple inputs, set them together. While its type is Dataset,
             it represents the preprocess behavior of the `net`, data preprocess operations will be serialized.
             In second situation, you should adjust batch size of dataset script manually which will impact on
             the batch size of 'net' input. Only supports parse "image" column from dataset currently.
        file_name (str): File name of the model to be exported.
        file_format (str): MindSpore currently supports 'AIR', 'ONNX' and 'MINDIR' format for exported model.

            - AIR: Ascend Intermediate Representation. An intermediate representation format of Ascend model.
            - ONNX: Open Neural Network eXchange. An open format built to represent machine learning models.
            - MINDIR: MindSpore Native Intermediate Representation for Anf. An intermediate representation format
              for MindSpore models. MINDIR does not support operators which have dictionary attribute.

        kwargs (dict): Configuration options dictionary.

            - enc_key (byte): Byte-type key used for encryption. The valid length is 16, 24, or 32.
            - enc_mode (Union[str, function]): Specifies the encryption mode, to take effect when enc_key is set.

              - For 'AIR' and 'ONNX' models, only customized encryption is supported.
              - For 'MINDIR', all options are supported. Option: 'AES-GCM', 'AES-CBC', 'SM4-CBC'
                or Customized encryption.
                Default: ``'AES-GCM'``.
              - For details of using the customized encryption, please check the `tutorial
                <https://mindspore.cn/mindarmour/docs/en/master/model_encrypt_protection.html>`_.

            - dataset (Dataset): Specifies the preprocessing method of the dataset, which is used to import the
              preprocessing of the dataset into MindIR.

            - obf_config (dict): obfuscation config.

              - type (str): The type of obfuscation, only 'dynamic' is supported until now.
              - obf_ratio (float, str): The ratio of nodes in original model that would be obfuscated. `obf_ratio`
                should be in range of (0, 1] or in ["small", "medium", "large"]. "small", "medium" and "large" are
                correspond to 0.1, 0.3, and 0.6 respectively.
              - customized_func (function): A python function used for customized function mode, which used for control
                the switch branch of obfuscation structure. The outputs of customized_func should be boolean and const (
                Reference to 'my_func()' in
                `tutorials <https://www.mindspore.cn/mindarmour/docs/en/master/dynamic_obfuscation_protection.html>`_).
                This function needs to ensure that its result is constant for any input. Users can refer to opaque
                predicates. If customized_func is set, then it should be passed to `load()` interface when loading
                obfuscated model.
              - obf_random_seed (int): Obfuscation random seed, which should be in (0, 9223372036854775807]. The
                structure of obfuscated models corresponding to different random seeds is different. If
                `obf_random_seed` is set, then it should be passed
                to :class:`mindspore.nn.GraphCell` interface when loading
                obfuscated model. It should be noted that at least one of `customized_func` or `obf_random_seed` should
                be set, and the latter mode would be applied if both of them are set.

            - incremental (bool): export MindIR incrementally.

            - custom_func (function): Functions for custom defined export policies. This function will be used to
              customize the model during network export. Currently only support for files with mindir format. The
              function only accepts one input representing the proto object of the mindir file. When modifying a model,
              it is necessary to ensure the correctness of the `custom_func` , otherwise it may lead to model loading
              failure or functional errors. Default: ``None`` .

    Examples:
        >>> import mindspore as ms
        >>> import numpy as np
        >>> from mindspore import Tensor
        >>>
        >>> # Define the network structure of LeNet5. Refer to
        >>> # https://gitee.com/mindspore/docs/blob/master/docs/mindspore/code/lenet.py
        >>> net = LeNet5()
        >>> input_tensor = Tensor(np.ones([1, 1, 32, 32]).astype(np.float32))
        >>> ms.export(net, input_tensor, file_name='lenet', file_format='MINDIR')
        >>>
        >>> # Export model in MindIR format and modified the model info using custom_func
        >>> # The custom_func only support one input representing the Proto object of the model
        >>> # And custom_func does not support return value
        >>> def _custom_func(mindir_model):
        ...     mindir_model.producer_name = "test11111"
        ...     mindir_model.producer_version = "11.0"
        ...     mindir_model.user_info["version"] = "11.0"
        >>> ms.export(net, input_tensor, file_name="lenet", file_format='MINDIR', custom_func=_custom_func)


    Tutorial Examples:
        - `Saving and Loading the Model - Saving and Loading MindIR
          <https://mindspore.cn/tutorials/en/master/beginner/save_load.html#saving-and-loading-mindir>`_
    """
    old_ms_jit_value = context.get_context("jit_syntax_level")
    context.set_context(jit_syntax_level=mindspore.STRICT)

    supported_formats = ['AIR', 'ONNX', 'MINDIR']
    if file_format not in supported_formats:
        raise ValueError(f"For 'export', 'file_format' must be one of {supported_formats}, but got {file_format}.")
    if file_format == 'AIR':
        logger.warning("AIR format is deprecated, and will be removed in a future version, please use other format or "
                       "use MindSpore Lite to do offline inference")
    Validator.check_file_name_by_regular(file_name)
    logger.info("exporting model file:%s format:%s.", file_name, file_format)

    if check_input_dataset(*inputs, dataset_type=mindspore.dataset.Dataset):
        if len(inputs) != 1:
            raise RuntimeError(f"You can only serialize one dataset into MindIR, got " + str(len(inputs)) + " datasets")
        shapes, types, columns = inputs[0].output_shapes(), inputs[0].output_types(), inputs[0].get_col_names()
        kwargs['dataset'] = inputs[0]
        only_support_col = "image"

        inputs_col = list()
        for c, s, t in zip(columns, shapes, types):
            if only_support_col != c:
                continue
            inputs_col.append(Tensor(np.random.uniform(-1.0, 1.0, size=s).astype(t)))
        if not inputs_col:
            raise RuntimeError(f"Only supports parse \"image\" column from dataset now, given dataset has columns: "
                               + str(columns))
        inputs = tuple(inputs_col)

    file_name = os.path.realpath(file_name)
    if 'enc_key' in kwargs.keys():
        kwargs['enc_key'], kwargs['enc_mode'] = _check_key_mode_type(file_format, **kwargs)
    _export(net, file_name, file_format, *inputs, **kwargs)

    context.set_context(jit_syntax_level=old_ms_jit_value)


def _get_funcgraph(net, *inputs):
    """
    Compile the MindSpore network and get FuncGraph.

    Arg:
        net (Union[Cell, function]): MindSpore network.
        inputs (Union[Tensor, Dataset, List, Tuple, Number, Bool]): It represents the inputs
             of the `net`, if the network has multiple inputs, set them together. While its type is Dataset,
             it represents the preprocess behavior of the `net`, data preprocess operations will be serialized.
             In second situation, you should adjust batch size of dataset script manually which will impact on
             the batch size of 'net' input. Only supports parse "image" column from dataset currently.

    Returns:
        FuncGraph, a mindspore._c_expression.FuncGraph obj.

    Raises:
        ValueError: input `net` is not a nn.Cell.

    Examples:
        >>> import mindspore as ms
        >>> import numpy as np
        >>> from mindspore import Tensor
        >>>
        >>> # Define the network structure of LeNet5. Refer to
        >>> # https://gitee.com/mindspore/docs/blob/master/docs/mindspore/code/lenet.py
        >>> net = LeNet5()
        >>> input_tensor = Tensor(np.ones([1, 1, 32, 32]).astype(np.float32))
        >>> ms.get_funcgraph(net, input_tensor)

    """
    if not isinstance(net, nn.Cell):
        raise ValueError(f"For get_funcgraph's parameter 'net', currently only support Cell right now.")
    phase_name = "lite_infer_predict" if _is_in_auto_parallel_mode() else "lite_infer_get_func_graph"
    graph_id, _ = _executor.compile(net, *inputs, phase=phase_name, do_convert=False)
    # pylint: disable=protected-access
    func_graph = _executor._get_func_graph(net, graph_id)
    return func_graph


def _export(net, file_name, file_format, *inputs, **kwargs):
    """
    It is an internal conversion function. Export the MindSpore prediction model to a file in the specified format.
    """
    logger.info("exporting model file:%s format:%s.", file_name, file_format)
    if "obf_config" in kwargs and file_format != "MINDIR":
        raise ValueError(f"Dynamic obfuscation only support for MindIR format, but got {file_format} format.")
    if "custom_func" in kwargs and file_format != "MINDIR":
        raise ValueError(f"Currently only support custom_func for MindIR format, but got {file_format} format.")
    if file_format == 'AIR':
        _save_air(net, file_name, *inputs, **kwargs)
    elif file_format == 'ONNX':
        _save_onnx(net, file_name, *inputs, **kwargs)
    elif file_format == 'MINDIR':
        _save_mindir(net, file_name, *inputs, **kwargs)


def _check_key_mode_type(file_format, **kwargs):
    """check enc_key and enc_mode are valid"""
    enc_key = Validator.check_isinstance('enc_key', kwargs.get('enc_key'), bytes)
    enc_mode = kwargs.get('enc_mode')

    if callable(enc_mode):
        return enc_key, enc_mode

    enc_mode = 'AES-GCM'
    if 'enc_mode' in kwargs.keys():
        enc_mode = Validator.check_isinstance('enc_mode', kwargs.get('enc_mode'), str)

    if file_format in ('AIR', 'ONNX'):
        raise ValueError(f"AIR/ONNX only support customized encryption, but got {enc_mode}.")

    if enc_mode in ('AES-CBC', 'AES-GCM', 'SM4-CBC'):
        return enc_key, enc_mode
    raise ValueError(f"MindIR only support AES-GCM/AES-CBC/SM4-CBC encryption, but got {enc_mode}")


def _save_air(net, file_name, *inputs, **kwargs):
    """Save AIR format file."""
    phase_name = 'export.air'
    graph_id, _ = _executor.compile(net, *inputs, phase=phase_name)
    if not file_name.endswith('.air'):
        file_name += ".air"
    if os.path.exists(file_name):
        os.chmod(file_name, stat.S_IWUSR)
    if "/" in file_name:
        real_path = os.path.realpath(file_name[:file_name.rfind("/")])
        os.makedirs(real_path, mode=0o700, exist_ok=True)
    if 'enc_key' in kwargs.keys() and 'enc_mode' in kwargs.keys():
        _executor.export(file_name, graph_id, enc_key=kwargs.get('enc_key'), encrypt_func=kwargs.get('enc_mode'))
    else:
        _executor.export(file_name, graph_id)
    os.chmod(file_name, stat.S_IRUSR)


def _save_onnx(net, file_name, *inputs, **kwargs):
    """Save ONNX format file."""
    # When dumping ONNX file, switch network mode to infer when it is training(NOTE: ONNX only designed for prediction)
    if not isinstance(net, nn.Cell):
        raise ValueError(f"Export ONNX format model only support nn.Cell object, but got {type(net)}.")
    _check_dynamic_input(inputs)
    cell_mode = net.training
    net.set_train(mode=False)
    total_size = _calculation_net_size(net)
    if total_size > PROTO_LIMIT_SIZE:
        raise RuntimeError('Export onnx model failed. Network size is: {}G, it exceeded the protobuf: {}G limit.'
                           .format(total_size / 1024 / 1024, PROTO_LIMIT_SIZE / 1024 / 1024))
    phase_name = 'export.onnx'
    graph_id, _ = _executor.compile(net, *inputs, phase=phase_name, do_convert=False)
    onnx_stream = _executor._get_func_graph_proto(net, graph_id)
    if 'enc_key' in kwargs.keys() and 'enc_mode' in kwargs.keys():
        enc_mode = kwargs.get('enc_mode')
        onnx_stream = enc_mode(onnx_stream, kwargs.get('enc_key'))
    if not file_name.endswith('.onnx'):
        file_name += ".onnx"
    if os.path.exists(file_name):
        os.chmod(file_name, stat.S_IWUSR)
    with open(file_name, 'wb') as f:
        f.write(onnx_stream)
        os.chmod(file_name, stat.S_IRUSR)
    net.set_train(mode=cell_mode)


def _check_dynamic_input(inputs):
    for ele in inputs:
        if isinstance(ele, Tensor) and -1 in ele.shape:
            raise ValueError(f"Export ONNX format model not support dynamic shape mode.")


def _generate_front_info_for_param_data_file(is_encrypt, kwargs):
    front_info = bytes()
    check_code = sys.byteorder == "little"
    front_info += check_code.to_bytes(1, byteorder=sys.byteorder)
    front_info += bytes(63)
    if is_encrypt():
        front_info = _encrypt(front_info, len(front_info), kwargs.get('enc_key'),
                              len(kwargs.get('enc_key')), kwargs.get('enc_mode'))
    return front_info


def _change_file(f, dirname, external_local, is_encrypt, kwargs):
    """Change to another file to write parameter data."""
    # The parameter has been not written in the file
    front_info = _generate_front_info_for_param_data_file(is_encrypt, kwargs)
    f.seek(0, 0)
    f.write(front_info)
    f.close()
    ori_data_file_name = f.name
    os.chmod(ori_data_file_name, stat.S_IRUSR)
    if os.path.getsize(ori_data_file_name) == 64:
        raise RuntimeError("The parameter size is exceed 1T,cannot export to the file")
    data_file_name = os.path.join(dirname, external_local)
    return _get_data_file(is_encrypt, kwargs, data_file_name)


def _get_data_file(is_encrypt, kwargs, data_file_name):
    """Get Data File to write parameter data."""
    # Reserves 64 bytes as spare information such as check data
    offset = 64
    if os.path.exists(data_file_name):
        os.chmod(data_file_name, stat.S_IWUSR)

    place_holder_data = bytes(offset)
    if is_encrypt():
        place_holder_data = _encrypt(place_holder_data, len(place_holder_data), kwargs["enc_key"],
                                     len(kwargs["enc_key"]), kwargs["enc_mode"])
    parameter_size = (offset / 1024)
    try:
        f = open(data_file_name, "wb")
        f.write(place_holder_data)
    except IOError:
        f.close()

    return f, parameter_size, offset


def _encrypt_data(is_encrypt, write_data, kwargs):
    """Encrypt parameter data."""
    if is_encrypt():
        if callable(kwargs.get('enc_mode')):
            enc_func = kwargs.get('enc_mode')
            write_data = enc_func(write_data, kwargs.get('enc_key'))
        else:
            write_data = _encrypt(write_data, len(write_data), kwargs.get('enc_key'),
                                  len(kwargs.get('enc_key')), kwargs.get('enc_mode'))
    return write_data


def _split_save(net_dict, model, file_name, is_encrypt, **kwargs):
    """The function to save parameter data."""
    logger.warning("Parameters in the net capacity exceeds 1G, save MindIR model and parameters separately.")
    # save parameter
    if model.graph.map_parameter:
        raise ValueError("MapParameter not support save in split MindIR file now.")
    file_prefix = file_name.split("/")[-1]
    if file_prefix.endswith(".mindir"):
        file_prefix = file_prefix[:-7]
    current_path = os.path.realpath(file_name)
    dirname = os.path.dirname(current_path)
    data_path = os.path.join(dirname, file_prefix + "_variables")
    if os.path.exists(data_path):
        shutil.rmtree(data_path)
    os.makedirs(data_path, mode=0o700, exist_ok=True)
    os.chmod(data_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    index = 0
    external_local = os.path.join(file_prefix + "_variables", "data_" + str(index))
    data_file_name = os.path.join(dirname, external_local)
    f, parameter_size, offset = _get_data_file(is_encrypt, kwargs, data_file_name)
    try:
        round = 0
        names = []
        for param_proto in model.graph.parameter:
            name = param_proto.name[param_proto.name.find(":") + 1:]
            names.append((name, param_proto))
            names.sort(key=lambda x: x[0])
        for pairs in names:
            name = pairs[0]
            param_proto = pairs[1]
            param = net_dict[name]
            raw_data = param.data.get_bytes()
            data_length = len(raw_data)
            append_size = 0
            if data_length % 64 != 0:
                append_size = 64 - (data_length % 64)
                parameter_size += ((append_size + data_length) / 1024)
            if parameter_size > PARAMETER_SPLIT_SIZE:
                index += 1
                external_local = os.path.join(file_prefix + "_variables", "data_" + str(index))
                f, parameter_size, offset = _change_file(f, dirname, external_local, is_encrypt, kwargs)
                parameter_size += ((append_size + data_length) / 1024)
            param_proto.external_data.location = external_local
            param_proto.external_data.length = data_length
            param_proto.external_data.offset = offset
            write_data = raw_data + bytes(append_size)
            offset += (data_length + append_size)
            write_data = _encrypt_data(is_encrypt, write_data, kwargs)
            f.write(write_data)
            round += 1
            logger.debug(f"writing {round}th split data, name:{name}")

        graph_file_name = os.path.join(dirname, file_prefix + "_graph.mindir")
        if os.path.exists(graph_file_name):
            os.chmod(graph_file_name, stat.S_IWUSR)
        with open(graph_file_name, 'wb') as model_file:
            os.chmod(graph_file_name, stat.S_IRUSR | stat.S_IWUSR)
            model_string = model.SerializeToString()
            if is_encrypt():
                model_string = _encrypt(model_string, len(model_string), kwargs.get('enc_key'),
                                        len(kwargs.get('enc_key')), kwargs.get('enc_mode'))
            model_file.write(model_string)
            os.chmod(graph_file_name, stat.S_IRUSR)

        front_info = _generate_front_info_for_param_data_file(is_encrypt, kwargs)
        f.seek(0, 0)
        f.write(front_info)
    finally:
        f.close()
        os.chmod(data_file_name, stat.S_IRUSR)


def _msfunc_info(net, *inputs):
    """Get mindir stream and parameter dict of ms_function"""
    # pylint: disable=protected-access
    net_dict = OrderedDict()
    _ms_func_executor = _MindsporeFunctionExecutor(net, time.time() * 1e9)
    graph_id = _ms_func_executor.compile(net.__name__, *inputs)
    mindir_stream = _executor._get_func_graph_proto(net, graph_id, 'mind_ir')
    params = _ms_func_executor._graph_executor.get_params(graph_id)
    for name, value in params.items():
        net_dict[name] = Parameter(value, name=name)
    return mindir_stream, net_dict


def _cell_info(net, incremental, *inputs):
    """Get mindir stream and net dict of cell"""
    phase_name = "export.mindir"
    graph_id, _ = _executor.compile(net, *inputs, phase=phase_name, do_convert=False)
    # pylint: disable=protected-access
    mindir_stream = _executor._get_func_graph_proto(net, graph_id, 'mind_ir', incremental=incremental)
    # clean obfuscation config to prevent the next call
    _executor.obfuscate_config = None

    net_dict = net.parameters_dict()
    return mindir_stream, net_dict


def _set_obfuscate_config(**kwargs):
    """Set obfuscation config for executor."""
    logger.warning("Obfuscate model.")
    if 'enc_mode' in kwargs.keys():
        enc_mode = Validator.check_isinstance('enc_mode', kwargs.get('enc_mode'), str)
        if enc_mode not in ["AES-GCM", "AES-CBC", "SM4-CBC"]:
            raise ValueError(
                "Only MindIR files that encrypted with 'AES-GCM', 'AES-CBC' or 'SM4-CBC' is supported for"
                "obfuscation, but got {}.".format(enc_mode))
    obf_ratio, customized_funcs, obf_random_seed = _check_obfuscate_params(kwargs.get('obf_config'))
    if customized_funcs and obf_random_seed > 0:
        logger.warning("Although 'customized_func' and 'obf_random_seed' are set, the 'obf_random_seed' mode would be"
                       " applied, remember to set 'obf_random_seed' when loading obfuscated model.")

    if obf_random_seed == 0:  # apply customized_func mode
        device_target = context.get_context('device_target')
        if device_target in ["GPU", "Ascend"]:
            raise ValueError(
                "Customized func mode only support 'device_target'='CPU, but got {}.".format(device_target))
        clean_funcs()
        for func in customized_funcs:
            add_opaque_predicate(func.__name__, func)
    _executor.obfuscate_config = {'obf_ratio': obf_ratio, 'obf_random_seed': obf_random_seed}


def _save_mindir(net, file_name, *inputs, **kwargs):
    """Save MindIR format file."""
    # set obfuscate configs
    if 'obf_config' in kwargs.keys():
        _set_obfuscate_config(**kwargs)
        for item in inputs:
            if -1 in item.shape:
                raise ValueError(
                    "Dynamic shape input is not supported now, but got the shape of inputs: {}.".format(item.shape))

    incremental = kwargs.get('incremental', False)

    model = mindir_model()
    if not isinstance(net, nn.Cell):
        mindir_stream, net_dict = _msfunc_info(net, *inputs)
    else:
        mindir_stream, net_dict = _cell_info(net, incremental, *inputs)
    model.ParseFromString(mindir_stream)

    if kwargs.get('dataset'):
        check_input_data(kwargs.get('dataset'), data_class=mindspore.dataset.Dataset)
        dataset = kwargs.get('dataset')
        _save_dataset_to_mindir(model, dataset)

    custom_func = kwargs.get('custom_func', None)
    if custom_func is not None:
        custom_func(model)

    save_together = _save_together(net_dict, model)
    is_encrypt = lambda: 'enc_key' in kwargs.keys() and 'enc_mode' in kwargs.keys()
    if save_together:
        _save_mindir_together(net_dict, model, file_name, is_encrypt, **kwargs)
    else:
        _split_save(net_dict, model, file_name, is_encrypt, **kwargs)


def _save_mindir_together(net_dict, model, file_name, is_encrypt, **kwargs):
    """Save graph and parameter together."""
    for param_proto in model.graph.parameter:
        param_name = param_proto.name[param_proto.name.find(":") + 1:]
        if param_name in net_dict.keys():
            param_data = net_dict[param_name].data.get_bytes()
            param_proto.raw_data = param_data
        else:
            raise ValueError("The parameter '{}' is not belongs to any cell,"
                             "the data of parameter cannot be exported.".format(param_proto.name))
    incremental = kwargs.get('incremental', False)
    for map_param_proto in model.graph.map_parameter:
        map_param_name = map_param_proto.name[map_param_proto.name.find(":") + 1:]
        if map_param_name in net_dict.keys():
            map_parameter = net_dict[map_param_name]
            key_bytes, value_bytes, status_bytes = map_parameter.export_bytes(incremental)
            map_param_proto.key_tensor.raw_data = key_bytes
            map_param_proto.value_tensor.raw_data = value_bytes
            map_param_proto.status_tensor.raw_data = status_bytes
        else:
            raise ValueError("The map_parameter '{}' is not belongs to any cell,"
                             "the data of parameter cannot be exported.".format(map_param_proto.name))
    if not file_name.endswith('.mindir'):
        file_name += ".mindir"
    current_path = os.path.realpath(file_name)
    dirname = os.path.dirname(current_path)
    os.makedirs(dirname, mode=0o700, exist_ok=True)
    if os.path.exists(file_name):
        os.chmod(file_name, stat.S_IWUSR)
    with open(file_name, 'wb') as f:
        os.chmod(file_name, stat.S_IRUSR | stat.S_IWUSR)
        model_string = model.SerializeToString()
        if is_encrypt():
            if callable(kwargs.get('enc_mode')):
                enc_func = kwargs.get('enc_mode')
                model_string = enc_func(model_string, kwargs.get('enc_key'))
            else:
                model_string = _encrypt(model_string, len(model_string), kwargs.get('enc_key'),
                                        len(kwargs.get('enc_key')), kwargs.get('enc_mode'))
        f.write(model_string)
        os.chmod(file_name, stat.S_IRUSR)


def _save_together(net_dict, model):
    """Whether graph and parameter save together during save mindir model."""
    data_total = 0
    for param_proto in model.graph.parameter:
        name = param_proto.name[param_proto.name.find(":") + 1:]
        if name in net_dict.keys():
            data_total += sys.getsizeof(net_dict[name].data.get_bytes()) / 1024
        else:
            raise ValueError("The parameter '{}' is not belongs to any cell,"
                             "the data of parameter cannot be exported.".format(param_proto.name))
        if data_total > TOTAL_SAVE:
            return False
    return True


def _save_dataset_to_mindir(model, dataset):
    """Save dataset preprocess operations into mindir model."""
    dataset_json = dataset.to_json()
    reverse_dataset = []
    while dataset_json:
        reverse_dataset = [dataset_json] + reverse_dataset
        if len(dataset_json['children']) > 1:
            logger.warning("Need to support dataset_node with more than one child, using child 0 as default.")
        dataset_json = dataset_json['children'][0] if dataset_json['children'] else []

    for op in reverse_dataset:
        if op['op_type'] == 'Map':
            model.preprocessor.op.add()
            model.preprocessor.op[-1].input_columns = json.dumps(op['input_columns'])
            model.preprocessor.op[-1].output_columns = json.dumps(op['output_columns'])
            model.preprocessor.op[-1].op_type = json.dumps(op['op_type'])
            model.preprocessor.op[-1].operations = json.dumps(op['operations'])
            model.preprocessor.op[-1].offload = op['offload'] if 'offload' in op.keys() else False


def check_checkpoint(ckpt_file_name):
    """
    Check whether the checkpoint is valid.

    Args:
        ckpt_file_name (str): Checkpoint file name.

    Returns:
        bool, whether the checkpoint is valid.

    Examples:
        >>> import mindspore as ms
        >>> ckpt_file_name = "./checkpoint/LeNet5-1_32.ckpt"
        >>> check_result = ms.check_checkpoint(ckpt_file_name)
        >>> print(check_result)
        True
    """
    if not ckpt_file_name.endswith('.ckpt'):
        return False
    checkpoint_list = Checkpoint()
    with _ckpt_fs.open(ckpt_file_name, *_ckpt_fs.open_args) as f:
        pb_content = f.read()
        if pb_content[-17:-10] == b"crc_num":
            crc_num_bytes = pb_content[-10:]
            pb_content = pb_content[:-17]
            crc_num = int.from_bytes(crc_num_bytes, byteorder='big')
            cal_crc_num = binascii.crc32(pb_content, 0)
            if cal_crc_num != crc_num:
                logger.warning("For 'check_checkpoint', the ckpt crc check is failed.")
                return False
        try:
            checkpoint_list.ParseFromString(pb_content)
        except google.protobuf.message.DecodeError as e:
            logger.warning("For 'check_checkpoint', the ckpt parse is failed.")
            logger.warning(e)
            return False
        return True


def parse_print(print_file_name):
    """
    Parse data file generated by :class:`mindspore.ops.Print`.

    Args:
        print_file_name (str): The file name needs to be parsed.

    Returns:
        List, element of list is Tensor.

    Raises:
        ValueError: The print file does not exist or is empty.
        RuntimeError: Failed to parse the file.

    Examples:
        >>> import numpy as np
        >>> import mindspore as ms
        >>> from mindspore import nn, Tensor, ops
        >>> ms.set_context(mode=ms.GRAPH_MODE, print_file_path='log.data')
        >>> class PrintInputTensor(nn.Cell):
        ...         def __init__(self):
        ...             super().__init__()
        ...             self.print = ops.Print()
        ...
        ...         def construct(self, input_pra):
        ...             self.print('print:', input_pra)
        ...             return input_pra
        >>> x = np.array([[1, 2, 3, 4], [5, 6, 7, 8]]).astype(np.float32)
        >>> input_pra = Tensor(x)
        >>> net = PrintInputTensor()
        >>> net(input_pra)
        >>>
        >>> data = ms.parse_print('./log.data')
        >>> print(data)
        ['print:', Tensor(shape=[2, 4], dtype=Float32, value=
        [[ 1.00000000e+00,  2.00000000e+00,  3.00000000e+00,  4.00000000e+00],
        [ 5.00000000e+00,  6.00000000e+00,  7.00000000e+00,  8.00000000e+00]])]
    """
    print_file_path = os.path.realpath(print_file_name)

    if os.path.getsize(print_file_path) == 0:
        raise ValueError("For 'parse_print', the print file may be empty, please make sure enter the correct "
                         "'print_file_name'.")

    logger.info("Execute load print process.")
    print_list = Print()

    try:
        with open(print_file_path, "rb") as f:
            pb_content = f.read()
        print_list.ParseFromString(pb_content)
    except BaseException as e:
        logger.critical("Failed to read the print file %s, please check whether the file is "
                        "correct.", print_file_name)
        raise ValueError(e.__str__() + "\nFailed to read the print file {}, please check whether "
                                       "the file is correct.".format(print_file_name)) from e

    tensor_list = []

    try:
        for print_ in print_list.value:
            # String type
            if print_.HasField("desc"):
                tensor_list.append(print_.desc)
            elif print_.HasField("tensor"):
                dims = print_.tensor.dims
                data_type = print_.tensor.tensor_type
                data = print_.tensor.tensor_content
                np_type = tensor_to_np_type.get(data_type)
                param_data = np.fromstring(data, np_type)
                ms_type = tensor_to_ms_type.get(data_type)
                if dims and dims != [0]:
                    param_value = param_data.reshape(dims)
                    tensor_list.append(Tensor(param_value, ms_type))
                # Scalar type
                else:
                    data_type_ = data_type.lower()
                    if 'float' in data_type_:
                        param_data = float(param_data[0])
                    elif 'int' in data_type_:
                        param_data = int(param_data[0])
                    elif 'bool' in data_type_:
                        param_data = bool(param_data[0])
                    tensor_list.append(Tensor(param_data, ms_type))

    except BaseException as e:
        logger.critical("Failed to load the print file %s.", print_list)
        raise RuntimeError(e.__str__() + "\nFailed to load the print file {}.".format(print_list)) from e

    return tensor_list


def _merge_param_with_strategy(sliced_data, parameter_name, strategy, is_even):
    """
    Merge data slices to one tensor with whole data when strategy is not None.

    Args:
        sliced_data (list[numpy.ndarray]): Data slices in order of rank_id.
        parameter_name (str): Name of parameter.
        strategy (dict): Parameter slice strategy.
        is_even (bool): Slice manner that True represents slicing evenly and False represents slicing unevenly.

    Returns:
        Tensor, the merged Tensor which has the whole data.

    Raises:
        ValueError: Failed to merge.
    """
    layout = strategy.get(parameter_name)
    try:
        dev_mat = list(layout.dev_matrix[0].dim)
        tensor_map = list(layout.tensor_map[0].dim)
        param_split_shape = list(layout.param_split_shape[0].dim)
        field_size = int(layout.field)
    except BaseException as e:
        raise ValueError(f"{e.__str__()}. For 'merge_sliced_parameter'"
                         f", please make sure that 'strategy' is correct.") from e

    device_count = 1
    for dim in dev_mat:
        device_count *= dim

    if len(sliced_data) != device_count:
        raise ValueError(f"For 'merge_sliced_parameter', the length of 'sliced_parameters' should be equal to "
                         f"device_count. The length of 'sliced_parameters' is {len(sliced_data)}, but "
                         f"device_count is {device_count}.")

    if not param_split_shape:
        if not is_even:
            raise ValueError("For 'merge_sliced_parameter', the shape of every parameter in 'sliced_parameters' "
                             "should be the same when slice manner is even.")

        all_gather_tensor = Tensor(np.concatenate(sliced_data))

        if field_size > 0:
            merged_tensor = _reshape_param_data_with_weight(all_gather_tensor, dev_mat, field_size)
        else:
            merged_tensor = _reshape_param_data(all_gather_tensor, dev_mat, tensor_map)

    else:
        tensor_strategy = _get_tensor_strategy(dev_mat, tensor_map)

        slice_count = 1
        for dim in tensor_strategy:
            slice_count *= dim

        if len(param_split_shape) != slice_count:
            raise ValueError(f"For 'merge_sliced_parameter', the param_split_shape length in 'strategy' should be "
                             f"{slice_count}, but got {len(param_split_shape)}.")

        tensor_slices_new = list(range(slice_count))
        tensor_slices = sliced_data
        for i in range(device_count):
            slice_index = int(_get_tensor_slice_index(dev_mat, tensor_strategy, tensor_map, i))
            if tensor_slices[i].shape[0] != param_split_shape[slice_index]:
                raise ValueError(f"For 'merge_sliced_parameter', the slice {slice_index} should be "
                                 f"{param_split_shape[slice_index]} in 0 axis, but got "
                                 f"{tensor_slices[i].shape[0]}.")
            tensor_slices_new[slice_index] = np.array(tensor_slices[i])

        dim_len = len(tensor_strategy)
        for i in range(dim_len):
            ele_count = int(len(tensor_slices_new) / tensor_strategy[dim_len - 1 - i])
            tensor_slices_new_inner = []
            for j in range(ele_count):
                new_tensor = tensor_slices_new[j * tensor_strategy[dim_len - 1 - i]]
                for k in range(j * tensor_strategy[dim_len - 1 - i] + 1,
                               (j + 1) * tensor_strategy[dim_len - 1 - i]):
                    new_tensor = np.concatenate((new_tensor, tensor_slices_new[k]), axis=dim_len - 1 - i)
                tensor_slices_new_inner.insert(len(tensor_slices_new_inner), np.array(new_tensor))
            tensor_slices_new = tensor_slices_new_inner
        merged_tensor = Tensor(tensor_slices_new[0])

    return merged_tensor


def restore_group_info_list(group_info_file_name):
    """
    Build rank list, the checkpoint of ranks in the rank list has the same contents with the local rank
    who saves the `group_info_file_name`. To save the group info file, please export GROUP_INFO_FIL
    environment variables like "export GROUP_INFO_FILE=/data/group_info.pb".

    Args:
        group_info_file_name (str): Name of group information file.

    Returns:
        List, the rank list.

    Raises:
        ValueError: group information file is incorrect.
        TypeError: `group_info_file_name` is not str.

    Examples:
        >>> import mindspore as ms
        >>> ms.restore_list = restore_group_info_list("./group_info.pb")
    """
    if not isinstance(group_info_file_name, str):
        raise TypeError(f"For 'restore_group_info_list', the argument 'group_info_file_name' should be str, "
                        f"but got {type(group_info_file_name)}.")

    if not os.path.isfile(group_info_file_name):
        raise ValueError(f"For 'restore_group_info_list', no such group information file: {group_info_file_name}.")

    if os.path.getsize(group_info_file_name) == 0:
        raise ValueError("For 'restore_group_info_list', the group information file should not be empty.")

    return _restore_group_info_list(group_info_file_name)


def build_searched_strategy(strategy_filename):
    """
    Build strategy of every parameter in network. Used in the case of distributed inference.

    Args:
        strategy_filename (str): Name of strategy file.

    Returns:
        Dict, whose key is parameter name and value is slice strategy of this parameter.

    Raises:
        ValueError: Strategy file is incorrect.
        TypeError: `strategy_filename` is not a string.

    Examples:
        >>> import mindspore as ms
        >>> strategy = ms.build_searched_strategy("./strategy_train.ckpt")
    """
    return _build_searched_strategy(strategy_filename)


def merge_sliced_parameter(sliced_parameters, strategy=None):
    """
    Merge parameter slices into one parameter. Used in the case of distributed inference.

    Args:
        sliced_parameters (list[Parameter]): Parameter slices in order of rank id.
        strategy (Optional[dict]): Parameter slice strategy, whose key is parameter name and
            value is slice strategy of this parameter. If strategy is None, just merge
            parameter slices in 0 axis order. Default: ``None``.

    Returns:
        Parameter, the merged parameter which has the whole data.

    Raises:
        ValueError: Failed to merge.
        TypeError: The sliced_parameters is incorrect or strategy is not dict.
        KeyError: The parameter name is not in keys of strategy.

    Examples:
        >>> import numpy as np
        >>> import mindspore as ms
        >>> from mindspore import Tensor, Parameter
        >>>
        >>> sliced_parameters = [
        ...                      Parameter(Tensor(np.array([0.00023915, 0.00013939, -0.00098059])),
        ...                                "network.embedding_table"),
        ...                      Parameter(Tensor(np.array([0.00015815, 0.00015458, -0.00012125])),
        ...                                "network.embedding_table"),
        ...                      Parameter(Tensor(np.array([0.00042165, 0.00029692, -0.00007941])),
        ...                                "network.embedding_table"),
        ...                      Parameter(Tensor(np.array([0.00084451, 0.00089960, -0.00010431])),
        ...                                "network.embedding_table")]
        >>> merged_parameter = ms.merge_sliced_parameter(sliced_parameters)
        >>> print(merged_parameter)
        Parameter (name=network.embedding_table, shape=(12,), dtype=Float64, requires_grad=True)
    """
    if not isinstance(sliced_parameters, list):
        raise TypeError(f"For 'merge_sliced_parameter', the argument 'sliced_parameters' should be list, "
                        f"but got {type(sliced_parameters)}.")

    if not sliced_parameters:
        raise ValueError("For 'merge_sliced_parameter', the argument 'sliced_parameters' should not be empty.")

    if strategy and not isinstance(strategy, dict):
        raise TypeError(f"For 'merge_sliced_parameter', the argument 'strategy' should be dict, "
                        f"but got {type(strategy)}.")

    try:
        parameter_name = sliced_parameters[0].name
        parameter_shape = sliced_parameters[0].data.shape
        parameter_shape_length = len(parameter_shape)
    except BaseException as e:
        raise TypeError(e.__str__() + f" For 'merge_sliced_parameter', the element in 'sliced_parameters' should be "
                                      f"'Parameter', but got {type(sliced_parameters[0])} at index 0.") from e

    is_even = True
    for index, parameter in enumerate(sliced_parameters):
        if not isinstance(parameter, Parameter):
            raise TypeError(f"For 'merge_sliced_parameter', the element in 'sliced_parameters' should be 'Parameter', "
                            f"but got {type(parameter)} at index {index}.")

        if parameter.name != parameter_name \
                or len(parameter.data.shape) != parameter_shape_length \
                or parameter.data.shape[1:] != parameter_shape[1:]:
            raise ValueError(f"For 'merge_sliced_parameter', please make sure that the elements in 'slice_parameters'"
                             f" have the same name, dimension length and shape except 0 axis. The name, dimension "
                             f"length, shape except 0 axis should be {parameter_name}, {parameter_shape_length}, "
                             f"{parameter_shape[1:]}, but got name: {parameter.name}, dimension length: "
                             f"{len(parameter.data.shape)}, shape except 0 axis: {parameter.data.shape[1:]} "
                             f"at index {index}.")

        if parameter.data.shape != parameter_shape:
            is_even = False

    layerwise_parallel = sliced_parameters[0].layerwise_parallel
    requires_grad = sliced_parameters[0].requires_grad
    sliced_data = []
    for parameter in sliced_parameters:
        if parameter.data.dtype == mstype.bfloat16:
            sliced_data.append(cpu_cast(parameter.data, mstype.float32).asnumpy())
        else:
            sliced_data.append(parameter.data.asnumpy())

    if not strategy:
        merged_tensor = Tensor(np.concatenate(sliced_data))
        merged_parameter = Parameter(merged_tensor, parameter_name, requires_grad, layerwise_parallel)

    else:
        if parameter_name not in strategy.keys():
            raise KeyError(f"For 'merge_sliced_parameter', the parameter name {parameter_name} should be a key in "
                           f"the 'strategy'. Please check 'sliced_parameter' and 'strategy'.")
        merged_tensor = _merge_param_with_strategy(sliced_data, parameter_name, strategy, is_even)
        merged_parameter = Parameter(merged_tensor, parameter_name, requires_grad, layerwise_parallel)

    return merged_parameter


def _gather_tasks_load_dis(unified_safetensors_dir, predict_strategy, network, dst_safetensors_dir, dst_device_num,
                           output_format, name_map):
    """gather transform tasks"""
    tasks = []
    for rank in range(0, dst_device_num):
        tasks.append(
            (unified_safetensors_dir, predict_strategy, network, dst_safetensors_dir, rank, output_format, name_map))
    return tasks


def load_distributed_checkpoint(network, checkpoint_filenames=None, predict_strategy=None,
                                train_strategy_filename=None, strict_load=False, dec_key=None, dec_mode='AES-GCM',
                                format='ckpt', unified_safetensors_dir=None, dst_safetensors_dir=None, rank_id=None,
                                output_format='safetensors', name_map=None, max_process_num=64):
    """
    Load checkpoint into net for distributed predication. Used in the case of distributed inference.

    Note:
        `output_format` will only take effect when `format` is set to `safetensors` and `network` is set to `None`.

    Args:
        network (Cell): Network for distributed predication, When the format is `safetensors`, the network parameter
                        can be left blank or passed as None, and the interface will execute save mode.
        checkpoint_filenames (list[str]): The name of Checkpoint files in order of rank id. Default: ``None`` .
        predict_strategy (Union[dict, str]): Strategy of predication process. It means that using one device to predict
                                 when setting predict_strategy as None. Default: ``None`` .
        train_strategy_filename (str): The filename of training strategy protocol buffer file.
                                       When train_strategy_filename is None, the training strategy file will be
                                       obtained from context.get_auto_parallel_context("strategy_ckpt_load_file").
                                       Therefore, the training strategy file needs to be specified
                                       in at least one of them. Default: ``None`` .
        strict_load (bool): Whether to strict load the parameter into net. If ``False`` , it will load parameter
                            into net when parameter name's suffix in checkpoint file is the same as the
                            parameter in the network. When the types are inconsistent, perform type conversion
                            on the parameters of the same type, such as float32 to float16. Default: ``False`` .
        dec_key (Union[None, bytes]): Byte type key used for decryption. If the value is ``None`` , the decryption
                                      is not required. Default: ``None`` .
        dec_mode (str): This parameter is valid only when dec_key is not set to ``None`` . Specifies the decryption
                        mode, currently supports ``'AES-GCM'`` , ``'AES-CBC'``  and ``'SM4-CBC'`` .
                        Default: ``'AES-GCM'`` .
        format (str): Input weight format to be loaded into the network.
                      It can be set to either "ckpt" or "safetensors". Default: "ckpt".
        unified_safetensors_dir (str): Directory of input weight files to be loaded into the network.
                                       Default: ``None`` .
        dst_safetensors_dir (str): In the save mode scenario, the save directory for weights.
        rank_id (int): The logical sequence number of the card. In non save mode, it is automatically obtained
                       globally by initializing the network; In save mode, save the file according to the input
                       sequence number. If it is not input, save the entire file.
        output_format (str, optional): Control the format of the output checkpoint after conversion.
            It can be set to either "ckpt" or "safetensors". Default: "safetensors".
        name_map (dict): The weight mapping dictionary will modify the weight names according to the mapping
            dictionary before loading or saving the segmented weights into the network. Default: None.
        max_process_num (int): Maximum number of processes. Default: 64.

    Raises:
        TypeError: The type of inputs do not match the requirements.
        ValueError: Failed to load checkpoint into net.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For the Ascend devices, users need to prepare the rank table, set rank_id and device_id.
            Please see the `rank table startup
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/rank_table.html>`_
            for more details.

            For the GPU devices, users need to prepare the host file and mpi, please see the `mpirun startup
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/mpirun.html>`_ .

            For the CPU device, users need to write a dynamic cluster startup script, please see the `Dynamic Cluster
            Startup <https://www.mindspore.cn/docs/en/master/model_train/parallel/dynamic_cluster.html>`_ .

        >>> import os
        >>> import numpy as np
        >>> import mindspore as ms
        >>> import mindspore.dataset as ds
        >>> from mindspore import nn, ops, train
        >>> from mindspore.communication import init
        >>>
        >>> step_per_epoch = 4
        >>> device_num = 8
        >>>
        >>> # Define the network structure.
        >>> class Net(nn.Cell):
        ...     def __init__(self, matmul_size, strategy=None):
        ...         super().__init__()
        ...         matmul_np = np.full(matmul_size, 0.5, dtype=np.float32)
        ...         self.matmul_weight = ms.Parameter(ms.Tensor(matmul_np))
        ...         self.matmul = ops.MatMul()
        ...         self.neg = ops.Neg()
        ...         if strategy is not None:
        ...             self.matmul.shard(strategy)
        ...
        ...     def construct(self, inputs):
        ...         x = self.matmul(inputs, self.matmul_weight)
        ...         x = self.neg(x)
        ...         return x
        >>>
        >>> # Create dataset.
        >>> def get_dataset(*inputs):
        ...     def generate():
        ...         for _ in range(step_per_epoch):
        ...             yield inputs
        ...     return generate
        >>>
        >>> # Train network and save distributed checkpoint.
        >>> def train_net():
        ...     ms.set_context(mode=ms.GRAPH_MODE)
        ...     init()
        ...     np.random.seed(1)
        ...     input_data = np.random.rand(16, 96).astype(np.float32)
        ...     label_data = np.random.rand(16, 16).astype(np.float32)
        ...     fake_dataset = get_dataset(input_data, label_data)
        ...     dataset = ds.GeneratorDataset(fake_dataset, ["input", "label"])
        ...
        ...     # Set parallel strategy.
        ...     strategy = ((1, 4), (4, 1))
        ...     ms.set_auto_parallel_context(parallel_mode=ms.ParallelMode.SEMI_AUTO_PARALLEL, device_num=device_num,
        ...                                  strategy_ckpt_save_file="./train_strategy.ckpt")
        ...     network = Net(matmul_size=(96, 16), strategy=strategy)
        ...     net_opt = nn.Momentum(network.trainable_params(), 0.01, 0.9)
        ...     net_loss = nn.SoftmaxCrossEntropyWithLogits(reduction="mean")
        ...     model = ms.Model(network=network, loss_fn=net_loss, optimizer=net_opt)
        ...     ckpt_config = train.CheckpointConfig(keep_checkpoint_max=1, integrated_save=False)
        ...     global_rank_id = int(os.getenv("RANK_ID"))
        ...     ckpt_path = "./rank_{}_ckpt".format(global_rank_id)
        ...     ckpt_callback = train.ModelCheckpoint(prefix="parallel", directory=ckpt_path, config=ckpt_config)
        ...     model.train(epoch=2, train_dataset=dataset, callbacks=[ckpt_callback], dataset_sink_mode=False)
        ...     ms.reset_auto_parallel_context()
        >>>
        >>> # Load distributed checkpoint and test.
        >>> def load_model():
        ...     ms.set_context(mode=ms.GRAPH_MODE)
        ...     init()
        ...     ms.set_auto_parallel_context(full_batch=True, parallel_mode="semi_auto_parallel",
        ...                                  strategy_ckpt_load_file="./train_strategy.ckpt", device_num=device_num)
        ...     predict_data = ms.Tensor(np.random.randn(128, 96).astype(np.float32))
        ...     network = Net(matmul_size=(96, 16))
        ...     model = ms.Model(network)
        ...     predict_layout = model.infer_predict_layout(ms.Tensor(predict_data))
        ...     ckpt_file_list = ["./rank_{}_ckpt/parallel-2_4.ckpt".format(i) for i in range(0, device_num)]
        ...     ms.load_distributed_checkpoint(network, ckpt_file_list, predict_layout)
        ...     predict_result = model.predict(predict_data)
        ...     print(predict_result)
        >>>
        >>> train_net()
        >>> load_model()
        [[-7.3259363 -7.497216  -7.398196  ... -7.374962  -7.204874  -7.234935 ]
        [ 3.362938   3.3535435  3.3832688 ...  3.4263954  3.279045   3.3202887]
        ...
        [ 1.6067538  1.6244187  1.5384722 ...  1.5449994  1.6195512  1.6176052]]
    """
    if format not in ['safetensors', 'ckpt'] or output_format not in ['safetensors', 'ckpt']:
        raise ValueError(
            f"For 'load_distributed_checkpoint', 'format' and 'output_format' "
            f"must be 'ckpt' or 'safetensors', but got {format}.")

    if format == 'safetensors':
        if unified_safetensors_dir is None:
            raise ValueError(f"For 'load_distributed_checkpoint', 'unified_safetensors_dir' can not be None "
                             f"when format is 'safetensors'.")
        unsupport_param = [checkpoint_filenames, train_strategy_filename, dec_key]
        for param in unsupport_param:
            if param is not None:
                raise ValueError(f"For 'load_distributed_checkpoint', {param} must be None "
                                 f"when format is 'safetensors'.")
        if strict_load or dec_mode != 'AES-GCM':
            raise ValueError(f"For 'load_distributed_checkpoint', strict_load and dec_mode must be default "
                             f"when format is 'safetensors'.")
        if network is not None:
            try:
                rank_id = get_rank()
            except RuntimeError:
                rank_id = 0
                logger.warning(f"Get rank failed, default loading weight for rank 0.")
            _load_parallel_checkpoint(
                (unified_safetensors_dir, predict_strategy, network, None, rank_id, output_format, name_map))
        else:
            if dst_safetensors_dir is None:
                raise ValueError(f"For 'load_distributed_checkpoint', 'dst_safetensors_dir' can not be None "
                                 f"when network is None.")
            if rank_id is not None:
                _load_parallel_checkpoint((unified_safetensors_dir, predict_strategy, network, dst_safetensors_dir,
                                           rank_id, output_format, name_map))
            else:
                dst_strategy_dict = _build_searched_strategy(predict_strategy)
                dst_stage_device_num = _get_device_num_from_strategy(dst_strategy_dict)
                dst_stage_num = _extract_pipeline_stage_num(dst_strategy_dict)
                dst_device_num = dst_stage_device_num * dst_stage_num
                tasks = _gather_tasks_load_dis(unified_safetensors_dir, predict_strategy, network, dst_safetensors_dir,
                                               dst_device_num, output_format, name_map)
                with Pool(processes=max_process_num) as pool:
                    list(pool.imap(_load_parallel_checkpoint, tasks))
        return

    network = Validator.check_isinstance("network", network, nn.Cell)
    _check_checkpoint_file(checkpoint_filenames)
    _check_predict_strategy(predict_strategy)

    dec_key = Validator.check_isinstance('dec_key', dec_key, (type(None), bytes))
    dec_mode = Validator.check_isinstance('dec_mode', dec_mode, str)

    if train_strategy_filename is None:
        train_strategy_filename = context.get_auto_parallel_context("strategy_ckpt_load_file")
    _train_strategy = build_searched_strategy(train_strategy_filename)
    train_strategy = _convert_to_list(_train_strategy)

    train_dev_count = 1
    ckpt_file_len = len(checkpoint_filenames)
    for dim in train_strategy[list(train_strategy.keys())[0]][0]:
        train_dev_count *= dim
    if train_dev_count != ckpt_file_len:
        raise ValueError(f"For 'Load_distributed_checkpoint', the length of 'checkpoint_filenames' should be "
                         f"equal to the device count of training process. "
                         f"But got the length of 'checkpoint_filenames'"
                         f" is {ckpt_file_len} and the device count is {train_dev_count}.")
    rank_list = _infer_rank_list(train_strategy, predict_strategy)

    param_total_dict = defaultdict(dict)
    for file_index, file_name in enumerate(checkpoint_filenames):
        ckpt_dict = load_checkpoint(file_name, dec_key=dec_key, dec_mode=dec_mode)
        for param_name, param in ckpt_dict.items():
            param_total_dict[param_name][file_index] = param

    param_dict = {}
    param_not_in_strategy = []
    param_not_in_ckpt = []
    for _, param in network.parameters_and_names():
        sliced_params = []
        if param.name not in rank_list.keys():
            param_not_in_strategy.append(param.name)
            continue
        if param.name not in param_total_dict:
            param_not_in_ckpt.append(param.name)
            continue

        param_rank = rank_list.get(param.name)[0]
        skip_merge_split = rank_list.get(param.name)[1]
        shard_stride = train_strategy.get(param.name)[4]
        tensor_map = train_strategy.get(param.name)[1]
        first_dim_shard_idx = tensor_map[0] if tensor_map else -1
        device_arrangement = train_strategy.get(param.name)[0]
        first_dim_shard_size = 1
        if first_dim_shard_idx >= 0:
            first_dim_shard_size = device_arrangement[-1 - first_dim_shard_idx]
        if train_strategy.get(param.name)[5]:
            shard_size = int(ckpt_file_len / shard_stride / train_strategy.get(param.name)[5] / first_dim_shard_size)
        else:
            shard_size = 0
        for rank in param_rank:
            param_total_list = list(range(0, ckpt_file_len))
            if first_dim_shard_size != 1:
                param_total_list = _get_param_list_when_first_dim_sharded(device_arrangement, first_dim_shard_idx, rank)
            if shard_size > 0:
                rank_index = param_total_list.index(rank)
                start = rank_index // shard_size * shard_size
                param_total_list = param_total_list[start:start + shard_size]
            if shard_stride > 0:
                param_stride = []
                # merge pre parameter
                param_index = param_total_list[0:param_total_list.index(rank) + 1][::-1][::shard_stride]
                param_index.extend(param_total_list[param_total_list.index(rank):][::shard_stride])
                param_index = list(set(param_index))
                param_index.sort()
                for rank_num in param_index:
                    if param_total_dict[param.name][rank_num].data.dtype == mstype.bfloat16:
                        param_stride.append(
                            cpu_cast(param_total_dict[param.name][rank_num].data, mstype.float32).asnumpy())
                    else:
                        param_stride.append(param_total_dict[param.name][rank_num].data.asnumpy())

                sliced_param = Parameter(Tensor(np.concatenate(param_stride)), name=param.name)
            else:
                sliced_param = param_total_dict[param.name][rank]

            sliced_params.append(sliced_param)
        if skip_merge_split:
            split_param = sliced_params[0]
        else:
            param_unique_strategy = _remove_repeated_slices(train_strategy[param.name])
            _param_unique_strategy = _convert_to_layout(param.name, param_unique_strategy)
            split_param = _merge_and_split(sliced_params, _param_unique_strategy, predict_strategy)
        opt_shard_group = predict_strategy[param.name][5] if predict_strategy else None
        if opt_shard_group:
            if split_param.data.dtype == mstype.bfloat16:
                data = cpu_cast(split_param.data, mstype.float32).asnumpy()
            else:
                data = split_param.data.asnumpy()
            rank = get_rank(opt_shard_group)
            size = get_group_size(opt_shard_group)
            try:
                data_slice = np.split(data, size)[rank]
            except BaseException as e:
                logger.critical("Failed to load opt shard slice in load distributed checkpoint for {}. Data shape is {}"
                                " and group is {}".format(param.name, split_param.data.shape, opt_shard_group))
                raise RuntimeError(e.__str__() + f"\nFor 'load_distributed_checkpoint', failed to load opt shard slice"
                                                 f" in load distributed checkpoint for {param.name}. Data shape is "
                                                 f"{split_param.data.shape} and group is {opt_shard_group}.") from e
            split_param = Parameter(Tensor(data_slice), param.name,
                                    split_param.requires_grad, split_param.layerwise_parallel)
        param_dict[param.name] = split_param

    if param_not_in_strategy:
        logger.warning("For 'load_distributed_checkpoint', {} parameters in network are not in the slice strategy, "
                       "you can check whether 'predict_strategy' or 'train_strategy_filename' is correct."
                       .format(param_not_in_strategy))
    if param_not_in_ckpt:
        logger.warning("For 'load_distributed_checkpoint', {} parameters in network and slice strategy but not in "
                       "the checkpoint file, please check whether 'checkpoint_filenames' is correct."
                       .format(param_not_in_ckpt))

    load_param_into_net(network, param_dict, strict_load=strict_load)


def async_ckpt_thread_status():
    """
    Get the status of asynchronous save checkpoint thread.

    When performing asynchronous save checkpoint, you can determine whether the asynchronous thread is completed.

    Returns:
        bool, True, Asynchronous save checkpoint thread is running.
        False, Asynchronous save checkpoint thread is not executing.

    Examples:
        >>> import mindspore as ms
        >>> ms.async_ckpt_thread_status()
        False
    """
    thr_list = threading.enumerate()
    return True in [ele.getName() == "asyn_save_ckpt" for ele in thr_list]


def _check_predict_strategy(predict_strategy):
    """Check predict strategy."""

    def _check_int_list(arg):
        if not isinstance(arg, list):
            return False
        for item in arg:
            if not isinstance(item, int):
                return False
        return True

    if predict_strategy is None:
        return

    flag = True
    predict_strategy = Validator.check_isinstance("predict_strategy", predict_strategy, dict)
    for key in predict_strategy.keys():
        if not isinstance(key, str) or not isinstance(predict_strategy[key], (list, tuple)) \
                or len(predict_strategy[key]) < 4:
            flag = False
        dev_matrix, tensor_map, param_split_shape, field_size = predict_strategy[key][:4]
        if not _check_int_list(dev_matrix) or not _check_int_list(tensor_map) or \
                not (_check_int_list(param_split_shape) or not param_split_shape) or \
                not (isinstance(field_size, int) and field_size == 0):
            flag = False

    if not flag:
        raise ValueError(f"For 'load_distributed_checkpoint', the argument 'predict_strategy' is dict, "
                         f"the key of it must be string, and the value of it must be list or tuple that "
                         f"the first four elements must be dev_matrix (list[int]), tensor_map (list[int]), "
                         f"param_split_shape (list[int]) and field_size (int, which value is 0)."
                         f"Please check whether 'predict_strategy' is correct.")


def _check_checkpoint_file(checkpoint_filenames):
    """Check checkpoint file name."""
    for index, filename in enumerate(checkpoint_filenames):
        if not isinstance(filename, str) or not os.path.exists(filename) \
                or filename[-5:] != ".ckpt" or os.path.getsize(filename) == 0:
            raise ValueError(f"For 'load_distributed_checkpoint', please check 'checkpoint_filenames', and "
                             f"make sure the {filename} at index {index} is a valid checkpoint file, it must "
                             f"be a string ending with '.ckpt', and the checkpoint file it represents must "
                             f"be exist and not empty.")


def _merge_and_split(sliced_params, train_strategy, predict_strategy):
    """Merge sliced parameter and split it according to the predict strategy."""
    merged_param = merge_sliced_parameter(sliced_params, train_strategy)
    if predict_strategy is None:
        return merged_param
    param_name = merged_param.name
    tensor_layout = predict_strategy[param_name]
    rank = get_rank()
    split_tensor = _load_tensor(merged_param.data, tensor_layout[0], tensor_layout[1], rank_id=rank)
    requires_grad = merged_param.requires_grad
    layerwise_parallel = merged_param.layerwise_parallel
    if merged_param.data.dtype == mstype.bfloat16:
        split_param = Parameter(Tensor(split_tensor, mstype.bfloat16), param_name, requires_grad, layerwise_parallel)
    else:
        split_param = Parameter(split_tensor, param_name, requires_grad, layerwise_parallel)
    return split_param


def _calculation_net_size(net):
    """Calculate the size of parameters in the network."""
    data_total = 0
    net_dict = net.parameters_dict()
    for name in net_dict:
        data_total += sys.getsizeof(net_dict[name].data.get_bytes()) / 1024

    return data_total


def _get_mindir_inputs(file_name):
    """
    Get MindIR file's inputs.

    Note:
        1. Parsing encrypted MindIR file is not supported.
        2. Parsing dynamic shape MindIR file is not supported.

    Args:
        file_name (str): MindIR file name.

    Returns:
        Tensor, list(Tensor), the input of MindIR file.

    Raises:
        TypeError: If the parameter file_name is not `str`.
        RuntimeError: MindIR's input is not tensor type or has no dims.

    Examples:
        >>> input_tensor = get_mindir_inputs("lenet.mindir")
    """
    Validator.check_file_name_by_regular(file_name)
    file_name = os.path.realpath(file_name)
    model = read_proto(file_name)
    input_tensor = []

    for ele_input in model.graph.input:
        input_shape = []
        if not hasattr(ele_input, "tensor") or not hasattr(ele_input.tensor[0], "dims"):
            raise RuntimeError("MindIR's inputs has no tensor or tensor has no dims, please check MindIR file.")

        for ele_shape in ele_input.tensor[0].dims:
            input_shape.append(ele_shape)
        if is_shape_unknown(input_shape):
            raise RuntimeError(f"MindIR input's shape is: {input_shape}, dynamic shape is not supported.")

        mindir_type = ele_input.tensor[0].data_type
        if mindir_type not in mindir_to_tensor_type:
            raise RuntimeError(f"MindIR input's type: {mindir_type} is not supported.")

        input_type = mindir_to_tensor_type.get(mindir_type)
        input_tensor.append(Tensor(shape=input_shape, dtype=input_type, init=One()))

    if not input_tensor:
        logger.warning("The MindIR model has no input, return None.")
        return None
    return input_tensor[0] if len(input_tensor) == 1 else input_tensor


def convert_model(mindir_file, convert_file, file_format):
    """
    Convert mindir model to other format model. The current version only supports conversion to ONNX models.

    .. warning::
        This is an experimental API that is subject to change or deletion.

    Args:
        mindir_file (str): MindIR file name.
        convert_file (str): Convert model file name.
        file_format (str): Convert model's format, current version only supports "ONNX".

    Raises:
        TypeError: If the parameter `mindir_file` is not `str`.
        TypeError: If the parameter `convert_file` is not `str`.
        ValueError: If the parameter `file_format` is not "ONNX".

    Examples:
        >>> import mindspore as ms
        >>> ms.convert_model("lenet.mindir", "lenet.onnx", "ONNX")
    """
    Validator.check_file_name_by_regular(mindir_file)
    Validator.check_file_name_by_regular(convert_file)
    if file_format != "ONNX":
        raise ValueError(f"For 'convert_model', 'file_format' must be 'ONNX', but got {file_format}.")
    net_input = _get_mindir_inputs(mindir_file)
    graph = load(mindir_file)
    net = nn.GraphCell(graph)
    if isinstance(net_input, Tensor):
        export(net, net_input, file_name=convert_file, file_format=file_format)
    else:
        export(net, *net_input, file_name=convert_file, file_format=file_format)


def _transform_tensor_to_numpy(path, name_map=None):
    return _load_and_transform(path, name_map, mindspore.load_checkpoint, lambda v, new_name: v.asnumpy())


def _transform_numpy_to_tensor(path, name_map=None):
    return _load_and_transform(path, name_map, load_file, lambda v, new_name: mindspore.Parameter(v, name=new_name))


def _process_file(file_info):
    cur_ckpt_path, name_map, save_path, file = file_info
    param_dict_numpy = _transform_tensor_to_numpy(cur_ckpt_path, name_map)
    safetensors_filename = file.replace(".ckpt", ".safetensors")
    dst_file = os.path.join(save_path, safetensors_filename)
    save_file(param_dict_numpy, dst_file)


def _process_file_safetensors(file_info):
    cur_safe_path, name_map, save_path, file = file_info
    param_dict_tensor = _transform_numpy_to_tensor(cur_safe_path, name_map)
    ckpt_filename = file.replace(".safetensors", ".ckpt")
    dst_file = os.path.join(save_path, ckpt_filename)
    mindspore.save_checkpoint(param_dict_tensor, dst_file)


def _gather_safetensors_tasks(file_path, save_path, file_name_regex, name_map):
    """gather transform rank together"""
    tasks = []
    for root, dirs, _ in os.walk(file_path):
        if root != file_path:
            continue

        rank_dirs = [d for d in dirs if d.startswith('rank')]
        if not rank_dirs:
            raise ValueError(
                f"For 'safetensors_to_ckpt', no directories starting with 'rank' found in {file_path}")

        for rank_dir in rank_dirs:
            rank_dir_path = os.path.join(root, rank_dir)
            dst_root = os.path.join(save_path,
                                    os.path.relpath(rank_dir_path, file_path)) if save_path else rank_dir_path
            os.makedirs(dst_root, exist_ok=True)
            tasks.extend(
                (os.path.join(rank_dir_path, file), name_map, dst_root, file)
                for file in os.listdir(rank_dir_path)
                if file.endswith(".safetensors") and (file_name_regex is None or re.findall(file_name_regex, file))
            )
    return tasks


def _gather_tasks_covert(file_path, save_path, file_name_regex, name_map):
    """gather transform rank together"""
    tasks = []
    for root, dirs, _ in os.walk(file_path):
        if root != file_path:
            continue

        rank_dirs = [d for d in dirs if d.startswith('rank')]
        if not rank_dirs:
            raise ValueError(
                f"For 'ckpt_to_safetensors', no directories starting with 'rank' found in {file_path}")

        for rank_dir in rank_dirs:
            rank_dir_path = os.path.join(root, rank_dir)
            dst_root = os.path.join(save_path,
                                    os.path.relpath(rank_dir_path, file_path)) if save_path else rank_dir_path
            os.makedirs(dst_root, exist_ok=True)
            tasks.extend(
                (os.path.join(rank_dir_path, file), name_map, dst_root, file)
                for file in os.listdir(rank_dir_path)
                if file.endswith(".ckpt") and (file_name_regex is None or re.findall(file_name_regex, file))
            )
    return tasks


def ckpt_to_safetensors(file_path, save_path=None, name_map=None, file_name_regex=None, processes_num=1):
    """
    Converts MindSpore checkpoint files into safetensors format and saves them to `save_path`.
    Safetensors is a reliable and portable machine learning model storage format introduced by Huggingface,
    used for securely storing Tensors with fast speed (zero copy).

    Note:
        The number of multiprocess settings is related to the size of the host, and it is not recommended to set it
        too large, otherwise it may cause freezing.
        The safetensors format does not support the enc verification function. If ckpt is enabled to save enc
        verification, an error will be generated when performing the conversion.
        The safetensors format currently does not support crc verification function. If ckpt contains crc verification
        information, the crc verification information will be lost after conversion to safetensors.

    Args:
        file_path (str): Path to the directory containing checkpoint files or a single checkpoint file (.ckpt).
        save_path (str, optional): Directory path where safetensors files will be saved. Defaults: ``None``.
        name_map (dict, optional): Dictionary mapping original parameter names to new names. Defaults: ``None``.
        file_name_regex (str, optional): Regular expression used to match the file that needs to be converted.
                                   Defaults: ``None``.
        processes_num (int, optional): Number of processes to use for parallel processing. Defaults: 1.
    Raises:
        ValueError: If the input path is invalid or the save_path is not a directory,
                    or the file_path does not end with '.ckpt'.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> import mindspore as ms
        >>> ms.ckpt_to_safetensors("./ckpt_save_path")
        >>> ms.ckpt_to_safetensors("./ckpt_save_path/rank0/checkpoint_0.ckpt")
        >>> ms.ckpt_to_safetensors(file_path="./ckpt_save_path/rank0/checkpoint_0.ckpt", save_path="./new_path/")
        >>> namemap = {"lin.weight":"new_name"}
        >>> ms.ckpt_to_safetensors("./ckpt_save_path/rank0/checkpoint_0.ckpt", "./new_path/", namemap)
    """
    is_dir = os.path.isdir(file_path)
    is_file = os.path.isfile(file_path)
    if not is_dir and not is_file:
        raise ValueError(f"For 'ckpt_to_safetensors', the input path must be a valid path or file, but got {file_path}")
    if save_path and os.path.splitext(save_path)[1]:
        raise ValueError(f"For 'ckpt_to_safetensors', the save_path must be a directory, but got '{save_path}'")
    if name_map is not None and not isinstance(name_map, dict):
        raise ValueError(
            f"For 'ckpt_to_safetensors', the type of 'name_map' must be a directory, but got '{type(name_map)}'")

    if is_dir:
        tasks = _gather_tasks_covert(file_path, save_path, file_name_regex, name_map)
        with mp.Pool(processes=processes_num) as pool:
            list(_progress_bar(pool.imap(_process_file, tasks), total=len(tasks)))
    elif is_file:
        if not file_path.endswith(".ckpt"):
            raise ValueError(f"For 'ckpt_to_safetensors', the input file must be a .ckpt file, but got {file_path}")
        if file_name_regex is not None and not re.findall(file_name_regex, file_path):
            raise ValueError(f"For 'ckpt_to_safetensors', the input file does not match the regular expression.")
        if save_path and not os.path.exists(save_path):
            os.makedirs(save_path, exist_ok=True)

        param_dict_numpy = _transform_tensor_to_numpy(file_path, name_map)
        safetensors_filename = os.path.basename(file_path).replace(".ckpt", ".safetensors")
        dst_file = os.path.join(save_path if save_path else os.path.dirname(file_path), safetensors_filename)
        save_file(param_dict_numpy, dst_file)


def safetensors_to_ckpt(file_path, save_path=None, name_map=None, file_name_regex=None, processes_num=1):
    """
    Converts safetensors files into MindSpore checkpoint format and saves them to `save_path`.
    Safetensors is a reliable and portable machine learning model storage format introduced by Huggingface,
    used for securely storing Tensors with fast speed (zero copy).

    Note:
        The number of multiprocess settings is related to the size of the host, and it is not recommended to set it
        too large, otherwise it may cause freezing.

    Args:
        file_path (str): Path to the directory containing safetensors files or a single safetensors file (.safetensors).
        save_path (str, optional): Directory path where checkpoint files will be saved. Defaults: ``None``.
        name_map (dict, optional): Dictionary mapping original parameter names to new names. Defaults: ``None``.
        file_name_regex (str, optional): Regular expression used to match the file that needs to be converted.
                                   Defaults: ``None``.
        processes_num (int, optional): Number of processes to use for parallel processing. Defaults: 1.

    Raises:
        ValueError: If the input path is invalid, the save_path is not a directory,
                    or the file_path does not end with '.safetensors'.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> import mindspore as ms
        >>> ms.safetensors_to_ckpt("./safetensors_save_path")
        >>> ms.safetensors_to_ckpt("./safetensors_save_path/rank0/checkpoint_0.safetensors")
        >>> ms.safetensors_to_ckpt("./safetensors_save_path/rank0/checkpoint_0.safetensors", "./new_path/")
        >>> namemap = {"lin.weight":"new_name"}
        >>> ms.safetensors_to_ckpt("./safetensors_save_path/rank0/checkpoint_0.safetensors", "./new_path/", namemap)
    """
    is_dir = os.path.isdir(file_path)
    is_file = os.path.isfile(file_path)
    if not is_dir and not is_file:
        raise ValueError(f"For 'safetensors_to_ckpt', the input path must be a valid path or file, but got {file_path}")
    if save_path and os.path.splitext(save_path)[1]:
        raise ValueError(f"For 'safetensors_to_ckpt', the save_path must be a directory, but got '{save_path}'")
    if name_map is not None and not isinstance(name_map, dict):
        raise ValueError(
            f"For 'safetensors_to_ckpt', the type of 'name_map' must be a directory, but got '{type(name_map)}'")

    if is_dir:
        tasks = _gather_safetensors_tasks(file_path, save_path, file_name_regex, name_map)
        with mp.Pool(processes=processes_num) as pool:
            list(_progress_bar(pool.imap(_process_file_safetensors, tasks), total=len(tasks)))
    elif is_file:
        if not file_path.endswith(".safetensors"):
            raise ValueError(
                f"For 'safetensors_to_ckpt', the input file must be a .safetensors file, but got {file_path}")
        if file_name_regex is not None and not re.findall(file_name_regex, file_path):
            raise ValueError(f"For 'safetensors_to_ckpt', the input file does not match the regular expression.")
        if save_path and not os.path.exists(save_path):
            os.makedirs(save_path, exist_ok=True)

        param_dict_tensor = _transform_numpy_to_tensor(file_path, name_map)
        ckpt_filename = os.path.basename(file_path).replace(".safetensors", ".ckpt")
        dst_file = os.path.join(save_path if save_path else os.path.dirname(file_path), ckpt_filename)
        mindspore.save_checkpoint(param_dict_tensor, dst_file)

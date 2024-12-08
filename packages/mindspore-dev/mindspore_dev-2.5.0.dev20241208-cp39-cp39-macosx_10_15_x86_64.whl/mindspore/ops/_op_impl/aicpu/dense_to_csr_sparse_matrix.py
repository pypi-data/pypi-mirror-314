# Copyright 2022 Huawei Technologies Co., Ltd
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

"""DenseToCSRSparseMatrix op"""
from mindspore.ops.op_info_register import op_info_register, AiCPURegOp, DataType
dense_to_csr_sparse_matrix_op_info = AiCPURegOp("DenseToCSRSparseMatrix") \
    .fusion_type("OPAQUE") \
    .input(0, "dense_input", "required") \
    .input(1, "indices", "required") \
    .output(0, "y_dense_shape", "required") \
    .output(1, "y_batch_pointers", "required") \
    .output(2, "y_row_pointers", "required") \
    .output(3, "y_col_indices", "required") \
    .output(4, "y_values", "required") \
    .dtype_format(DataType.F64_Default, DataType.I32_Default, DataType.I32_Default, DataType.I32_Default,
                  DataType.I32_Default, DataType.I32_Default, DataType.F64_Default) \
    .dtype_format(DataType.F32_Default, DataType.I32_Default, DataType.I32_Default, DataType.I32_Default,
                  DataType.I32_Default, DataType.I32_Default, DataType.F32_Default) \
    .dtype_format(DataType.C64_Default, DataType.I32_Default, DataType.I32_Default, DataType.I32_Default,
                  DataType.I32_Default, DataType.I32_Default, DataType.C64_Default) \
    .dtype_format(DataType.C128_Default, DataType.I32_Default, DataType.I32_Default, DataType.I32_Default,
                  DataType.I32_Default, DataType.I32_Default, DataType.C128_Default) \
    .dtype_format(DataType.F64_Default, DataType.I64_Default, DataType.I64_Default, DataType.I64_Default,
                  DataType.I64_Default, DataType.I64_Default, DataType.F64_Default) \
    .dtype_format(DataType.F32_Default, DataType.I64_Default, DataType.I64_Default, DataType.I64_Default,
                  DataType.I64_Default, DataType.I64_Default, DataType.F32_Default) \
    .dtype_format(DataType.C64_Default, DataType.I64_Default, DataType.I64_Default, DataType.I64_Default,
                  DataType.I64_Default, DataType.I64_Default, DataType.C64_Default) \
    .dtype_format(DataType.C128_Default, DataType.I64_Default, DataType.I64_Default, DataType.I64_Default,
                  DataType.I64_Default, DataType.I64_Default, DataType.C128_Default) \
    .get_op_info()


@op_info_register(dense_to_csr_sparse_matrix_op_info)
def _dense_to_csr_sparse_matrix_aicpu():
    """DenseToCSRSparseMatrix AiCPU register"""
    return

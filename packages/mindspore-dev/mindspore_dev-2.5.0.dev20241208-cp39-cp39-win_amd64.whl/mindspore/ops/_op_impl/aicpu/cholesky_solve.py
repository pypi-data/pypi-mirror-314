# Copyright 2021 Huawei Technologies Co., Ltd
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

"""CholeskySolve op"""
from mindspore.ops.op_info_register import op_info_register, AiCPURegOp, DataType

cholesky_solve_op_info = AiCPURegOp("CholeskySolve") \
    .fusion_type("OPAQUE") \
    .input(0, "x1", "required") \
    .input(1, "x2", "required") \
    .output(0, "y", "required") \
    .attr("upper", "bool") \
    .dtype_format(DataType.F32_Default, DataType.F32_Default, DataType.F32_Default) \
    .dtype_format(DataType.F64_Default, DataType.F64_Default, DataType.F64_Default) \
    .get_op_info()


@op_info_register(cholesky_solve_op_info)
def _cholesky_solve_aicpu():
    """CholeskySolve aicpu register"""
    return

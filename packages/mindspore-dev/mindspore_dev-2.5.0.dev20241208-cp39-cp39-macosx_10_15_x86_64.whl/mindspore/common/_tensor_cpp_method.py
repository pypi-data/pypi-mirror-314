# Copyright 2024 Huawei Technologies Co., Ltd
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
"""Add tensor cpp methods for stub tensor"""

tensor_cpp_methods = ['abs', '__abs__', 'absolute', 'add', '__add__', 'all', 'any', 'argmax', 'argmin', 'atan2', 'arctan2', 'ceil', 'chunk', 'clamp', 'clip', 'clone', 'cos', 'cumsum', 'div', 'divide', 'eq', 'erf', 'exp', 'flatten', 'floor', 'gather', 'greater', 'gt', 'index_select', 'isfinite', 'isneginf', 'less', 'lt', 'less_equal', 'le', 'log', 'logical_and', 'logical_not', 'logical_or', 'masked_fill', 'masked_select', 'matmul', 'max', 'maximum', 'mean', 'min', 'minimum', 'mul', 'nan_to_num', 'neg', 'negative', 'new_ones', 'new_zeros', 'not_equal', 'ne', 'pow', 'prod', 'reciprocal', 'remainder', 'repeat_interleave', 'reshape', 'round', 'rsqrt', 'scatter_', 'select', 'sigmoid', 'sin', 'sort', 'split', 'sqrt', 'square', 'sub', '__isub__', '__sub__', 'sum', 'tanh', 'tile', 'to', 'topk', 'tril', 'triu', 'trunc', 'where']

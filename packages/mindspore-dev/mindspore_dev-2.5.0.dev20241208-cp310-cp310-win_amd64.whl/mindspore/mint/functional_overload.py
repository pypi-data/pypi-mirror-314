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
"""Holding mint APIs"""
from mindspore._c_expression import _clamp_instance
from mindspore._c_expression import _div_instance
from mindspore._c_expression import _fmod_instance
from mindspore._c_expression import _remainder_instance
from mindspore._c_expression import _repeat_interleave_instance
from mindspore._c_expression import _split_instance

def clamp(*args, **kwargs):
    return _clamp_instance(*args, **kwargs)


def clip(*args, **kwargs):
    return _clamp_instance(*args, **kwargs)


def div(*args, **kwargs):
    return _div_instance(*args, **kwargs)


def divide(*args, **kwargs):
    return _div_instance(*args, **kwargs)


def fmod(*args, **kwargs):
    return _fmod_instance(*args, **kwargs)


def remainder(*args, **kwargs):
    """
    remainder(input, other) -> Tensor

    Computes the remainder of `input` divided by `other` element-wise. The result has the same sign as the divisor and
    its absolute value is less than that of `other`.

    Supports broadcasting to a common shape and implicit type promotion.

    .. math::

        remainder(input, other) = input - input.div(other, rounding\_mode="floor") * other

    Note:
        Complex inputs are not supported. At least one input need to be tensor, but not both are bool tensors.

    Args:
        input (Union[Tensor, numbers.Number, bool]): The dividend is a numbers.Number or
            a bool or a tensor whose data type is
            `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore/mindspore.dtype.html>`_ or
            `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore/mindspore.dtype.html>`_.
        other (Union[Tensor, numbers.Number, bool]): The divisor is a numbers.Number or
            a bool or a tensor whose data type is number or bool\_ when the dividend is a tensor.
            When the dividend is Scalar, the divisor must be a Tensor whose data type is number or bool\_.

    Returns:
        Tensor, with dtype promoted and shape broadcasted.

    Raises:
        TypeError: If `input` and `other` are not of types: (tensor, tensor), (tensor, number), (tensor, bool),
            (number, tensor) or (bool, tensor).
        ValueError: If `input` and `other` are not broadcastable.

    Supported Platforms:
        ``Ascend``

    Examples:
        >>> import numpy as np
        >>> from mindspore import Tensor, ops
        >>> x = Tensor(np.array([-4.0, 5.0, 6.0]).astype(np.float32))
        >>> y = Tensor(np.array([3.0, 2.0, 3.0]).astype(np.float64))
        >>> output = ops.remainder_ext(x, y)
        >>> print(output)
        [2.  1.  0.]
    """
    return _remainder_instance(*args, **kwargs)


def repeat_interleave(*args, **kwargs):
    return _repeat_interleave_instance(*args, **kwargs)


def split(*args, **kwargs):
    return _split_instance(*args, **kwargs)

__all__ = [
    "clamp",
    "clip",
    "div",
    "divide",
    "fmod",
    "remainder",
    "repeat_interleave",
    "split",
]

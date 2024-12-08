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
"""normalization for mint"""
from __future__ import absolute_import
from __future__ import division

from mindspore import mint
from mindspore.nn.cell import Cell


class _AdaptiveAvgPoolNd(Cell):
    """Common base of AdaptiveAvgPoolNd"""

    def __init__(self, output_size) -> None:
        super(_AdaptiveAvgPoolNd, self).__init__()
        self.output_size = output_size

    def extend_repr(self):
        return 'output_size={}'.format(self.output_size)


class AdaptiveAvgPool1d(_AdaptiveAvgPoolNd):
    r"""
    Applies a 1D adaptive average pooling over an input signal composed of several input planes.

    The output is of size :math:`L_{out}` , for any input size.
    The number of output features is equal to the number of input planes.

    .. warning::
        This is an experimental API that is subject to change or deletion.

    Args:
        output_size (int): the target output size :math:`L_{out}` .

    Inputs:
        - **input** (Tensor) - The input with shape :math:`(N, C, L_{in})` or :math:`(C, L_{in})` .

    Supported Platforms:
        ``Ascend``

    Examples:
        >>> import mindspore
        >>> from mindspore import Tensor, mint
        >>> import numpy as np
        >>> input = Tensor(np.array([[[2, 1, 2], [2, 3, 5]]]), mindspore.float16)
        >>> net = mint.nn.AdaptiveAvgPool1d(3)
        >>> output = net(input)
        >>> print(output)
        [[[2. 1. 2.]
          [2. 3. 5.]]]
    """

    def construct(self, input):
        return mint.nn.functional.adaptive_avg_pool1d(input, self.output_size)


class AdaptiveAvgPool2d(_AdaptiveAvgPoolNd):
    r"""
    Applies a 2D adaptive average pooling over an input signal composed of several input planes.

    The output is of size :math:`H x W` , for any input size.
    The number of output features is equal to the number of input planes.

    .. warning::
        This is an experimental API that is subject to change or deletion.

    Args:
        output_size (Union(int, tuple[int])): the target output size of the image of the form :math:`H x W` .
            Can be a tuple :math:`(H, W)` or a single :math:`H` for square image :math:`H x H` .
            :math:`H` and :math:`W` can be either a ``int`` , or ``None`` which means the size will
            be the same as that of the input.

    Inputs:
        - **input** (Tensor) - The input with shape :math:`(N, C, H, W)` or :math:`(C, H, W)` .

    Supported Platforms:
        ``Ascend``

    Examples:
        >>> import mindspore
        >>> from mindspore import Tensor, mint
        >>> import numpy as np
        >>> input = Tensor(np.array([[[2, 1, 2], [2, 3, 5]]]), mindspore.float16)
        >>> net = mint.nn.AdaptiveAvgPool2d((2, 2))
        >>> output = net(input)
        >>> print(output)
        [[[1.5 1.5]
          [2.5 4. ]]]
    """

    def construct(self, input):
        return mint.nn.functional.adaptive_avg_pool2d(input, self.output_size)


class MaxUnpool2d(Cell):
    r"""
    Computes the inverse of `Maxpool2d`.

    `MaxUnpool2d` keeps the maximal value and set all position of non-maximal values to zero.
    Typically the input is of shape :math:`(N, C, H_{in}, W_{in})` or :math:`(C, H_{in}, W_{in})`,
    and the output is of shape :math:`(N, C, H_{out}, W_{out})` or :math:`(C, H_{out}, W_{out})`.
    The operation is as follows.

    .. math::
        \begin{array}{ll} \\
        H_{out} = (H{in} - 1) \times stride[0] - 2 \times padding[0] + kernel\_size[0] \\
        W_{out} = (W{in} - 1) \times stride[1] - 2 \times padding[1] + kernel\_size[1] \\
        \end{array}

    .. warning::
        This is an experimental API that is subject to change or deletion.

    Args:
        kernel_size (Union[int, tuple[int]]): The size of kernel used to take the maximum value,
            an int number that represents height and width of the kernel,
            or a tuple of two int numbers that represent height and width respectively.
        stride (Union[int, tuple[int]], optional): The distance of kernel moving,
            an int number that represents the height and width of movement are both stride,
            or a tuple of two int numbers that represent height and width of movement respectively.
            Default: ``None`` , which indicates the moving step is `kernel_size` .
        padding (Union[int, tuple[int]], optional): The pad value to be filled. Default: ``0`` .
            If `padding` is an integer, the paddings of height and width are the same, equal to padding.
            If `padding` is a tuple of two integers, the padding of height and width equal to padding[0]
            and padding[1] correspondingly.

    Inputs:
        - **input** (Tensor) - The input Tensor to invert.
          Tensor of shape :math:`(N, C, H_{in}, W_{in})` or :math:`(C, H_{in}, W_{in})`.
        - **indices** (Tensor) - Max values' index represented by the indices.
          Tensor of shape must be same with input 'input'.
          Values of indices must belong to :math:`[0, H_{in} \times W_{in} - 1]`.
          Data type must be in int32 or int64.
        - **output_size** (tuple[int], optional) - The target output size. Default: ``None`` .
          If output_size == (), then the shape of output computed by `kernel_size`, `stride` and `padding`.
          If output_size != (), then output_size must be :math:`(N, C, H, W)` , :math:`(C, H, W)` or :math:`(H, W)`
          and output_size must belong to :math:
          `[(N, C, H_{out} - stride[0], W_{out} - stride[1]), (N, C, H_{out} + stride[0], W_{out} + stride[1])]`.

    Returns:
        Tensor, with shape :math:`(N, C, H_{out}, W_{out})` or :math:`(C, H_{out}, W_{out})`,
        with the same data type with `input`.

    Raises:
        TypeError: If data type of `input` or `indices` is not supported.
        TypeError: If `kernel_size`, `stride` or `padding` is neither an int nor a tuple.
        ValueError: If numbers in `stride`, `padding` or `kernel_size` is not positive.
        ValueError: If the shape of `input` and `indices` are not equal.
        ValueError: If `input` whose length is not 3 or 4.
        ValueError: If `output_size` whose type is not tuple.
        ValueError: If `output_size` is not close to output size computed by attr `kernel_size`, `stride`, `padding`.

    Supported Platforms:
        ``Ascend``

    Examples:
        >>> import numpy as np
        >>> from mindspore import Tensor, mint
        >>> input = Tensor(np.array([[[[0, 1], [8, 9]]]]).astype(np.float32))
        >>> indices = Tensor(np.array([[[[0, 1], [2, 3]]]]).astype(np.int64))
        >>> net =  mint.nn.MaxUnpool2d(1, stride=1, padding=0)
        >>> output = net(input, indices)
        >>> print(output.asnumpy())
        [[[[0. 1.]
           [8. 9.]]]]
    """

    def __init__(self, kernel_size, stride=None, padding=0) -> None:
        super(MaxUnpool2d, self).__init__()
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding

    def construct(self, input, indices, output_size=None):
        return mint.nn.functional.max_unpool2d(input, indices,
                                               self.kernel_size, self.stride,
                                               self.padding, output_size)

__all__ = [
    'AdaptiveAvgPool2d',
    'AdaptiveAvgPool1d',
    'MaxUnpool2d',
]

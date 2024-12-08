# Copyright 2021-2022 Huawei Technologies Co., Ltd
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
"""Controlling dump behavior."""
from __future__ import absolute_import
from warnings import warn

import mindspore.context as context
from mindspore._c_expression import security


def set_dump(target, enabled=True):
    """
    Enable or disable dump for the `target` and its contents.

    `target` should be an instance of :class:`mindspore.nn.Cell` or :class:`mindspore.ops.Primitive` .
    Please note that this API takes effect only when Synchronous Dump is enabled and the `dump_mode`
    field in dump config file is ``"2"`` . See the `dump document
    <https://www.mindspore.cn/docs/en/master/model_train/debug/dump.html>`_ for details.
    The default enabled status for
    a :class:`mindspore.nn.Cell` or :class:`mindspore.ops.Primitive` is False.

    Note:
        1. This API only supports being called before training starts.
           If you call this API during training, it may not be effective.
        2. After using `set_dump(Cell, True)` , operators in forward and backward
           computation  (computation generated by the grad operations) of the
           cell will be dumped.
        3. For :class:`mindspore.nn.SoftmaxCrossEntropyWithLogits` layer, the forward
           computation and backward computation use the same set of
           operators. So you can only see dump data from backward computation.
           Please note that :class:`mindspore.nn.SoftmaxCrossEntropyWithLogits` layer will also use
           the above operators internally when initialized with `sparse=True` and
           `reduction="mean"` .

    Args:
        target (Union[Cell, Primitive]): The Cell instance or Primitive instance
            to which the dump flag is set.
        enabled (bool, optional): ``True`` means enable dump, ``False`` means disable dump.
            Default: ``True`` .

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Please set environment variable `MINDSPORE_DUMP_CONFIG` to the dump config file and set `dump_mode` field
            in dump config file to 2 before running this example.
            See `dump document <https://www.mindspore.cn/docs/en/master/model_train/debug/dump.html>`_ for details.

        >>> import numpy as np
        >>> import mindspore as ms
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, set_dump
        >>>
        >>> ms.set_context(device_target="Ascend", mode=ms.GRAPH_MODE)
        >>>
        >>> class MyNet(nn.Cell):
        ...     def __init__(self):
        ...         super().__init__()
        ...         self.conv1 = nn.Conv2d(5, 6, 5, pad_mode='valid')
        ...         self.relu1 = nn.ReLU()
        ...
        ...     def construct(self, x):
        ...         x = self.conv1(x)
        ...         x = self.relu1(x)
        ...         return x
        >>>
        >>> if __name__ == "__main__":
        ...     net = MyNet()
        ...     set_dump(net.conv1)
        ...     input_tensor = Tensor(np.ones([1, 5, 10, 10], dtype=np.float32))
        ...     output = net(input_tensor)
    """
    if security.enable_security():
        raise ValueError('The set_dump API is not supported, please recompile '
                         'source without "-s on".')

    import mindspore.nn as nn  # avoid circular import
    from mindspore.ops import Primitive
    if not isinstance(target, nn.Cell) and not isinstance(target, Primitive):
        raise ValueError(f"The \"target\" parameter must be an instance of "
                         f"Cell or Primitive, "
                         f"but got an instance of {type(target)}.")

    if not isinstance(enabled, bool):
        raise ValueError("The \"enabled\" parameter must be bool.")

    # Checking for device target and mode.
    current_target = context.get_context("device_target")
    if current_target != "Ascend":
        # We will not return here in case user changed device_target later.
        warn("Current device_target is {}, which is not supported by set_dump. "
             "Only Ascend device target is supported currently. "
             "If you have Ascend device, consider set device_target to Ascend "
             "before calling set_dump.".format(current_target))

    current_mode = context.get_context("mode")
    if current_mode != context.GRAPH_MODE:
        # We will not return here in case user changed mode later.
        warn(
            "Current mode is PYNATIVE_MODE, which is not supported by set_dump. "
            "Only GRAPH_MODE is supported currently. "
            "Consider set mode to GRAPH_MODE "
            "before calling set_dump.")

    # The actual set dump logic.
    if isinstance(target, nn.Cell):
        target.add_flags(dump=enabled)
        for cell in target.cells():
            set_dump(cell, enabled)

        primitives = getattr(target, "_primitives", {})
        for value in primitives.values():
            if value and "dump" in value.attrs:
                set_dump(value, enabled)

    if isinstance(target, Primitive):
        target.add_prim_attr("dump", "true" if enabled else "false")

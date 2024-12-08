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
"""Communication management API"""
from __future__ import absolute_import
from mindspore import log as logger
from mindspore.ops import ReduceOp, cat
from mindspore.common.tensor import Tensor
from mindspore._c_expression import Tensor as Tensor_
from mindspore.ops.primitive import _primexpr
from mindspore.communication._comm_helper import (
    _destroy_group_helper,
    _get_rank_helper,
    _get_size_helper,
    _get_backend,
    _get_group_ranks,
)
from mindspore.communication import (
    init,
    release,
    get_group_size,
    get_world_rank_from_group_rank,
    create_group,
    GlobalComm,
    get_group_rank_from_world_rank,
)
from mindspore.communication.comm_func import (
    _deal_comm_outputs,
    _check_all_tensors,
    _contiguous,
    _check_all_tensor_same_dtype,
    _is_split_sizes_empty,
    _get_size,
    _get_group_rank_from_world_rank_from_cache_helper,
)
from mindspore.ops.auto_generate.gen_ops_prim import (
    dist_comm_all_gather_op,
    dist_comm_all_reduce_op,
    dist_comm_reduce_scatter_op,
    dist_comm_isend_op,
    dist_comm_all_to_all_v_op,
    dist_comm_reduce_scatter_tensor_op,
    dist_comm_all_to_all_v_single_op,
    dist_comm_broadcast_op,
    dist_comm_all_gather_into_tensor_op,
    dist_comm_irecv_op,
    dist_comm_scatter_tensor_op,
    dist_comm_gather_into_tensor_op,
    dist_comm_gather_op,
    dist_comm_reduce_op,
    dist_comm_scatter_op,
    dist_comm_barrier_op,
    dist_comm_batch_isend_irecv_op,
)


def init_process_group(backend="hccl",
                       init_method=None,
                       timeout=None,
                       world_size=-1,
                       rank=-1,
                       store=None,
                       pg_options=None,
                       device_id=None):
    """
    Init collective communication lib. And create a default collective communication group.

    Note:
        This method isn't supported in GPU and CPU versions of MindSpore.
        In Ascend hardware platforms, this API should be set before the definition of any Tensor and Parameter,
        and the instantiation and execution of any operation and net.

    Args:
        backend (str, optional): The backend to ues. default is hccl and now only support hccl.
        init_method (str, invalid): URL specifying how to init collective communication group. Provides parameters
            consistent with pytorch, but is not currently support, setting is invalid.
        timeout (timedelta, invalid): Timeout for API executed. Provides parameters consistent with pytorch, but is not
            currently support, setting is invalid.
        world_size (int, optional): Number of the processes participating in the job.
        rank (int, invalid): Rank of the current process. Provides parameters consistent with pytorch, but is not
            currently support, setting is invalid.
        store (Store, invalid): Key/Value store accessible to all workers, used to exchange connection/address
            information. Provides parameters consistent with pytorch, but is not currently support,
            setting is invalid.
        pg_options (ProcessGroupOptions, invalid): process group options specifying what additional options need to be
            passed in during the construction of specific process group. Provides parameters consistent with pytorch,
            but is not currently support, setting is invalid.
        device_id (int, invalid): the device id to exeute. Provides parameters consistent with pytorch, but is not
            currently support, setting is invalid.

    Raises:
        ValueError: If `backend` is not hccl.
        ValueError: If `world_size` is not equal to -1 or process group number.
        RuntimeError: If device target is invalid, or backend is invalid, or distributed initialization fails,
            or the environment variables RANK_ID/MINDSPORE_HCCL_CONFIG_PATH
            have not been exported when backend is HCCL.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

        >>> import mindspore as ms
        >>> from mindspore import set_context
        >>> from mindspore.mint.distributed import init_process_group, destroy_process_group
        >>> set_context(device_target="Ascend")
        >>> init_process_group()
        >>> destroy_process_group()
    """
    if init_method is not None:
        logger.warning("init_method is ignored, setting is invalid")
    if timeout is not None:
        logger.warning("timeout is ignored, setting is invalid")
    if store is not None:
        logger.warning("store is ignored, setting is invalid")
    if pg_options is not None:
        logger.warning("pg_options is ignored, setting is invalid")
    if device_id is not None:
        logger.warning("device_id is ignored, setting is invalid")
    if rank != -1:
        logger.warning("rank is ignored, setting is invalid")
    if backend != "hccl":
        raise ValueError(
            "Only support hccl now, please setting backend to hccl or using default value"
        )

    # init hccl & create world group
    init(backend)

    if world_size != -1 and world_size != get_group_size():
        raise ValueError(
            "world_size is wrong, please using default value or setting: ",
            get_group_size(),
        )


def destroy_process_group(group=None):
    """
    Destroy the user collective communication group.
    If group is None or "hccl_world_group", Destroy all group and release collective communication lib.

    Note:
        - This method isn't supported in GPU and CPU versions of MindSpore.
        - This method should be used after init_process_group().

    Args:
        group (str, optional): The communication group to work on. Normally, the group should be created by
            `mindspore.mint.distributed.new_group`. If ``None``, which means ``"hccl_world_group"`` in Ascend.
            Default: ``None``.

    Raises:
        TypeError: If group is not a string.
        RuntimeError: If HCCL is not available or MindSpore is GPU/CPU version.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

        >>> import mindspore as ms
        >>> from mindspore import set_context
        >>> from mindspore.mint.distributed import init_process_group, destroy_process_group
        >>> set_context(device_target="Ascend")
        >>> init_process_group()
        >>> destroy_process_group()
    """

    if group == GlobalComm.WORLD_COMM_GROUP or group is None:
        release()
    elif not isinstance(group, str):
        raise TypeError(
            "For 'destroy_group', the argument 'group' must be type of string or None, "
            "but got 'group' type : {}.".format(type(group))
        )
    else:
        _destroy_group_helper(group)


def get_rank(group=None):
    """
    Get the rank ID for the current device in the specified collective communication group.

    Note:
        This method should be used after mindspore.mint.distributed.init_process_group.

    Args:
        group (str, optional): The communication group to work on. Normally, the group should be created by
            `mindspore.mint.distributed.new_group`. If ``None``, which means ``"hccl_world_group"`` in Ascend.
            Default: ``None``.

    Returns:
        int, the rank ID of the calling process within the group.
        return -1, if not part of the group

    Raises:
        TypeError: If group is not a string.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

        >>> from mindspore import set_context
        >>> from mindspore.mint.distributed import init_process_group, get_rank
        >>> set_context(device_target="Ascend")
        >>> init_process_group()
        >>> rank_id = get_rank()
        >>> print(rank_id)
        >>> # the result is the rank_id in world_group
    """
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "For 'get_rank', the argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    try:
        ret = _get_rank_helper(group)
    except RuntimeError as e:
        logger.warning(e)
        ret = -1
    return ret


def get_world_size(group=None):
    """
    Get the rank size of the specified collective communication group.

    Note:
        This method should be used after mindspore.mint.distributed.init_process_group.

    Args:
        group (str, optional): The communication group to work on. Normally, the group should be created by
            `mindspore.mint.distributed.new_group`. If ``None``, which means ``"hccl_world_group"`` in Ascend.
            Default: ``None``.

    Returns:
        int, the rank size of the group.
        return -1, if the group is not available.

    Raises:
        TypeError: If group is not a string.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

        >>> import mindspore as ms
        >>> from mindspore import set_context
        >>> from mindspore.mint.distributed import init_process_group, get_world_size
        >>> set_context(device_target="Ascend")
        >>> init_process_group()
        >>> group_size = get_world_size()
        >>> print("group_size is: ", group_size)
        group_size is: 8
    """
    ret = -1
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "For 'get_world_size', the argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    try:
        ret = _get_size_helper(group)
    except RuntimeError as e:
        logger.warning(e)
        ret = -1
    return ret


def new_group(ranks=None,
              timeout=None,
              backend=None,
              pg_options=None,
              use_local_synchronization=False,
              group_desc=None):
    """
    Create a new distributed group.

    Note:
        This method should be used after init_process_group().

    Args:
        ranks (list[int], optional): List of ranks of group members. If ``None``,
            will be create the world group. Default is ``None``.
        timeout (int, invalid): Currently it is a reserved parameter.
        backend (str, invalid): Currently it is a reserved parameter.
        pg_options (str, invalid): Currently it is a reserved parameter.
        use_local_synchronization (bool, invalid): Currently it is a reserved parameter.
        group_desc (str, invalid): Currently it is a reserved parameter.

    Returns:
        A string with group name. Return "" in the abnormal scenarios.

    Raises:
        TypeError: If list ranks in Group has duplicate rank id.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.
            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

        >>> import mindspore as ms
        >>> from mindspore import set_context
        >>> from mindspore.mint.distributed import init_process_group, get_backend
        >>> set_context(device_target="Ascend")
        >>> init_process_group()
        >>> group = new_group()
        >>> print("group is: ", group)
        group is: hccl
    """
    if ranks is not None:
        if not isinstance(ranks, list):
            raise TypeError("ranks must be list, but got {}".format(type(ranks)))
        ranks = sorted(ranks)
    else:
        return GlobalComm.WORLD_COMM_GROUP
    group = "group_" + "_".join([str(elem) for elem in ranks])
    try:
        create_group(group, ranks)
    except RuntimeError as e:
        logger.warning(e)
        group = ""
    return group


def get_backend(group=None):
    """
    Get the backend of communication process groups.

    Note:
        Only one communication backend is supported by MindSpore for each process.
        It should be one of `hccl`/`nccl`/`mccl`. Currently only support hccl.

    Args:
        group (str, optional): The communication group to work on. It is a reserved parameter.
            Normally, the group should be created by `mindspore.mint.distributed.new_group`, If ``None``,
            which means ``"hccl_world_group"`` in Ascend. Default: ``None``.

    Returns:
        string, the backend of the group.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.
            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

        >>> import mindspore as ms
        >>> from mindspore import set_context
        >>> from mindspore.mint.distributed import init_process_group, get_backend
        >>> set_context(device_target="Ascend")
        >>> init_process_group()
        >>> backend = get_backend()
        >>> print("backend is: ", backend)
        backend is: hccl
    """
    return _get_backend()


def get_global_rank(group, group_rank):
    """
    A function that returns the rank id in the world group corresponding to the
    rank which id is 'group_rank' in the user group.

    Note:
        This method should be used after init_process_group().

    Args:
        group (str): The communication group to work on. Normally, the group should
            be created by `mindspore.mint.distributed.new_group`. If ``None``, which
            means ``"hccl_world_group"`` in Ascend.
        group_rank (int): Group rank to query.

    Returns:
        An integer scalar with the rank id in the world group.

    Raises:
        TypeError: If the `group` is not a str.
        TypeError: If the `group_rank` is not an integer.
        RuntimeError: If device target is invalid, or backend is invalid, or distributed initialization fails.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.

            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 4 devices.

        >>> import mindspore as ms
        >>> from mindspore import set_context
        >>> from mindspore.mint.distributed import init_process_group, get_global_rank, new_group, get_rank
        >>> set_context(device_target="Ascend")
        >>> init_process_group()
        >>> rank_ids = [0,4]
        >>> if get_rank() in rank_ids:
        ...     group = new_group(rank_ids)
        ...     world_rank_id = get_global_rank(group, 1)
        ...     print("world_rank_id is: ", world_rank_id)
        world_rank_id is: 4
    """
    if not isinstance(group_rank, int):
        raise TypeError(
            f"The group_rank argument must be integer, but got {type(group_rank)}."
        )

    if group is None or group is GlobalComm.WORLD_COMM_GROUP:
        return group_rank

    if not isinstance(group, str):
        raise TypeError(
            "For 'get_global_rank', the argument 'group' must be type of string or None, "
            "but got 'group' type : {}.".format(type(group))
        )
    return get_world_rank_from_group_rank(group, group_rank)


def get_group_rank(group, global_rank):
    """
    Get the rank ID in the specified user communication group corresponding to
    the rank ID in the world communication group.

    Note:
        This method should be used after mindspore.mint.distributed.init_process_group.

    Args:
        group (str): The communication group to work on. Normally, the group should be
            created by `mindspore.mint.distributed.new_group`. If ``None``, which means
            ``"hccl_world_group"`` in Ascend.
        global_rank (int): A rank ID in the world communication group.

    Returns:
        int, the rank ID in the user communication group.

    Raises:
        TypeError: If global_rank is not an integer or the group is not a string.
        RuntimeError: If device target is invalid, or backend is invalid, or distributed initialization fails.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

        >>> import mindspore as ms
        >>> from mindspore import set_context
        >>> from mindspore.mint.distributed import init_process_group, new_group, get_group_rank, get_rank
        >>> set_context(mode=ms.GRAPH_MODE, device_target="Ascend")
        >>> init_process_group()
        >>> rank_ids = [0,4]
        >>> if get_rank() in rank_ids:
        ...     group = new_group(rank_ids)
        ...     group_rank_id = get_group_rank(4, group)
        ...     print("group_rank_id is: ", group_rank_id)
        group_rank_id is: 1
    """
    if not isinstance(global_rank, int):
        raise TypeError(
            f"The global_rank argument must be integer, but got {type(global_rank)}."
        )
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "For 'get_group_rank_from_world_rank', the argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    return _get_group_rank_from_world_rank_from_cache_helper(
        world_rank_id=global_rank, group=group
    )


def get_process_group_ranks(group=None):
    """
    Gets the ranks of the specific group and returns the process ranks in the communication group as a list.

    Args:
        group (str, optional): The communication group to work on. Normally, the group should be created by
            `mindspore.mint.distributed.new_group`. If ``None``, which means ``"hccl_world_group"`` in Ascend.
            Default: ``None``.

    Returns:
        List (List[int]), List of process ranks in the specified communication group.

    Raises:
        TypeError: If the `group` is not a str.
        RuntimeError: If device target is invalid, or backend is invalid, or distributed initialization fails.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.

            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 4 devices.

        >>> import mindspore as ms
        >>> from mindspore import set_context
        >>> from mindspore.mint.distributed import init_process_group, get_process_group_ranks
        >>> set_context(device_target="Ascend")
        >>> init_process_group()
        >>> output = get_process_group_ranks()
        >>> print(output)
        [0, 1, 2, 3]

    """
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP

    if not isinstance(group, str):
        raise TypeError(
            "For 'get_process_group_ranks', the argument 'group' must be type of string or None, "
            "but got 'group' type : {}.".format(type(group))
        )
    return _get_group_ranks(group)


@_primexpr
def _check_all_tensor_same_dtype_and_shape(*tensor_lists):
    """check all the input tensor has same dtype and shape"""
    consistent_dtype = None
    consistent_shape = None
    for list_ in tensor_lists:
        if not isinstance(list_, (list, tuple)):
            list_ = [list_]
        for tensor_ in list_:
            if not isinstance(tensor_, Tensor):
                continue
            dtype = tensor_.dtype
            shape = tensor_.shape
            if consistent_dtype is None:
                consistent_dtype = dtype
                consistent_shape = shape
            else:
                if dtype != consistent_dtype:
                    raise TypeError(
                        "tensor_lists dtype must be the same, "
                        f"but got {consistent_dtype} and {dtype}."
                    )
                if shape != consistent_shape:
                    raise TypeError(
                        "tensor_lists shape must be the same, "
                        f"but got {consistent_shape} and {shape}."
                    )


def all_reduce(tensor, op=ReduceOp.SUM, group=None, async_op=False):
    """
    Reduce tensors across all devices in such a way that all deviceswill get the same final result,
    returns the tensor which is all reduced.

    Note:
        The tensors must have the same shape and format in all processes of the collection.

    Args:
        tensor (Tensor): The input and output tensor of collective. The shape of tensor is :math:`(x_1, x_2, ..., x_R)`.
            The function operates in-place.
        op (str, optional): Specifies an operation used for element-wise reductions, like sum, prod, max, and min.
            Default: ``ReduceOp.SUM`` .
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        async_op (bool, optional): Whether this operator should be an async operator. Default: ``False`` .

    Returns:
        CommHandle, CommHandle is an async work handle, if `async_op` is set to True. CommHandle will be None,
        when `async_op` is False.

    Raises:
        TypeError: If the type of the first input parameter is not Tensor, or any of `op` and `group` is not a str,
                   `op` range is illegal or async_op is not bool.
        RuntimeError: If device target is invalid, or backend is invalid, or distributed initialization fails.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> import numpy as np
        >>> from mindspore.mint.distributed import init_process_group
        >>> from mindspore.mint.distributed import all_reduce
        >>> from mindspore import Tensor
        >>>
        >>> init_process_group()
        >>> tensor = Tensor(np.ones([2, 8]).astype(np.float32))
        >>> output = all_reduce(tensor)
        >>> print(tensor)
        [[2. 2. 2. 2. 2. 2. 2. 2.]
         [2. 2. 2. 2. 2. 2. 2. 2.]]

    """
    if not isinstance(tensor, (Tensor, Tensor_)):
        raise TypeError("For all_reduce, the input tensor must be tensor")
    if not isinstance(op, str):
        raise TypeError("For all_reduce, the input op type must be str")
    if op not in ("sum", "prod", "min", "max"):
        raise TypeError(
            "For all_reduce, the input op value must be one of sum, prod, min, max"
        )

    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP

    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if not isinstance(async_op, bool):
        raise TypeError(
            f"The argument 'async_op' must be a bool, but got {type(async_op)}."
        )

    output = dist_comm_all_reduce_op(tensor, op, group)
    _, handle = _deal_comm_outputs(output, async_op)
    return handle


def all_gather_into_tensor(output_tensor, input_tensor, group=None, async_op=False):
    """
    Gathers tensors from the specified communication group and returns the tensor which is all gathered.

    Note:
        The tensors must have the same shape and format in all processes of the collection.

    Args:
        output_tensor (Tensor): The output tensor to be all gathered into tensor.If the number of devices
            in the group is N, then the shape of output tensor is :math:`(N*x_1, x_2, ..., x_R)`.
        input_tensor (Tensor): The input tensor to be all gathered into tensor.
            The shape of tensor is :math:`(x_1, x_2, ..., x_R)`.
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        async_op (bool, optional): Whether this operator should be an async operator. Default: ``False`` .

    Returns:
        CommHandle,  CommHandle is an async work handle, if `async_op` is set to True.
        CommHandle will be None, when `async_op` is False.

    Raises:
        TypeError: If the type of the input_tensor or output_tensor parameter is not Tensor,
            `group` is not a str, or async_op is not bool.
        RuntimeError: If device target is invalid, or backend is invalid, or distributed initialization fails.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> import numpy as np
        >>> import mindspore as ms
        >>> from mindspore import ops
        >>> from mindspore.mint.distributed import init_process_group
        >>> from mindspore.mint.distributed import all_gather_into_tensor
        >>> from mindspore import Tensor
        >>>
        >>> ms.set_context(mode=ms.GRAPH_MODE)
        >>> init_process_group()
        >>> input_tensor = Tensor(np.ones([2, 8]).astype(np.float32))
        >>> out_tensor = Tensor(np.zeros([4, 8]).astype(np.float32))
        >>> output = all_gather_into_tensor(out_tensor, input_tensor)
        >>> print(out_tensor)
        [[1. 1. 1. 1. 1. 1. 1. 1.]
         [1. 1. 1. 1. 1. 1. 1. 1.]
         [1. 1. 1. 1. 1. 1. 1. 1.]
         [1. 1. 1. 1. 1. 1. 1. 1.]]

    """

    if not isinstance(input_tensor, (Tensor, Tensor_)):
        raise TypeError("For all_gather_into_tensor, the input tensor must be tensor")
    if not isinstance(output_tensor, (Tensor, Tensor_)):
        raise TypeError("For all_gather_into_tensor, the output tensor must be tensor")
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if not isinstance(async_op, bool):
        raise TypeError(
            f"The argument 'async_op' must be a bool, but got {type(async_op)}."
        )
    group_size = get_group_size(group)
    result = dist_comm_all_gather_into_tensor_op(
        output_tensor, input_tensor, group_size, group
    )
    _, handle = _deal_comm_outputs(result, async_op)
    return handle


def reduce_scatter_tensor(output, input, op=ReduceOp.SUM, group=None, async_op=False):
    r"""
    Reduces and scatters tensors from the specified communication group and
    returns the tensor which is reduced and scattered.

    Note:
        The tensors must have the same shape and format in all processes of the collection.

    Args:
        output(Tensor): the output tensor has the same dtype as `input_x` with a shape of :math:`(N/rank\_size, *)`
        input(Tensor): The input tensor to be reduced and scattered, suppose it has a shape :math:`(N, *)`, where `*`
            means any number of additional dimensions. N must be divisible by rank_size.
            rank_size refers to the number of cards in the communication group.
        op (str, optional): Specifies an operation used for element-wise reductions,
            like SUM and MAX. Default: ``ReduceOp.SUM`` .
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        async_op (bool, optional): Whether this operator should be an async operator. Default: ``False`` .

    Returns:
        CommHandle, CommHandle is an async work handle, if `async_op` is set to True.
        CommHandle will be None, when `async_op` is False.

    Raises:
        TypeError: If the type of the input and output parameter is not Tensor, any of `op` and `group` is not a str.
            async_op is not bool or 'op' is invalid.
        ValueError: If the first dimension of the input cannot be divided by the rank_size.
        RuntimeError: If device target is invalid, or backend is invalid, or distributed initialization fails.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> import mindspore as ms
        >>> from mindspore import Tensor
        >>> from mindspore.mint.distributed import init_process_group
        >>> from mindspore.mint.distributed import reduce_scatter_tensor
        >>> import numpy as np
        >>>
        >>> ms.set_context(mode=ms.GRAPH_MODE)
        >>> init_process_group()
        >>> input_tensor = Tensor(np.ones([8, 8]).astype(np.float32))
        >>> output_tensor = Tensor(np.ones([4, 8]).astype(np.float32))
        >>> output = reduce_scatter_tensor(output_tensor ,input_tensor)
        >>> print(output_tensor)
        [[2. 2. 2. 2. 2. 2. 2. 2.]
         [2. 2. 2. 2. 2. 2. 2. 2.]
         [2. 2. 2. 2. 2. 2. 2. 2.]
         [2. 2. 2. 2. 2. 2. 2. 2.]]

    """

    if not isinstance(input, (Tensor, Tensor_)):
        raise TypeError("For reduce_scatter_tensor, the input tensor must be tensor")
    if not isinstance(output, (Tensor, Tensor_)):
        raise TypeError("For reduce_scatter_tensor, the output tensor must be tensor")
    if not isinstance(op, str):
        raise TypeError("For reduce_scatter_tensor, the input op type must be str")
    if op not in ("sum", "prod", "min", "max"):
        raise TypeError(
            "For reduce_scatter_tensor, the input op value must be one of sum, prod, min, max"
        )
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if not isinstance(async_op, bool):
        raise TypeError(
            f"The argument 'async_op' must be a bool, but got {type(async_op)}."
        )
    rank_size = get_group_size(group)
    result = dist_comm_reduce_scatter_tensor_op(output, input, rank_size, op, group)
    _, handle = _deal_comm_outputs(result, async_op)
    return handle


def reduce(tensor, dst, op=ReduceOp.SUM, group=None, async_op=False):
    """
    Reduces tensors across the processes in the specified communication group, sends the result
    to the target dst(global rank), and returns the tensor which is sent to the target process.

    Note:
        - Only process with destination rank receives the reduced output.
        - Only support PyNative mode, Graph mode is not currently supported.
        - Other processes only get a tensor with shape [1], which has no mathematical meaning.

    Args:
        tensor (Tensor): Input and output of the collective. The function operates in-place.
        dst (int): The target rank of the process(global rank) that receives the reduced output.
        op (str, optional): Specifies an operation used for element-wise reductions, like sum, prod, max, and min.
            Default: ``ReduceOp.SUM`` .
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        async_op (bool, optional): Whether this operator should be an async operator. Default: ``False`` .

    Returns:
        CommHandle, CommHandle is an async work handle, if `async_op` is set to True.
        CommHandle will be None, when `async_op` is False.

    Raises:
        TypeError: If the type of `tensor` is not Tensor, any of `op` and `group` is not a str.
            async_op is not bool or 'op' is invalid.
        RuntimeError: If device target is invalid, or backend is invalid, or distributed initialization fails.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.

            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 4 devices.

        >>> from mindspore import ops
        >>> import mindspore.nn as nn
        >>> from mindspore.mint.distributed import init_process_group, reduce
        >>> from mindspore import Tensor
        >>> import numpy as np
        >>> # Launch 4 processes.
        >>> init_process_group()
        >>> dest_rank=1
        >>> input_tensor = Tensor(np.ones([2, 8]).astype(np.float32))
        >>> output = reduce(input_tensor)
        >>> print(input_tensor)
        Process with rank 1: [[4. 4. 4. 4. 4. 4. 4. 4.]
                             [4. 4. 4. 4. 4. 4. 4. 4.]],
        Other proesses: [0.].
    """

    if not isinstance(tensor, (Tensor, Tensor_)):
        raise TypeError("For reduce, the input tensor must be tensor")
    if not isinstance(dst, int):
        raise TypeError("For reduce, the dst must be int")
    if not isinstance(op, str):
        raise TypeError("For reduce, the input op type must be str")
    if op not in ("sum", "prod", "min", "max"):
        raise TypeError(
            "For reduce, the input op value must be one of sum, prod, min, max"
        )
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if not isinstance(async_op, bool):
        raise TypeError(
            f"The argument 'async_op' must be a bool, but got {type(async_op)}."
        )
    result = dist_comm_reduce_op(tensor, op, dst, group)
    _, handle = _deal_comm_outputs(result, async_op)
    return handle


class P2POp:
    """
    Object for `batch_isend_irecv` input, to store information of ``"isend"`` and ``"irecv"``.

    Note:
        `tensor` will be modified in-place by final result when `op` is ``"irecv"``.

    Args:
        op(Union[str, function]): Only string of ``"isend"`` and ``"irecv"`` are allowed.
            Or function of ``distributed.isend`` and ``distributed.irecv`` are allowed.
        tensor(Tensor): tensor for sending/receiving.
        peer(int): remote global rank for send/receive.
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        tag(int, optional): currently not supported yet. Default: ``0``.

    Returns:
        P2POp Object.

    Raises:
        ValueError: when `op` is not string or function of 'isend' and 'irecv'.
        TypeError: when `tensor` is not type of Tensor or 'peer' is not int.
        NotImplementedError: when `tag` is not 0.

    Supported Platforms:
        ``Ascend``

    Examples:
        >>> import numpy as np
        >>> import mindspore
        >>> from mindspore.mint.distributed import P2POp, isend, irecv
        >>> from mindspore import Tensor
        >>> send_tensor = Tensor(1.)
        >>> send_op = P2POp('isend', send_tensor, 1)
        >>> send_op = P2POp(isend, send_tensor, 1)
        >>> recv_tensor = Tensor(0.)
        >>> recv_op = P2POp('irecv', recv_tensor, 0)
        >>> recv_op = P2POp(irecv, recv_tensor, 0)
    """

    def __init__(self, op, tensor, peer, group=None, tag=0):
        self.op = op
        self.tensor = tensor
        self.peer = peer
        self.group = group
        self.tag = tag

    def __new__(cls, op, tensor, peer, group=None, tag=0):
        if isinstance(op, str):
            op_name = op
            if op_name not in ["isend", "irecv"]:
                raise ValueError(
                    f"Expected ``op`` to be of type ``isend`` or ``irecv``, but got {op_name}"
                )
        else:
            if op not in [isend, irecv]:
                raise ValueError(
                    f"Expected ``op`` to be of type ``isend`` or ``irecv``, but got {op}"
                )
            op_name = op.__name__

        if not isinstance(tensor, (Tensor, Tensor_)):
            raise TypeError(
                f"Expected ``tensor`` to be Tensor, but got {type(tensor)}."
            )
        if not isinstance(peer, int):
            raise TypeError("For P2POp, the peer must be int")
        if tag != 0:
            raise NotImplementedError("``tag`` not support yet.")
        return object.__new__(cls)


TYPE_ISEND = 0
TYPE_IRECV = 1


def batch_isend_irecv(p2p_op_list):
    """
    Batch send and recv tensors asynchronously.

    Note:
        - The 'isend' and 'irecv' of `P2POp` in `p2p_op_list` between ranks need to match each other.
        - `P2POp` in `p2p_op_list` can only use the same communication group.
        - `tag` of `P2POp` in `p2p_op_list` is not support yet.
        - `tensor` of `P2POp` in `p2p_op_list` will not be modified by result inplace.
        - Only support PyNative mode, Graph mode is not currently supported.

    Args:
        p2p_op_list(list[P2POp]): list contains `P2POp`. `P2POp` is type of :class:`mindspore.mint.distributed.P2POp`

    Returns:
        list[CommHandle], CommHandle is an async work handle, Currently only one packaging handle is supported.

    Raises:
        TypeError: If `p2p_op_list` is empty or `p2p_op_list` are not all type of `P2POp`.
        TypeError: The group name in `p2p_op_list` are not consistent.
        TypeError: The `tensor` in `p2p_op_list` are not Tensor.
        TypeError: The `op` in `p2p_op_list` are not isend or irecv.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> import numpy as np
        >>> import mindspore
        >>> from mindspore.mint.distributed import init_process_group, get_rank, get_world_size
        >>> from mindspore.mint.distributed import import batch_isend_irecv, P2POp
        >>> from mindspore import Tensor
        >>>
        >>> init_process_group()
        >>> this_rank = get_rank()
        >>> world_size = get_world_size()
        >>> next_rank = (this_rank + 1) % world_size
        >>> prev_rank = (this_rank + world_size - 1) % world_size
        >>>
        >>> send_tensor = Tensor(this_rank + 1, dtype=mindspore.float32)
        >>> recv_tensor = Tensor(0., dtype=mindspore.float32)
        >>>
        >>> send_op = P2POp('isend', send_tensor, next_rank)
        >>> recv_op = P2POp('irecv', recv_tensor, prev_rank)
        >>>
        >>> p2p_op_list = [send_op, recv_op]
        >>> output = batch_isend_irecv(p2p_op_list)
        >>> print(recv_tensor)
        rank 0:
        (Tensor(shape=[], dtype=Float32, value= 0), Tensor(shape=[], dtype=Float32, value= 2))
        rank 1:
        (Tensor(shape=[], dtype=Float32, value= 0), Tensor(shape=[], dtype=Float32, value= 1))
    """
    tensors = []
    op_types = []
    remotes_ranks = []
    tags = []
    if not p2p_op_list:
        raise TypeError(f"p2p_op_list can not be empty list.")
    for _, p2p_op in enumerate(p2p_op_list):
        if not isinstance(p2p_op, P2POp):
            raise TypeError("The elements in p2p_op_list must be type of P2POp.")
    group = p2p_op_list[0].group

    type_ = None
    for _, p2p_op in enumerate(p2p_op_list):
        if group != p2p_op.group:
            raise TypeError("The group name in p2p_op_list must be consistent.")
        if isinstance(p2p_op.op, str):
            type_ = p2p_op.op
        else:
            type_ = p2p_op.op.__name__
        rank_ = (
            p2p_op.peer
            if p2p_op.group is None
            else get_group_rank_from_world_rank(p2p_op.peer, p2p_op.group)
        )
        remotes_ranks.append(rank_)
        tags.append(p2p_op.tag)
        if type_ == "isend":
            tensors.append(p2p_op.tensor)
            op_types.append(TYPE_ISEND)
        elif type_ == "irecv":
            if isinstance(p2p_op.tensor, Tensor):
                tensors.append(p2p_op.tensor)
                op_types.append(TYPE_IRECV)
            else:
                raise TypeError("p2p_op.tensor must be tensor")
        else:
            raise TypeError("p2p_op.op must be isend or irecv")

    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    output = dist_comm_batch_isend_irecv_op(tensors, group, op_types, remotes_ranks)
    _, handle = _deal_comm_outputs(output, True)
    return [handle]


def scatter_tensor(output_tensor, input_tensor, src=0, group=None, async_op=False):
    r"""
    Scatter tensor evently across the processes in the specified communication group.

    Note:
        - The interface behavior only support Tensor input and scatter evenly, which
            is different from that of `pytoch.distributed.scatter`.
        - Only the tensor in process `src` (global rank) will do scatter.
        - Only support PyNative mode, Graph mode is not currently supported.

    Args:
        output_tensor (Tensor): Output tensor. It should have the same size across all ranks.
        input_tensor (Tensor):  The input tensor to be scattered. The shape of tensor is :math:`(x_1, x_2, ..., x_R)`.
        src (int, optional): Specifies the rank(global rank) of the process that send the tensor.
            And only process `src` will send the tensor. Default is 0.
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        async_op (bool, optional): Whether this operator should be an async operator. Default: ``False`` .

    Returns:
        CommHandle, CommHandle is an async work handle, if `async_op` is set to True.
        CommHandle will be None, when `async_op` is False.

    Raise:
        TypeError: If the type of the first input parameter is not Tensor, or any of `op` and `group` is not a str.
        RuntimeError: If device target is invalid, or backend is invalid, or distributed initialization fails.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> import mindspore as ms
        >>> from mindspore.mint.distributed import init_process_group
        >>> from mindspore.communication.comm_func import scatter_tensor
        >>> import numpy as np
        >>> # Launch 2 processes.
        >>>
        >>> init_process_group()
        >>> input = ms.Tensor(np.arange(8).reshape([4, 2]).astype(np.float32))
        >>> output = ms.Tensor(np.zeros([2, 2]).astype(np.float32))
        >>> out = scatter_tensor(output, input, src=0)
        >>> print(output)
        # rank_0
        [[0. 1.]
         [2. 3.]]
        # rank_1
        [[4. 5.]
         [6. 7.]]
    """
    if not isinstance(input_tensor, (Tensor, Tensor_)):
        raise TypeError("For scatter_tensor, the input tensor must be tensor")
    if not isinstance(output_tensor, (Tensor, Tensor_)):
        raise TypeError("For scatter_tensor, the output tensor must be tensor")
    if not isinstance(src, int):
        raise TypeError("For scatter_tensor, the src must be int")
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if not isinstance(async_op, bool):
        raise TypeError(
            f"The argument 'async_op' must be a bool, but got {type(async_op)}."
        )
    src = get_group_rank_from_world_rank(src, group)
    rank_size = get_group_size(group)
    rank_id = get_rank(group)
    output = dist_comm_scatter_tensor_op(
        output_tensor, input_tensor, rank_size, src, rank_id, group
    )
    _, handle = _deal_comm_outputs(output, async_op)
    return handle


def gather_into_tensor(output_tensor, input_tensor, dst=0, group=None, async_op=False):
    r"""
    Gathers tensors from the specified communication group. The operation will gather the tensor
    from processes according to dimension 0.

    Note:
        - Only the tensor in process `dst` (global rank) will keep the gathered tensor. The other process
            will keep a tensor with shape [1], which has no mathematical meaning.
        - Only support PyNative mode, Graph mode is not currently supported.

    Args:
        output_tensor (Tensor):  Output tensor to accommodate tensor elements from all ranks.
        input_tensor (Tensor): The tensor to be gathered. The shape of tensor is :math:`(x_1, x_2, ..., x_R)`.
            the input tensors in this API must have the same size across all ranks.
        dst(int, optional): Specifies the rank(global rank) of the process that receive the tensor.
            And only process `dst` will receive the gathered tensor. Default: 0.
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        async_op (bool, optional): Whether this operator should be an async operator. Default: ``False`` .

    Returns:
        CommHandle, CommHandle is an async work handle, if `async_op` is set to True.
        CommHandle will be None, when `async_op` is False.

    Raise:
        TypeError: If the type of the `input_tensor` or `output_tensor` parameter is not Tensor,
            or any of `op` and `group` is not a str.
        RuntimeError: If device target is invalid, or backend is invalid, or distributed initialization fails.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> import numpy as np
        >>> import mindspore as ms
        >>> import mindspore.nn as nn
        >>> from mindspore.mint.distributed import init_process_group
        >>> from mindspore import Tensor
        >>> from mindspore.communication.comm_func import gather_into_tensor
        >>> # Launch 2 processes.
        >>>
        >>> init_process_group()
        >>> input = Tensor(np.arange(4).reshape([2, 2]).astype(np.float32))
        >>> output = Tensor(np.zeros([4, 2]).astype(np.float32))
        >>> handle = gather_into_tensor(output, input, dst=0)
        >>> print(output)
        Process with rank 0: [[0. 1.],
                              [2. 3.],
                              [0. 1.],
                              [2. 3.]]
        Process with rank 1:  [[0. 0.],
                              [0. 0.],
                              [0. 0.],
                              [0. 0.]]
    """
    if not isinstance(input_tensor, (Tensor, Tensor_)):
        raise TypeError("For gather_into_tensor, the input tensor must be tensor")
    if not isinstance(output_tensor, (Tensor, Tensor_)):
        raise TypeError("For gather_into_tensor, the output tensor must be tensor")
    if not isinstance(dst, int):
        raise TypeError("For gather_into_tensor, the dst must be int")
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if not isinstance(async_op, bool):
        raise TypeError(
            f"The argument 'async_op' must be a bool, but got {type(async_op)}."
        )
    group_size = get_group_size(group)
    dst = get_group_rank_from_world_rank(dst, group)
    rank_id = get_rank(group)
    output = dist_comm_gather_into_tensor_op(
        output_tensor, input_tensor, group_size, dst, rank_id, group
    )
    _, handle = _deal_comm_outputs(output, async_op)
    return handle


def broadcast(tensor, src, group=None, async_op=False):
    """
    Broadcasts the tensor to the whole group.

    Note:
        - The tensors must have the same shape and format in all processes of the collection.
        - Only support PyNative mode, Graph mode is not currently supported.

    Args:
        tensor (Tensor): Data to be sent if src is the rank of current process,
            and tensor to be used to save received data otherwise.
        src (int): Specifies the rank(global rank) of the process that broadcast the tensor.
            And only process `src` will broadcast the tensor.
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        async_op (bool, optional): Whether this operator should be an async operator. Default: ``False`` .

    Returns:
        CommHandle, CommHandle is an async work handle, if `async_op` is set to True.
        CommHandle will be None, when `async_op` is False.

    Raises:
        TypeError: If the type of the `tensor` parameter is not Tensor, `src` is not an integer,
            `group` is not a string or `async_op` is not bool.
        RuntimeError: If device target is invalid, or backend is invalid, or distributed initialization fails.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> import mindspore as ms
        >>> from mindspore import Tensor
        >>> from mindspore.mint.distributed import init_process_group, broadcast
        >>> import numpy as np
        >>> # Launch 2 processes.
        >>>
        >>> init_process_group()
        >>> data = ms.Tensor(np.arange(8).reshape([2, 4]).astype(np.float32))
        >>> handle = broadcast(tensor=data, src=0)
        >>> print(data)
        [[0. 1. 2. 3.]
         [4. 5. 6. 7.]]

    Tutorial Examples:
        - `Distributed Set Communication Primitives - Broadcast
          <https://www.mindspore.cn/docs/en/master/api_python/samples/ops/communicate_ops.html#broadcast>`_

    """
    if not isinstance(tensor, (Tensor, Tensor_)):
        raise TypeError("For broadcast, the input tensor must be tensor")
    if not isinstance(src, int):
        raise TypeError("For broadcast, the src must be int")
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if not isinstance(async_op, bool):
        raise TypeError(
            f"The argument 'async_op' must be a bool, but got {type(async_op)}."
        )
    rank = get_group_rank_from_world_rank(src, group)
    output = dist_comm_broadcast_op(tensor, rank, group)
    _, handle = _deal_comm_outputs(output, async_op)
    return handle


def barrier(group=None, async_op=False, device_ids=None):
    """
    Synchronizes all processes in the specified group. Once the process call this operation, it will be blocked until
    all processes call this operation. After all processes finish calling the operations, the blocked processes
    will be woken and continue their task.

    Args:
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        async_op (bool, optional): Whether this operator should be an async operator. Default: ``False`` .
        device_ids (list[int], optional): Currently It is a reserved Parameter.

    Returns:
        CommHandle, CommHandle is an async work handle, if `async_op` is set to True.
        CommHandle will be None, when `async_op` is False.

    Raises:
        TypeError: `group` is not a str or `async_op` is not a bool.
        RuntimeError: If backend is invalid, or distributed initialization fails.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> from mindspore.mint.distributed import init_process_group
        >>> from mindspore.communication.comm_func import barrier
        >>> # Launch 2 processes.
        >>> init_process_group()
        >>> barrier()

    Tutorial Examples:
        - `Distributed Set Communication Primitives - Barrier
          <https://www.mindspore.cn/docs/en/master/api_python/samples/ops/communicate_ops.html#barrier>`_
    """
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if not isinstance(async_op, bool):
        raise TypeError(
            f"The argument 'async_op' must be a bool, but got {type(async_op)}."
        )
    output = dist_comm_barrier_op(group)
    _, handle = _deal_comm_outputs(output, async_op, True)
    return handle


def send(tensor, dst=0, group=None, tag=0):
    """
    Send tensors to the specified dest_rank.

    Note:
        - Send and Receive must be used in combination and have same tag.
        - Only support PyNative mode, Graph mode is not currently supported.

    Args:
        tensor (Tensor): Tensor to send.
        dst (int, optional): A required integer identifying the destination rank(global rank). Default: 0.
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        tag (int, optional): A required integer identifying the send/recv message tag. The message will
            be received by the Receive op with the same "tag". Default: 0. It is a reserved parameter currently.

    Raises:
        TypeError: If the `tensor` is not Tensor, `dst` is not an int or `group` is not a str.
        ValueError: If the `dst` process rank id is same as the current process.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> from mindspore import ops
        >>> import mindspore.nn as nn
        >>> from mindspore.mint.distributed import init_process_group
        >>> from mindspore.mint.distributed import send
        >>> from mindspore import Tensor
        >>> import numpy as np
        >>>
        >>> init_process_group()
        >>> input_ = Tensor(np.ones([2, 8]).astype(np.float32))
        >>> send(input_, 0)
    """
    if not isinstance(tensor, (Tensor, Tensor_)):
        raise TypeError("For send, the input tensor must be tensor")
    if not isinstance(dst, int):
        raise TypeError("For send, the dst must be int")
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if get_rank() == dst:
        raise ValueError(
            "Invalid destination rank: destination rank should not be the same as "
            "the rank of the current process."
        )
    _dst = _get_group_rank_from_world_rank_from_cache_helper(dst, group)
    output = dist_comm_isend_op(tensor, _dst, group, tag)
    _deal_comm_outputs(output, False)



def recv(tensor, src=0, group=None, tag=0):
    """
    Receive tensors from src.

    Note:
        - Send and Receive must be used in combination and have same tag.
        - Only support PyNative mode, Graph mode is not currently supported.

    Args:
        tensor (Tensor): Tensor to fill with received data.
        src (int, optional): A required integer identifying the source rank(global rank). Default: ``0``.
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        tag (int, optional): A required integer identifying the send/recv message tag. The message will
            be received by the Send op with the same "tag". Default: 0. It is a reserved parameter currently.

    Returns:
        int, If success, return ``0``.

    Raises:
        TypeError: If the `tensor` is not Tensor, `src` is not an int or `group` is not a str.
        ValueError: If the rank ID of the process is greater than the rank size of the communication group.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> from mindspore import ops
        >>> import mindspore.nn as nn
        >>> from mindspore.mint.distributed import init_process_group
        >>> from mindspore.mint.distributed import recv
        >>> from mindspore import Tensor
        >>> import numpy as np
        >>>
        # Launch 2 processes.
        Process 0 send the following array to Process 1
        [[ 0.  1.]
         [ 2.  3.]]
        >>> init_process_group()
        >>> x = ms.Tensor(np.zeros([2, 2]))
        # Process 1 receive tensor from Process 0.
        >>> out = recv(x, src=0)
        >>> print(out)
        [[ 0.  1.]
         [ 2.  3.]]
    """
    if not isinstance(tensor, (Tensor, Tensor_)):
        raise TypeError("For recv, the input tensor must be tensor")
    if not isinstance(src, int):
        raise TypeError("For recv, the src must be int")
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    _src = _get_group_rank_from_world_rank_from_cache_helper(src, group)
    _deal_comm_outputs(
        dist_comm_irecv_op(tensor, tag, _src, group), False
    )
    return 0


def isend(tensor, dst=0, group=None, tag=0):
    """
    Send tensors to the specified dest_rank asynchronously.

    Note:
        - Send and Receive must be used in combination and have same tag.
        - Only support PyNative mode, Graph mode is not currently supported.

    Args:
        tensor (Tensor): Tensor to send.
        dst (int, optional): A required integer identifying the destination rank(global rank). Default: 0.
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        tag (int, optional): A required integer identifying the send/recv message tag. The message will
            be received by the Receive op with the same "tag". Default: 0. It is a reserved parameter currently.

    Returns:
        CommHandle, it is an async work handle.

    Raises:
        TypeError: If the `tensor` is not Tensor, `dst` is not an int or `group` is not a str.
        ValueError: If the `dst` process rank id is same as the current process.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> from mindspore import ops
        >>> import mindspore.nn as nn
        >>> from mindspore.mint.distributed import init_process_group
        >>> from mindspore.mint.distributed import isend
        >>> from mindspore import Tensor
        >>> import numpy as np
        >>>
        >>> init_process_group()
        >>> input_ = Tensor(np.ones([2, 8]).astype(np.float32))
        >>> handle = isend(input_, 0)
        >>> handle.wait()
    """
    if not isinstance(tensor, (Tensor, Tensor_)):
        raise TypeError("For isend, the input tensor must be tensor")
    if not isinstance(dst, int):
        raise TypeError("For isend, the dst must be int")
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if get_rank() == dst:
        raise ValueError(
            "Invalid destination rank: destination rank should not be the same as "
            "the rank of the current process."
        )
    _dst = _get_group_rank_from_world_rank_from_cache_helper(dst, group)
    output = dist_comm_isend_op(tensor, _dst, group, tag)
    _, handle = _deal_comm_outputs(output, True)
    return handle


def irecv(tensor, src=0, group=None, tag=0):
    """
    Receive tensors from src asynchronously.

    Note:
        - Send and Receive must be used in combination and have same tag.
        - Only support PyNative mode, Graph mode is not currently supported.

    Args:
        tensor (Tensor): Tensor to fill with received data.
        src (int, optional): A required integer identifying the source rank(global rank). Default: ``0``.
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        tag (int, optional): A required integer identifying the send/recv message tag. The message will
            be received by the Send op with the same "tag". Default: ``0``. It is a reserved parameter currently.

    Returns:
        CommHandle, CommHandle is an async work handle, if `async_op` is set to True.
        CommHandle will be None, when `async_op` is False.

    Raises:
        TypeError: If the type of `tensor` is not Tensor, If `src` is not an int or `group` is not a str.
        ValueError: If the rank ID of the process is greater than the rank size of the communication group.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> from mindspore import ops
        >>> import mindspore.nn as nn
        >>> from mindspore.mint.distributed import init_process_group
        >>> from mindspore.mint.distributed import irecv
        >>> from mindspore import Tensor
        >>> import numpy as np
        >>>
        # Launch 2 processes.
        Process 0 send the following array to Process 1
        [[ 0.  1.]
         [ 2.  3.]]
        >>> init_process_group()
        >>> x = ms.Tensor(np.zeros([2, 2]))
        # Process 1 receive tensor from Process 0.
        >>> handle = irecv(x, src=0)
        >>> handle.wait()
        >>> print(x)
        [[ 0.  1.]
         [ 2.  3.]]
    """
    if not isinstance(tensor, (Tensor, Tensor_)):
        raise TypeError("For irecv, the input tensor must be tensor")
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if not isinstance(src, int):
        raise TypeError("For irecv, the src must be int")
    _src = _get_group_rank_from_world_rank_from_cache_helper(src, group)
    output = dist_comm_irecv_op(tensor, tag, _src, group)
    _, handle = _deal_comm_outputs(output, True)
    return handle


def all_to_all(output_tensor_list, input_tensor_list, group=None, async_op=False):
    """
    scatter and gather list of tensor to/from all rank according to input/output tensor list.

    Note:
        - tensor shape in `output_shape_list` and `input_tensor_list` should be match across ranks.
        - Only support PyNative mode, Graph mode is not currently supported.

    Args:
        output_tensor_list (List[Tensor]): List of tensors that indicate the gathered from remote ranks.
        input_tensor_list (List[Tensor]): List of tensors to scatter to the remote rank.
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        async_op (bool, optional): Whether this operator should be an async operator. Default: ``False`` .

    Returns:
        CommHandle, CommHandle is an async work handle, if `async_op` is set to True.
        CommHandle will be None, when `async_op` is False.

    Raises:
        TypeError: If not all elements in `input_tensor_list` or `output_tensor_list` are Tensor.
        TypeError: If tensors in `input_tensor_list` or `output_tensor_list` are not the same type.
        TypeError: If `group` is not str or `async_op` is not bool.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> import numpy as np
        >>> import mindspore
        >>> from mindspore.mint.distributed import init_process_group, get_rank
        >>> from mindspore.mint.distributed import all_to_all
        >>> from mindspore import Tensor
        >>> from mindspore.ops import zeros
        >>>
        >>> init_process_group()
        >>> this_rank = get_rank()
        >>> if this_rank == 0:
        >>>     send_tensor_list = [Tensor(1.), Tensor([[2, 3], [4, 5.]])]
        >>>     recv_tensor_list = [Tensor((0), dtype=ms.float32), Tensor([0, 0.])]
        >>> if this_rank == 1:
        >>>     send_tensor_list = [Tensor([2, 2.]), Tensor([4, 5, 6, 7.])]
        >>>     recv_tensor_list = [Tensor([[0, 0.],[0, 0]]), Tensor([0, 0, 0, 0.])]
        >>> handle = all_to_all(recv_tensor_list, send_tensor_list)
        >>> print(recv_tensor_list)
        rank 0:
        (Tensor(shape=[], dtype=Float32, value= 1),
         Tensor(shape=[2], dtype=Float32, value= [2.00000000e+00, 2.00000000e+00]))
        rank 1:
        (Tensor(shape=[2, 2], dtype=Float32, value=
        [[2.00000000e+00, 3.00000000e+00],
         [4.00000000e+00, 5.00000000e+00]]),
         Tensor(shape=[4], dtype=Float32, value=[4.00000000e+00, 5.00000000e+00, 6.00000000e+00, 7.00000000e+00]))

    """
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if not isinstance(async_op, bool):
        raise TypeError(
            f"The argument 'async_op' must be a bool, but got {type(async_op)}."
        )

    _check_all_tensors(input_tensor_list)
    _check_all_tensors(output_tensor_list)
    _check_all_tensor_same_dtype(input_tensor_list)
    _check_all_tensor_same_dtype(output_tensor_list)
    send_numel_list = []
    send_flatten_tensor = []
    recv_numel_list = []
    recv_shape_list = []

    for tensor in input_tensor_list:
        send_numel_list.append(tensor.size)
        send_flatten_tensor.append(tensor.reshape(-1))
    for tensor in output_tensor_list:
        recv_numel_list.append(tensor.size)
        recv_shape_list.append(tensor.shape)

    send_flatten_tensor = cat(send_flatten_tensor)
    send_flatten_tensor = _contiguous(send_flatten_tensor)

    rank_size = get_group_size(group)
    output = dist_comm_all_to_all_v_op(
        output_tensor_list,
        send_flatten_tensor,
        group,
        send_numel_list,
        recv_numel_list,
        rank_size,
    )
    _, handle = _deal_comm_outputs(output, async_op)
    return handle


def _get_all_to_all_single_numel_list(tensor, output, output_split_sizes,
                                      input_split_sizes, group):
    """get numel list for all_to_all_single."""
    if _is_split_sizes_empty(input_split_sizes):
        _world_size = get_group_size(group)
        if tensor.shape[0] % _world_size != 0:
            raise ValueError(
                "input shape at dim 0 must be divided by world_size, "
                f"but got {tensor.shape[0]} and {_world_size}."
            )
        _split_size = tensor.shape[0] // _world_size
        input_split_sizes = (_split_size,) * _world_size
    if _is_split_sizes_empty(output_split_sizes):
        _world_size = get_group_size(group)
        shape_dim_0 = output.shape[0]

        if shape_dim_0 % _world_size != 0:
            raise ValueError(
                "output shape at dim 0 must be divided by world_size, "
                f"but got {shape_dim_0} and {_world_size}."
            )
        _split_size = shape_dim_0 // _world_size
        output_split_sizes = (_split_size,) * _world_size

    send_size_without_first_dim = _get_size(tensor.shape[1:])
    send_numel_list = [size * send_size_without_first_dim for size in input_split_sizes]

    recv_shape_without_first_dim = output.shape[1:]
    recv_size_without_first_dim = _get_size(recv_shape_without_first_dim)
    recv_numel_list = [
        size * recv_size_without_first_dim for size in output_split_sizes
    ]
    return send_numel_list, recv_numel_list, recv_shape_without_first_dim


def all_to_all_single(output,
                      input,
                      output_split_sizes=None,
                      input_split_sizes=None,
                      group=None,
                      async_op=False):
    """
    scatter and gather input with split size to/from all rank, and return result in a single tensor.

    Note:
        - 'output' and 'tensor' shape should be match across ranks.
        - Only support PyNative mode, Graph mode is not currently supported.

    Args:
        output (Tensor): the output tensor is gathered concatenated from remote ranks.
        input (Tensor): tensor to be scattered to remote rank.
        output_split_sizes (Union(Tuple(int), List(int)), optional): output split size at dim 0. If set to None,
            it means equally split by ``world_size``. Default: ``None``.
        input_split_sizes (Union(Tuple(int), List(int)), optional): input split size at dim 0. If set to None,
            it means equally split by ``world_size``. Default: ``None``.
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        async_op (bool, optional): Whether this operator should be an async operator. Default: ``False`` .

    Returns:
        CommHandle, CommHandle is an async work handle, if `async_op` is set to True.
        CommHandle will be None, when `async_op` is False.

    Raises:
        TypeError: If `input` or `output` is not tensor. `group` is not a str, or async_op is not bool.
        ValueError: When `input_split_sizes` is empty, input dim 0 can not be divided by ``world_size``.
        ValueError: When `output_split_sizes` is empty, output dim 0 can not be divided by ``world_size``.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> import numpy as np
        >>> import mindspore
        >>> from mindspore.mint.distributed import init_process_group, get_rank
        >>> from mindspore.mint.distributed import all_to_all_single
        >>> from mindspore import Tensor
        >>> from mindspore.ops import zeros
        >>>
        >>> init_process_group()
        >>> this_rank = get_rank()
        >>> if this_rank == 0:
        >>>     output = Tensor(np.zeros([3, 3]).astype(np.float32))
        >>>     tensor = Tensor([[0, 1, 2.], [3, 4, 5], [6, 7, 8]])
        >>>     result = all_to_all_single(output, tensor, [2, 1], [2, 1])
        >>>     print(output)
        >>> if this_rank == 1:
        >>>     output = Tensor(np.zeros([3, 3]).astype(np.float32))
        >>>     tensor = Tensor([[9, 10., 11], [12, 13, 14]])
        >>>     result = all_to_all_single(output, tensor)
        >>>     print(output)
        rank 0:
        [[ 0.  1.  2.]
         [ 3.  4.  5.]
         [ 9. 10. 11.]]
        rank 1:
        [[ 6.  7.  8.]
         [12. 13. 14.]]

    """

    _check_all_tensors([input])
    _check_all_tensors([output])
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if not isinstance(async_op, bool):
        raise TypeError(
            f"The argument 'async_op' must be a bool, but got {type(async_op)}."
        )
    split_sizes_empty = _is_split_sizes_empty(output_split_sizes) and _is_split_sizes_empty(input_split_sizes)
    send_numel_list, recv_numel_list, _ = \
        _get_all_to_all_single_numel_list(input, output, output_split_sizes, input_split_sizes, group)
    _input = input.reshape(-1)
    rank_size = get_group_size(group)
    result = dist_comm_all_to_all_v_single_op(
        output,
        _input,
        group,
        send_numel_list,
        recv_numel_list,
        rank_size,
        split_sizes_empty,
    )
    _, handle = _deal_comm_outputs(result, async_op)
    return handle


def _check_tensor_list(tensor_list, tensor, group_size):
    """check all elements in tensor_list are type of Tensor or tuple or list"""
    if not tensor_list or len(tensor_list) != group_size:
        raise TypeError(
            f"The argument list tensor len must be equal to group rank size, but got {len(tensor_list)}."
        )
    if tensor.dtype != tensor_list[0].dtype:
        raise TypeError(
            f"The argument list tensor type must be equal to tensor type, but got {tensor_list[0].dtype}."
        )
    if tensor.shape != tensor_list[0].shape:
        raise TypeError(
            f"The argument list tensor shape must be equal to tensor shape, but got {tensor_list[0].shape}."
        )


def all_gather(tensor_list, tensor, group=None, async_op=False):
    """
    Gathers tensors from the specified communication group and returns the tensor which is all gathered.

    Note:
        The tensors must have the same shape and format in all processes of the collection.

    Args:
        tensor_list (list[Tensor]): Output list.
        tensor (Tensor): The input tensor to be all gathered into tensor.
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        async_op (bool, optional): Whether this operator should be an async operator. Default: ``False`` .

    Returns:
        CommHandle,  CommHandle is an async work handle, if `async_op` is set to True.
        CommHandle will be None, when `async_op` is False.

    Raises:
        TypeError: If the type of input `tensor` is not Tensor, `tensor_list` is not Tensor List,
            `group` is not a str or async_op is not bool.
        TypeError: If size of `tensor_list` is not equal to group size。
        TypeError: If the type or shape of `tensor` not equal to the member of `tensor_list`。
        RuntimeError: If device target is invalid, or backend is invalid, or distributed initialization fails.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> import numpy as np
        >>> import mindspore as ms
        >>> from mindspore import ops
        >>> from mindspore.mint.distributed import init_process_group
        >>> from mindspore.mint.distributed import all_gather
        >>> from mindspore import Tensor
        >>>
        >>> ms.set_context(mode=ms.GRAPH_MODE)
        >>> init_process_group()
        >>> input_tensor = Tensor(np.ones([2, 8]).astype(np.float32))
        >>> out_tensors = [Tensor(np.zeros([2, 8]).astype(np.float32)), Tensor(np.zeros([2, 8]).astype(np.float32))]
        >>> output = all_gather(out_tensors, input_tensor)
        >>> print(out_tensors)
        [Tensor(shape=[2, 8], dtype=Float32, value=
        [[ 1.00000000e+00,  1.00000000e+00,  1.00000000e+00 ...  1.00000000e+00,  1.00000000e+00,  1.00000000e+00],
         [ 1.00000000e+00,  1.00000000e+00,  1.00000000e+00 ...  1.00000000e+00,  1.00000000e+00,  1.00000000e+00]]),
        Tensor(shape=[2, 8], dtype=Float32, value=
        [[ 1.00000000e+00,  1.00000000e+00,  1.00000000e+00 ...  1.00000000e+00,  1.00000000e+00,  1.00000000e+00],
         [ 1.00000000e+00,  1.00000000e+00,  1.00000000e+00 ...  1.00000000e+00,  1.00000000e+00,  1.00000000e+00]])]


    """
    _check_all_tensors(tensor_list)
    _check_all_tensor_same_dtype_and_shape(tensor_list)
    if not isinstance(tensor, (Tensor, Tensor_)):
        raise TypeError("For all_gather_into_tensor, the input tensor must be tensor")
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if not isinstance(async_op, bool):
        raise TypeError(
            f"The argument 'async_op' must be a bool, but got {type(async_op)}."
        )
    group_size = get_group_size(group)
    _check_tensor_list(tensor_list, tensor, group_size)
    result = dist_comm_all_gather_op(tensor_list, tensor, group_size, group)
    _, handle = _deal_comm_outputs(result, async_op)
    return handle


def reduce_scatter(output, input_list, op=ReduceOp.SUM, group=None, async_op=False):
    r"""
    Reduces and scatters tensors from the specified communication group and
    returns the tensor which is reduced and scattered.

    Note:
        The tensors must have the same shape and format in all processes of the collection.

    Args:
        output (Tensor): the output tensor.
        input_list (list[Tensor]): List of tensors to reduce and scatter.
        op (str, optional): Specifies an operation used for element-wise reductions,
            like SUM and MAX. Default: ``ReduceOp.SUM`` .
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        async_op (bool, optional): Whether this operator should be an async operator. Default: ``False`` .

    Returns:
        CommHandle, CommHandle is an async work handle, if `async_op` is set to True.
        CommHandle will be None, when `async_op` is False.

    Raises:
        TypeError: If the type of `output` parameter is not Tensor, `input_list` is not Tensor List.
        TypeError: If any of `op` and `group` is not a str. async_op is not bool or 'op' is invalid.
        TypeError: If size of `input_list` is not equal to group size。
        TypeError: If the type or shape of `output` not equal to the member of `input_list`。
        RuntimeError: If device target is invalid, or backend is invalid, or distributed initialization fails.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> import mindspore as ms
        >>> from mindspore import Tensor
        >>> from mindspore.mint.distributed import init_process_group
        >>> from mindspore.mint.distributed import reduce_scatter
        >>> import numpy as np
        >>>
        >>> ms.set_context(mode=ms.GRAPH_MODE)
        >>> init_process_group()
        >>> input_tensors = [Tensor(np.ones([4, 8]).astype(np.float32)), Tensor(np.ones([4, 8]).astype(np.float32))]
        >>> output_tensor = Tensor(np.zeros([4, 8]).astype(np.float32))
        >>> output = reduce_scatter(output_tensor ,input_tensors)
        >>> print(output_tensor)
        [[2. 2. 2. 2. 2. 2. 2. 2.]
         [2. 2. 2. 2. 2. 2. 2. 2.]
         [2. 2. 2. 2. 2. 2. 2. 2.]
         [2. 2. 2. 2. 2. 2. 2. 2.]]

    """

    _check_all_tensors(input_list)
    _check_all_tensor_same_dtype_and_shape(input_list)
    if not isinstance(output, (Tensor, Tensor_)):
        raise TypeError("For reduce_scatter, the output tensor must be tensor")
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if not isinstance(async_op, bool):
        raise TypeError(
            f"The argument 'async_op' must be a bool, but got {type(async_op)}."
        )
    if not isinstance(op, str):
        raise TypeError("For reduce_scatter, the input op type must be str")
    if op not in ("sum", "prod", "min", "max"):
        raise TypeError(
            "For reduce_scatter, the input op value must be one of sum, prod, min, max"
        )
    rank_size = get_group_size(group)
    _check_tensor_list(input_list, output, rank_size)
    result = dist_comm_reduce_scatter_op(output, input_list, rank_size, op, group)
    _, handle = _deal_comm_outputs(result, async_op)
    return handle


def scatter(tensor, scatter_list, src=0, group=None, async_op=False):
    r"""
    Scatter tensor evently across the processes in the specified communication group.

    Note:
        - The interface behavior only support Tensor List input and scatter evenly.
        - Only the tensor in process `src` (global rank) will do scatter.
        - Only support PyNative mode, Graph mode is not currently supported.

    Args:
        tensor (Tensor): the output tensor.
        scatter_list (list[Tensor]): List of same-sized tensors to scatter.
            default is None, must be specified on the source rank.
        src (int, optional): Specifies the rank(global rank) of the process that send the tensor.
            And only process `src` will send the tensor.
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        async_op (bool, optional): Whether this operator should be an async operator. Default: ``False`` .

    Returns:
        CommHandle, CommHandle is an async work handle, if `async_op` is set to True.
        CommHandle will be None, when `async_op` is False.

    Raise:
        TypeError: If the type of `tensor` parameter is not Tensor, `scatter_list` is not Tensor List.
        TypeError: If any of `op` and `group` is not a str. async_op is not bool or 'op' is invalid.
        TypeError: If size of `scatter_list` is not equal to group size。
        TypeError: If the type or shape of `tensor` not equal to the member of `scatter_list`。
        RuntimeError: If device target is invalid, or backend is invalid, or distributed initialization fails.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> import mindspore as ms
        >>> from mindspore.mint.distributed import init_process_group, scatter
        >>> import numpy as np
        >>> # Launch 2 processes.
        >>>
        >>> init_process_group()
        >>> inputs = [Tensor(np.arange(4).reshape([2.0, 2])), Tensor(np.arange(4).reshape([2, 2.0]))]
        >>> output = Tensor(np.zeros([2, 2]).astype(np.float32))
        >>> scatter(output, inputs, src=0)
        >>> print(output)
        # rank_0
        [[0. 1.]
         [2. 3.]]
        # rank_1
        [[0. 1.]
         [2. 3.]]
    """
    _check_all_tensors(scatter_list)
    _check_all_tensor_same_dtype_and_shape(scatter_list)
    if not isinstance(tensor, (Tensor, Tensor_)):
        raise TypeError("For scatter_tensor, the output tensor must be tensor")
    if not isinstance(src, int):
        raise TypeError("For scatter_tensor, the src must be int")
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if not isinstance(async_op, bool):
        raise TypeError(
            f"The argument 'async_op' must be a bool, but got {type(async_op)}."
        )
    src = get_group_rank_from_world_rank(src, group)
    rank_size = get_group_size(group)
    rank_id = get_rank(group)
    if src == rank_id:
        _check_tensor_list(scatter_list, tensor, rank_size)
    output = dist_comm_scatter_op(tensor, scatter_list, rank_size, src, rank_id, group)
    _, handle = _deal_comm_outputs(output, async_op)
    return handle


def gather(tensor, gather_list, dst=0, group=None, async_op=False):
    r"""
    Gathers tensors from the specified communication group. The operation will gather the tensor
    from processes according to dimension 0.

    Note:
        - Only the tensor in process `dst` (global rank) will keep the gathered tensor. The other process
          will keep a tensor list which has no mathematical meaning.
        - The tensors must have the same shape and format in all processes of the collection.
        - Only support PyNative mode, Graph mode is not currently supported.

    Args:
        tensor (Tensor): The tensor to be gathered.
        gather_list (list[Tensor]): List of same-sized tensors to use for gathered data.
        dst (int, optional): Specifies the rank(global rank) of the process that receive the tensor.
            And only process `dst` will receive the gathered tensor. Default: ``0`` .
        group (str, optional): The communication group to work on. If ``None``, which means ``"hccl_world_group"`` in
            Ascend. Default: ``None``.
        async_op (bool, optional): Whether this operator should be an async operator. Default: ``False`` .

    Returns:
        CommHandle, CommHandle is an async work handle, if `async_op` is set to True.
        CommHandle will be None, when `async_op` is False.

    Raise:
        TypeError: If the type of input tensor is not Tensor, or gather_list is not Tensor list.
        TypeError: If dst is not an integer, group is not a string or async_op is not bool.
        TypeError: If size of `gather_list` is not equal to group size。
        TypeError: If the type or shape of `tensor` not equal to the member of `gather_list`。
        RuntimeError: If device target is invalid, or backend is invalid, or distributed initialization fails.

    Supported Platforms:
        ``Ascend``

    Examples:
        .. note::
            Before running the following examples, you need to configure the communication environment variables.

            For Ascend devices, it is recommended to use the msrun startup method
            without any third-party or configuration file dependencies.
            Please see the `msrun start up
            <https://www.mindspore.cn/docs/en/master/model_train/parallel/msrun_launcher.html>`_
            for more details.

            This example should be run with 2 devices.

        >>> import numpy as np
        >>> import mindspore as ms
        >>> import mindspore.nn as nn
        >>> from mindspore.mint.distributed import init_process_group, gather
        >>> from mindspore import Tensor
        >>> # Launch 2 processes.
        >>> init_process_group()
        >>> input = Tensor(np.arange(4).reshape([2, 2]).astype(np.float32))
        >>> outputs = [Tensor(np.zeros([2, 2]).astype(np.float32)),Tensor(np.zeros([2, 2]).astype(np.float32))]
        >>> gather(input, outputs, dst=0)
        >>> print(outputs)
        # rank_0
        [Tensor(shape=[2, 2], dtype=Float32, value=
        [[ 0.00000000e+00,  1.00000000e+00],
         [ 2.00000000e+00,  3.00000000e+00]]), Tensor(shape=[2, 2], dtype=Float32, value=
        [[ 0.00000000e+00,  1.00000000e+00], [ 2.00000000e+00,  3.00000000e+00]])]
        [Tensor(shape=[2, 2], dtype=Float32, value=
        [[ 0.00000000e+00,  1.00000000e+00],
         [ 2.00000000e+00,  3.00000000e+00]]), Tensor(shape=[2, 2], dtype=Float32, value=
        [[ 0.00000000e+00,  1.00000000e+00], [ 2.00000000e+00,  3.00000000e+00]])]
        # rank_1
        [Tensor(shape=[2, 2], dtype=Float32, value=
        [[ 0.00000000e+00,  0.00000000e+00],
         [ 0.00000000e+00,  0.00000000e+00]]), Tensor(shape=[2, 2], dtype=Float32, value=
        [[ 0.00000000e+00,  0.00000000e+00], [ 0.00000000e+00,  0.00000000e+00]])]
        [Tensor(shape=[2, 2], dtype=Float32, value=
        [[ 0.00000000e+00,  0.00000000e+00],
         [ 0.00000000e+00,  0.00000000e+00]]), Tensor(shape=[2, 2], dtype=Float32, value=
        [[ 0.00000000e+00,  0.00000000e+00], [ 0.00000000e+00,  0.00000000e+00]])]
    """
    if not isinstance(tensor, (Tensor, Tensor_)):
        raise TypeError("For gather, the input tensor must be tensor")
    _check_all_tensors(gather_list)
    _check_all_tensor_same_dtype_and_shape(gather_list)
    if not isinstance(dst, int):
        raise TypeError("For gather, the dst must be int")
    if group is None:
        group = GlobalComm.WORLD_COMM_GROUP
    if not isinstance(group, str):
        raise TypeError(
            "The argument 'group' must be type of string, "
            "but got 'group' type : {}.".format(type(group))
        )
    if not isinstance(async_op, bool):
        raise TypeError(f"The argument 'async_op' must be a bool, but got {type(async_op)}.")
    group_size = get_group_size(group)
    dst = get_group_rank_from_world_rank(dst, group)
    rank_id = get_rank(group)
    if dst == rank_id:
        _check_tensor_list(gather_list, tensor, group_size)
    output = dist_comm_gather_op(tensor, gather_list, group_size, dst, rank_id, group)
    _, handle = _deal_comm_outputs(output, async_op)
    return handle

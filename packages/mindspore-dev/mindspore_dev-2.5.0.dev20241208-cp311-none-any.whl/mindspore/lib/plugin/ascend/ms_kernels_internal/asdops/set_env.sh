#!/bin/bash
# 
# Copyright (c) 2024 Huawei Technologies Co., Ltd.
# AscendOpCommonLib is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
# 
path="${BASH_SOURCE[0]}"
if [[ -f "$path" ]] && [[ "$path" =~ 'set_env.sh' ]];then
    asd_path=$(cd $(dirname $path); pwd )
    export MS_ASDOPS_HOME_PATH="${asd_path}"
    export ASDOPS_OPS_PATH=$MS_ASDOPS_HOME_PATH/ops
    export LD_LIBRARY_PATH=$MS_ASDOPS_HOME_PATH/lib:$MS_ASDOPS_HOME_PATH/host:$LD_LIBRARY_PATH
    export PATH=$MS_ASDOPS_HOME_PATH/bin:$PATH

    export PYTORCH_INSTALL_PATH="$(python3 -c 'import torch, os; print(os.path.dirname(os.path.abspath(torch.__file__)))')"
    export LD_LIBRARY_PATH=$PYTORCH_INSTALL_PATH/lib:$LD_LIBRARY_PATH
    export ASDOPS_LOG_TO_STDOUT=0
    export ASDOPS_LOG_LEVEL=INFO
    export ASDOPS_LOG_TO_FILE=0
    export ASDOPS_LOG_TO_FILE_FLUSH=0
    export ASDOPS_LOG_TO_BOOST_TYPE=atb #算子库对应加速库日志类型，默认transformer
    export ASDOPS_LOG_PATH=~
else
    echo "There is no 'set_env.sh' to import"
fi

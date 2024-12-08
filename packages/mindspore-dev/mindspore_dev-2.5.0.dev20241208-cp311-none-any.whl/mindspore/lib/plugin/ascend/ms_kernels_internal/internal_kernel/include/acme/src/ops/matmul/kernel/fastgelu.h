/**
 * Copyright 2024 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "kernel_operator.h"

template <typename T>
__aicore__ inline void FastGelu(AscendC::LocalTensor<T> &src, AscendC::LocalTensor<T> &tmp, int elements ) {
const T factor1 = 0.851;
const T addition = 1.;
const T factor2 = -1.702;
auto tmp1 = tmp[elements];
Abs(tmp1,src,elements);        //abs(x)
pipe_barrier(PIPE_V);
Sub(tmp,src,tmp1,elements);    // x-abs(x)
pipe_barrier(PIPE_V);
Muls(tmp,tmp,factor1,elements); // 0.851 *(x-abs(x))
pipe_barrier(PIPE_V);
Exp(tmp,tmp,elements);      // e^( 0.851 *(x-abs(x)))
pipe_barrier(PIPE_V);
Mul(tmp,src,tmp,elements);  //x*e^(0.851*(x-abs(x))
Muls(tmp1,tmp1,factor2,elements); // -1.702 *abs(x)
pipe_barrier(PIPE_V);
Exp(tmp1,tmp1,elements); // e^(-1.702*abs(x))
pipe_barrier(PIPE_V);
Adds(tmp1,tmp1,addition,elements); // 1+e^(-1.702*abs(x))
pipe_barrier(PIPE_V);
Div(src,tmp,tmp1,elements); // x*e^(0.851*(x-abs(x))/(1+e^(-1.702*abs(x)))
pipe_barrier(PIPE_V);
}

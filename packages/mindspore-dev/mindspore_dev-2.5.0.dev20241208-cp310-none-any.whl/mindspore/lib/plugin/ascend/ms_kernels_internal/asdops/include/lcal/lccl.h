/*
 * Copyright (c) 2024 Huawei Technologies Co., Ltd.
 * AscendOpCommonLib is licensed under Mulan PSL v2.
 * You can use this software according to the terms and conditions of the Mulan PSL v2.
 * You may obtain a copy of Mulan PSL v2 at:
 *          http://license.coscl.org.cn/MulanPSL2
 * THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
 * EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
 * MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
 * See the Mulan PSL v2 for more details.
 */
#ifndef LACL_LCCL_H
#define LACL_LCCL_H

#include <lcal_comm.h>


namespace Lcal {
class Lccl {
public:
    explicit Lccl(LcalComm *comm);
    explicit Lccl(LcalComm &comm);
    ~Lccl();
    int Init(const std::string &uid = "", int maxBuffSize = LCAL_BUFF_BYTES) const;
    int InitThread() const;
    int AllReduce(void *sendBuff, void *recvBuff, int64_t count, HcclDataType dataType,
        HcclReduceOp op = HCCL_REDUCE_SUM, aclrtStream stream = nullptr) const;
    int ReduceScatter(void *sendBuff, void *recvBuff, int64_t count, HcclDataType dataType,
        HcclReduceOp op = HCCL_REDUCE_SUM, aclrtStream stream = nullptr) const;
    int AllGather(void *sendBuff, void *recvBuff, int64_t count, HcclDataType dataType, aclrtStream stream) const;
    int All2All(void *sendBuff, void *recvBuff, int64_t count, HcclDataType dataType, aclrtStream stream) const;

    int All2AllVC(void *sendBuff, void *recvBuff, HcclDataType dataType, aclrtStream stream) const;

    /**
     * @brief 跨机专用分层All2All，一维数组实际上是一个展平了的二维数组。
     */
    int All2AllInternal(const void *sendBuff, const void *recvBuff, const int64_t *sendCountMatrix,
        HcclDataType dataType, aclrtStream stream) const;
    int Broadcast(void *buff, int64_t count, HcclDataType dataType, int32_t root, aclrtStream stream) const;
    int BandwidthTest(const void *buff, void *recvBuff, int64_t count, HcclDataType dataType,
                        int32_t root, aclrtStream stream) const;
    friend class LcclTest;

private:
    bool CheckDataType(const HcclDataType &dataType) const;
    bool CheckBuff(const void *sendBuff, const void *recvBuff) const;
    int LoopBack(const void *sendBuff, void *recvBuff, int64_t count, HcclDataType dataType) const;

private:
    LcalComm *comm_ = nullptr;
    int rank_ = 0;
    int rankSize_ = 0;
};
}
#endif // LACL_LCCL_H


/*
 * calution: this file was generated automaticlly donot change it.
*/

#ifndef ACLNN_DECODER_KV_CACHE_H_
#define ACLNN_DECODER_KV_CACHE_H_

#include "aclnn/acl_meta.h"

#ifdef __cplusplus
extern "C" {
#endif

/* funtion: aclnnDecoderKvCacheGetWorkspaceSize
 * parameters :
 * cache : required
 * update : required
 * validSeqLen : required
 * batchIndex : required
 * seqLenAxis : required
 * newMaxSeqLen : required
 * curMaxSeqLen : required
 * out : required
 * workspaceSize : size of workspace(output).
 * executor : executor context(output).
 */
__attribute__((visibility("default")))
aclnnStatus aclnnDecoderKvCacheGetWorkspaceSize(
    const aclTensor *cache,
    const aclTensor *update,
    const aclTensor *validSeqLen,
    const aclTensor *batchIndex,
    const aclTensor *seqLenAxis,
    const aclTensor *newMaxSeqLen,
    const aclTensor *curMaxSeqLen,
    const aclTensor *out,
    uint64_t *workspaceSize,
    aclOpExecutor **executor);

/* funtion: aclnnDecoderKvCache
 * parameters :
 * workspace : workspace memory addr(input).
 * workspaceSize : size of workspace(input).
 * executor : executor context(input).
 * stream : acl stream.
 */
__attribute__((visibility("default")))
aclnnStatus aclnnDecoderKvCache(
    void *workspace,
    uint64_t workspaceSize,
    aclOpExecutor *executor,
    aclrtStream stream);

#ifdef __cplusplus
}
#endif

#endif

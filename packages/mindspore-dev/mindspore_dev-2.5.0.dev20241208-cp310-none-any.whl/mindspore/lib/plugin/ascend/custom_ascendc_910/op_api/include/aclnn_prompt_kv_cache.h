
/*
 * calution: this file was generated automaticlly donot change it.
*/

#ifndef ACLNN_PROMPT_KV_CACHE_H_
#define ACLNN_PROMPT_KV_CACHE_H_

#include "aclnn/acl_meta.h"

#ifdef __cplusplus
extern "C" {
#endif

/* funtion: aclnnPromptKvCacheGetWorkspaceSize
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
aclnnStatus aclnnPromptKvCacheGetWorkspaceSize(
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

/* funtion: aclnnPromptKvCache
 * parameters :
 * workspace : workspace memory addr(input).
 * workspaceSize : size of workspace(input).
 * executor : executor context(input).
 * stream : acl stream.
 */
__attribute__((visibility("default")))
aclnnStatus aclnnPromptKvCache(
    void *workspace,
    uint64_t workspaceSize,
    aclOpExecutor *executor,
    aclrtStream stream);

#ifdef __cplusplus
}
#endif

#endif

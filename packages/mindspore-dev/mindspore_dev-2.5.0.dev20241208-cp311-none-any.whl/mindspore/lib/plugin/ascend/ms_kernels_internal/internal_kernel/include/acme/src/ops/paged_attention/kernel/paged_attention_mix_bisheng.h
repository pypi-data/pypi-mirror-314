#ifndef MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_PAGED_ATTENTION_KERNEL_PAGED_ATTENTION_MIX_BISHENG_H
#define MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_PAGED_ATTENTION_KERNEL_PAGED_ATTENTION_MIX_BISHENG_H
constexpr float DROPOUT_PROP = 0.5;
constexpr uint64_t KSIZE = 1024;
constexpr uint64_t LOOP_LEN = 5;
constexpr uint64_t UB_HALF_BUF_SIZE = 16 * KSIZE;
constexpr uint64_t BIT_UINT8 = 8;
constexpr uint64_t BIT_BLOCK = 256;
constexpr uint64_t BLOCK_SIZE_16 = 16;
constexpr uint64_t BLOCK_SIZE_32 = 8;
constexpr uint64_t VECTOR_SIZE_16 = 128;
constexpr uint64_t VECTOR_SIZE_32 = 64;
constexpr uint64_t CUBE_MATRIX_SIZE = 256;  // 16 * 16
constexpr uint64_t CUBE_MATRIX_SIZE_512 = 512;  // 16 * 32
constexpr uint64_t UB_UINT8_BLOCK_SIZE = 16 * KSIZE; // 64 * 128 * 2B
constexpr uint64_t L0AB_INT8_BUF_SIZE = 32 * KSIZE; // 128 * 128 * 2
constexpr uint64_t UB_UINT8_LINE_SIZE = 512;    // 64 * 4B，申请两倍空间防踩踏。
constexpr uint64_t UB_FLOAT_LINE_SIZE = 128;    // 64，申请两倍空间防踩踏。
constexpr uint64_t UB_HALF_LINE_SIZE = 256;     // UB_FLOAT_LINE_SIZE * 2

constexpr uint64_t L0AB_HALF_BUF_SIZE = 16 * KSIZE; // 128 * 128
constexpr uint64_t L1_SIZE = 512 * 1024; // 512KB
constexpr uint64_t L0AB_UINT8_BLOCK_SIZE = 32768; // 128 * 128 * 2B
constexpr uint64_t L1_MAX_SHARE_NUM = (L1_SIZE - 8 * L0AB_UINT8_BLOCK_SIZE) / L0AB_UINT8_BLOCK_SIZE / 2;
constexpr uint64_t SUB_SP_SIZE_16 = 16 * KSIZE;  // 1024*16, 2048*8, 4096*4, 8192*2, 16K*1, 5种分块方法
constexpr uint64_t SUB_SP_SIZE_32 = 8 * KSIZE;  // 1024*8, 2048*4, 4096*2, 8192*1, 4种分块方法

constexpr uint64_t QK_REDAY_0 = 0;
constexpr uint64_t QK_REDAY_1 = 1;
constexpr uint64_t QK_REDAY_2 = 2;
constexpr uint64_t QK_REDAY_3 = 3;
constexpr uint64_t SOFTMAX_REDAY_0 = 4;
constexpr uint64_t SOFTMAX_REDAY_1 = 5;
constexpr uint64_t SOFTMAX_REDAY_2 = 6;
constexpr uint64_t SOFTMAX_REDAY_3 = 7;
constexpr uint64_t VEC_QUANT_REDAY_0 = 8;
constexpr uint64_t VEC_QUANT_REDAY_1 = 9;
constexpr uint64_t VEC_QUANT_REDAY_2 = 10;
constexpr uint64_t VEC_QUANT_REDAY_3 = 11;
constexpr uint64_t FLSH_DECODING_INTER_REDAY = 12;
constexpr uint64_t FLSH_DECODING_INTRA_REDAY = 13;

enum Type {
    kFp16 = 0,
    kBf16 = 1,
    kFp32 = 2
};

enum Layout {
    kBsh = 0,
    kBnsd = 1
};

enum QuantMode {
    kNoQuant = 0,
    kPerChannel = 1,
    kPerToken = 2
};

enum QuantMethod : int {
    kFp16Vec = 0,
    kFp32Vec = 1,
    kIntCube = 2
};

enum class FDMode {kOn, kOff};

inline uint64_t ceil(uint64_t y, uint64_t x) {
    return (y + x - 1) / x;
}

inline uint64_t round(uint64_t y, uint64_t x) {
    return ceil(y, x) * x;
}

#endif

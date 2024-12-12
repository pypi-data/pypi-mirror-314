adh_add_library(
  NAME zstd
  SOURCES
    common/debug.c
    common/entropy_common.c
    common/error_private.c
    common/fse_decompress.c
    common/pool.c
    common/threading.c
    common/xxhash.c
    common/zstd_common.c
    compress/fse_compress.c
    compress/hist.c
    compress/huf_compress.c
    compress/zstd_compress.c
    compress/zstd_compress_literals.c
    compress/zstd_compress_sequences.c
    compress/zstd_double_fast.c
    compress/zstd_fast.c
    compress/zstd_lazy.c
    compress/zstd_ldm.c
    compress/zstd_opt.c
    compress/zstdmt_compress.c
    decompress/huf_decompress.c
    decompress/zstd_ddict.c
    decompress/zstd_decompress.c
    decompress/zstd_decompress_block.c
  PUBLIC_HEADERS
    ${CMAKE_CURRENT_LIST_DIR}/zstd.h
  EXPORT ${PROJECT_NAME}Targets
)


target_include_directories(
    zstd PUBLIC 
    $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}/common>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}/compress>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}/decompress>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

/*
py-fpng-nb
https://github.com/dofuuz/py-fpng-nb

SPDX-FileCopyrightText: (c) 2024 KEUM Myungchul
SPDX-License-Identifier: MIT

Fast PNG writer for Python.
py-fpng-nb is a Python wrapper of fpng(https://github.com/richgel999/fpng).
*/

#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>

#include <fpng.h>


namespace nb = nanobind;
using namespace nb::literals;
using nb::ndarray;

using namespace fpng;


nb::bytes cfpng_encode_ndarray(
        ndarray<const uint8_t, nb::ndim<3>, nb::c_contig, nb::device::cpu> img) {
    const uint32_t h = img.shape(0);
    const uint32_t w = img.shape(1);
    const uint32_t num_chans = img.shape(2);
	// bool fpng_encode_image_to_memory(const void* pImage, uint32_t w, uint32_t h, uint32_t num_chans, std::vector<uint8_t>& out_buf, uint32_t flags = 0);

    std::vector<uint8_t> out_buf;
    auto ret = fpng_encode_image_to_memory(img.data(), w, h, num_chans, out_buf);

    if (!ret) std::runtime_error("fpng_encode_image_to_memory() failed!");

    // TODO: return by ref (not copy)
    return nb::bytes(out_buf.data(), out_buf.size());
}


nb::bytes cfpng_encode_image_to_memory(nb::bytes img, uint32_t w, uint32_t h, uint32_t num_chans) {
    std::vector<uint8_t> out_buf;
    auto ret = fpng_encode_image_to_memory(img.data(), w, h, num_chans, out_buf);

    if (!ret) std::runtime_error("fpng_encode_image_to_memory() failed!");

    // TODO: return by ref (not copy)
    return nb::bytes(out_buf.data(), out_buf.size());
}


bool cfpng_encode_image_to_file(const char* pFilename, nb::bytes pImage, uint32_t w, uint32_t h, uint32_t num_chans, uint32_t flags = 0) {
    return fpng_encode_image_to_file(pFilename, pImage.data(), w, h, num_chans, flags);
}



NB_MODULE(fpng_ext, m) {
    m.def("init", &fpng_init);
    m.def("cpu_supports_sse41", &fpng_cpu_supports_sse41);
    // m.def("crc32", );
    // m.def("adler32", );

    nb::enum_<decltype(FPNG_ENCODE_SLOWER)>(m, "EncodeFlag", nb::is_flag())
        .value("SLOWER", FPNG_ENCODE_SLOWER)
        .value("FORCE_UNCOMPRESSED", FPNG_FORCE_UNCOMPRESSED)
        .export_values();

    m.def("encode_image_to_memory", &cfpng_encode_image_to_memory);
    m.def("encode_image_to_file", &cfpng_encode_image_to_file);

    m.def("test_func", [](const char* pFilename, const uint8_t* asdf) { } );

    m.def("encode_ndarray", &cfpng_encode_ndarray);

    m.attr("DECODE_SUCCESS") = (int)FPNG_DECODE_SUCCESS;
    m.attr("DECODE_NOT_FPNG") = (int)FPNG_DECODE_NOT_FPNG;
    m.attr("DECODE_INVALID_ARG") = (int)FPNG_DECODE_INVALID_ARG;
    m.attr("DECODE_FAILED_NOT_PNG") = (int)FPNG_DECODE_FAILED_NOT_PNG;
    m.attr("DECODE_FAILED_HEADER_CRC32") = (int)FPNG_DECODE_FAILED_HEADER_CRC32;
    m.attr("DECODE_FAILED_INVALID_DIMENSIONS") = (int)FPNG_DECODE_FAILED_INVALID_DIMENSIONS;
    m.attr("DECODE_FAILED_DIMENSIONS_TOO_LARGE") = (int)FPNG_DECODE_FAILED_DIMENSIONS_TOO_LARGE;
    m.attr("DECODE_FAILED_CHUNK_PARSING") = (int)FPNG_DECODE_FAILED_CHUNK_PARSING;
    m.attr("DECODE_FAILED_INVALID_IDAT") = (int)FPNG_DECODE_FAILED_INVALID_IDAT;
    m.attr("DECODE_FILE_OPEN_FAILED") = (int)FPNG_DECODE_FILE_OPEN_FAILED;
    m.attr("DECODE_FILE_TOO_LARGE") = (int)FPNG_DECODE_FILE_TOO_LARGE;
    m.attr("DECODE_FILE_READ_FAILED") = (int)FPNG_DECODE_FILE_READ_FAILED;
    m.attr("DECODE_FILE_SEEK_FAILED") = (int)FPNG_DECODE_FILE_SEEK_FAILED;

    m.def("get_info", &fpng_get_info);
    m.def("decode_memory", &fpng_decode_memory);
    // m.def("decode_file", &fpng_decode_file);
}

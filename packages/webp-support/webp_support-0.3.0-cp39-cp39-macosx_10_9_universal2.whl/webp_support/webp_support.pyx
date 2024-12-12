# webp_support.pyx
cimport cython

cdef extern from "webp_support_c.h":
    bint is_webp_supported(const char *user_agent)

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef bint webp_supported(bytes user_agent):
    return is_webp_supported(user_agent)
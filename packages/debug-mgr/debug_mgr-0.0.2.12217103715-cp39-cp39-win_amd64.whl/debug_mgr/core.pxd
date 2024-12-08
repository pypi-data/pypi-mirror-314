
from debug_mgr cimport decl
from libc.stdint cimport intptr_t
from libc.stdint cimport int32_t
from libc.stdint cimport uint32_t
from libc.stdint cimport uint64_t
from libc.stdint cimport int64_t
from libcpp cimport bool
from libcpp.vector cimport vector as cpp_vector
from enum import IntFlag, IntEnum
cimport cpython.ref as cpy_ref

cdef class Factory(object):
    cdef decl.IFactory              *_hndl

    cpdef DebugMgr getDebugMgr(self)

cdef class DebugMgr(object):
    cdef decl.IDebugMgr             *_hndl
    cdef bool                       _owned

    cpdef void enable(self, bool en)

    cdef decl.IDebugMgr *getHndl(self)

    @staticmethod
    cdef DebugMgr mk(decl.IDebugMgr *hndl, bool owned=*)

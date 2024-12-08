

from libc.stdint cimport intptr_t
from libc.stdint cimport int32_t
from libc.stdint cimport uint32_t
from libc.stdint cimport uint64_t
from libc.stdint cimport int64_t
from libcpp cimport bool
from libcpp.vector cimport vector as cpp_vector
cimport cpython.ref as cpy_ref

ctypedef IFactory *IFactoryP
ctypedef IDebugMgr *IDebugMgrP

cdef extern from "dmgr/IFactory.h" namespace "dmgr":
    cdef cppclass IFactory:
        IDebugMgr *getDebugMgr()

cdef extern from "dmgr/IDebugMgr.h" namespace "dmgr":
    cdef cppclass IDebugMgr:
        void enable(bool en)

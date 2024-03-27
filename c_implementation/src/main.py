from ctypes import CDLL, POINTER, Structure, c_uint64, c_uint8

c_lib = CDLL(r".\c_implementation\src\main.dll", mode=1, use_errno=True, use_last_error=True)


class Set(Structure):
    _fields_ = [
        ("items", POINTER(c_uint64)),
        ("size", c_uint8),
        ("capacity", c_uint8)
    ]

c_lib.shor.restype = POINTER(Set)
c_lib.shor.argtypes = [c_uint64]

ptr = c_lib.shor(214136124)

results = set(ptr.contents.items[i] for i in range(ptr.contents.size))
# free the memory
c_lib.free_set(ptr)

print(results)

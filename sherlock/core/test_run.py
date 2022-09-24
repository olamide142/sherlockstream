import os
import time
import ctypes

# swig -python sherlock.i 
os.system("gcc -fPIC -c sherlock.c -I/usr/include/python3.10 && ld -shared sherlock.o -o _sherlock.so")

time.sleep(1)

lib_sherlock = ctypes.CDLL('./_sherlock.so')

print(
    lib_sherlock.get_pyobject(
        ctypes.py_object([1,2,3,4])
    )
)
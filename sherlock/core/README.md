swig -python sherlock.i
gcc -fPIC -c sherlock.c sherlock_wrap.c -I/usr/include/python3.10
ld -shared sherlock.o sherlock_wrap.o -o _sherlock.so
<!-- load _sherlock.so with ctypes.CDLL -->
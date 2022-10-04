import os
import time
import ctypes

class Dispatcher:

    def __init__(self):
        self.lib_sherlock = ctypes.CDLL('./_sherlock.so')

    def process(self):
        self.lib_sherlock.process_tracer(ctypes.py_object(self))

if __name__ == "__main__":
    # swig -python sherlock.i 
    os.system("gcc -fPIC -c sherlock.c -I/usr/include/python3.10 && ld -shared sherlock.o -o _sherlock.so")

    time.sleep(1)

    a = Dispatcher()
    a.process()


# # program to display the functioning of
# # settrace()
# from sys import settrace

# # local trace function which returns itself
# def my_tracer(frame, event, arg = None):
# 	# extracts frame code
# 	code = frame.f_code

# 	# extracts calling function name
# 	func_name = code.co_name

# 	# extracts the line number
# 	line_no = frame.f_lineno
    
# 	print(code.co_filename)
# 	return my_tracer


# # global trace function is invoked here and
# # local trace function is set for fun()
# def fun():
#     return "GFG"


# # global trace function is invoked here and
# # local trace function is set for check()
# def check():
# 	return fun()


# # returns reference to local
# # trace function (my_tracer)
# settrace(my_tracer)
# check()

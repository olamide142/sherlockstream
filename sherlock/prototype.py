# import os
# import pprint
# from re import sub
# from subprocess import Popen, PIPE
# import pdb
# from sys import stdin, stdout
# import cmd
# import io 

import pexpect
from pprint import pprint as pp

def open_pipe():

    process = pexpect.spawn('python -m pdb sherlock/sample.py')
    # import pdb;
    # pdb.set_trace()

    for i in range(10):
        process.sendline('n')
        process.expect("\r")
        print(str(process.before))
    print("Done")
def send_to_pipe():
    # pipe.
    pass


if __name__ == '__main__':
    open_pipe()

# else: send_to_pipe()
    

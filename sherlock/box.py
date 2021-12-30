import os
import pexpect 

from socket_manager import SocketManager
from code_inspector import CodeInspector

class Box():
    def __init__(self):
        self.process = pexpect.spawn('python3 -m pdb sherlock/run.py 9000', )
        self.inspector = CodeInspector()
        

    def kickoff(self):
        while 1:
            self.process.sendline(self.inspector.next_input())
            self.inspector.last_output = os.read(self.process.child_fd, 1024*30).decode()
            if 'The program finished and will be restarted' in str(self.inspector.last_output):# or 'Error' in str(self.inspector.last_output): #TODO: This should check a list of builtin errors and exceptions
                socketmanager = SocketManager()
                socketmanager.emit_no_questions_asked(self.inspector.get_recent_io())
                raise StopIteration
            yield self.inspector.last_output
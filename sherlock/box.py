import os
import pexpect 

from code_inspector import CodeInspector

class Box():
    def __init__(self):
        self.process = pexpect.spawn('python -m pdb sherlock/sample.py', )
        self.last_output = None
        self.last_input = None
        self.inspector = CodeInspector()

    def kickoff(self):
        while 1:
            self.last_input = self.update()
            self.process.sendline(self.last_input)
            self.last_output = os.read(self.process.child_fd, 1024*30).decode().strip()
            # import pdb; pdb.set_trace()
            if 'The program finished and will be restarted' in str(self.last_output):
                raise StopIteration
            yield self.last_output
    
    def update(self):
        if self.last_output is None:
            return u"\r\ns"
        else:
            return u"\r\nl"

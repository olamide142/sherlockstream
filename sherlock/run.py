import pdb
import sys
import subprocess
import os
from enum import Enum
import random
from uuid import uuid4

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from werkzeug.debug import tbtools



app = Flask(__name__)
socketio = SocketIO(app)

app.config['SECRET_KEY'] = 'secret'


class Box():
    
    def __init__(self, executable=None):
        self.id = uuid4()
        self.executable = sys.executable


class FileSystem(Box):
    """ Manage all execution state datastructure """

    def __init__(self, name=None):
        super().__init__()
        self.name = name 


class State(Enum):
    ERROR = 1

    def __call__(self):
        pdb.set_trace()


class SocketManager:

    @socketio.on('connect')
    def connect():
        print("Some one connected")
        emit('my response', {'data': f'{random.randint(100, 200)}'})

    @socketio.event
    def disconnect():
        print("Some one disconnected")


class StreamManager():

    streams = list()

    def __init__(self, file_name):
        self.file_name = self._file_status(file_name)

    def _file_status(self, file_name):
        if os.path.exists(file_name):
            StreamManager.streams.append(self)
            return file_name
        else:
            return State.ERROR


class CodeInspector(StreamManager):

    def __init__(self):
        # super().__init__(file_name=stream.)
        pass

    def runner(self):
        os.system()


@app.route("/")
def main():
    streams = StreamManager.streams
    # Trigger the debugger
    a = 's'+1
    return render_template('index.html')



if __name__ == '__main__':
    manager = StreamManager('') #sys.argv[1])
    socketio.run(app, debug=True)
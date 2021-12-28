import sys
import os

import pexpect
from flask import Flask, render_template
from flask_socketio import SocketIO
from werkzeug.debug import tbtools

from socket_manager import SocketManager

app = Flask(__name__)
socketio = SocketIO(app)

app.config['SECRET_KEY'] = 'secret'

@app.route("/")
def main():
    return render_template('index.html')


if __name__ == '__main__':
    # manager = StreamManager('') #sys.argv[1])
    socketio.on_namespace(SocketManager('/sherlock'))
    socketio.run(app, debug=True, port=int(sys.argv[1]))

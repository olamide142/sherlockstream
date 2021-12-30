import sys
import os

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
# from werkzeug.debug import tbtools

from socket_manager import SocketManager
from code_viewer import CodeViewer

app = Flask(__name__)
socketio = SocketIO(app)

app.config['SECRET_KEY'] = 'secret'

@app.route("/")
def main():
    return render_template('index.html')



@app.route("/fileview")
def file_view():
    
    view, startline, endline = CodeViewer.load_for_web(request)
    linenum = int(startline)
    for i,j in enumerate(view):
        a = str(linenum) + j
        view[i] = a
        linenum +=1
    return jsonify(lines=view, startline=startline, endline=endline)

if __name__ == '__main__':
    # manager = StreamManager('') #sys.argv[1])
    socketio.on_namespace(SocketManager('/sherlock'))
    socketio.run(app, debug=True, port=int(sys.argv[1]))
from flask_socketio import Namespace, emit

from box import Box

class SocketManager(Namespace):
    """ Manage all incoming and outgoing request
        of process execution in real time """

    def on_connect(self):
        print("Connected")
        emit('status', {'color': 'blue', 'msg': 'Sherlock On'})

    def on_disconnect(self):
        print("Disconnected")

    def on_start_btn(self, data):
        global box
        box = Box()
        try:
            for i in box.kickoff():
                emit('response', {'data': i, 'last_input':box.last_input})
        except RuntimeError:
            emit('status', {'color':'blue', 'msg':'Program completed'})


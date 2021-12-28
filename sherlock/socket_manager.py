from flask_socketio import Namespace, emit

class SocketManager(Namespace):
    """ Manage all incoming and outgoing request
        of process execution in real time """

    def on_connect(self,):
        print("Connected")
        emit('status', {'color': 'blue', 'msg': 'Sherlock On'})

    def on_disconnect(self):
        print("Disconnected")

    def on_start_btn(self, data):
        # global box
        box = __import__('box').Box()
        try:
            for last_output in box.kickoff():
                emit('response', box.inspector.get_recent_io())
        except RuntimeError:
            emit('status', {'color':'blue', 'msg':'Program completed'})

    def emit_no_questions_asked(self, json_data):
        emit('response', json_data)

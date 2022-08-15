import socketio

sio = socketio.Client()
sio.connect('http://localhost:5000')

class Dispatcher(socketio.ClientNamespace):

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def write(self, data):
        sio.emit( 'my_broadcast_event', {"data" : str(data)} )
            
    @sio.event
    def server_response(event, data=None):
        ...

    #sio.register_namespace(MyCustomNamespace('/chat'))
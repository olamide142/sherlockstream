import zmq

class Dispatcher:
    
    _instance = None
    _sock = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, port = 8889, host = "127.0.0.1"):
        if cls._instance is None:
            print("Connecting to hello world server...")
            cls._instance = cls.__new__(cls)
            context = zmq.Context()
            cls._sock = context.socket(zmq.REQ)
            cls._sock.connect(f"tcp://{host}:{port}")
        return cls._instance

    
    def write(cls, data):
        cls._sock.send_string(data)

        #  Get the reply.
        response = cls._sock.recv()
        if response != b"no":
            print(response)
        # might use response in the future
        return


if __name__ == '__main__':

    dispatcher = Dispatcher.instance()
    import uuid
    import time
    start = time.time()

    for i in range(1_000_000):
        
        dispatcher.write(str(uuid.uuid4()))

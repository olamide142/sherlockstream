
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:8889")

count = 0
start = None
with open('file.log', 'a') as f:

    while True:
        #  Wait for next request from client
        message = socket.recv()
        # print(f"Received request: {message}")

        count +=1
        if count == 1:
            start = time.time()
        if count %50000 == 0:
            socket.send_string(f"Written {count} in {time.time() - start} seconds")
        else:
            socket.send_string("no")

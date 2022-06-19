"""Manage a sherlock stream session
(not a network server)
"""
import functools

import zmq
from sherlock.sherlock_data.persistence import Log2DB

from sherlock.utils import recoverOriginal


"""ALGORITHM
    1: setup data structures
    2: start tailing logs in a thread
    3: parse the logs into data structure (maybe with re)
    4: Query/Order by feature
        * get most called function
        * least called function
    5: Group a sequence of calls that are identical 
        eg: a->b->c->d->e->a->b->c->f-e->a
        groups (a->b->c), (e->a)
    6: get list of logs with a range (depending on where 
        the scrollbar is maybe list slicing)
    7: load a lines from a file based on log line #::#::#
        

"""
class Server:

    def __init__(self, db) -> None:
        self.recovered = False
        self.db = db
        self.running = True
        self.socket = self.setUp()

    def setUp(self):
        # Creates a socket instance
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)
        subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
        # Connects to a bound socket
        subscriber.connect("ipc:///tmp/sherlock_stream_network")

        # Subscribes to all topics
        subscriber.subscribe("")

        print('[+] Server started')
        return subscriber

    def poll(self):
        while self.running:
            val = self.socket.recv_string()
            self.recover()
            if val:
                yield val.upper()
        raise StopIteration
    
    def kill(self):
        print("killing server")
        self.running = False
                
    @functools.lru_cache(maxsize=1)
    def recover(self):
        if not self.recovered:
            recoverOriginal(self.db)
            self.recovered = True

if __name__ == '__main__':
    # db = Log2DB.instance()
    # server = Server(db)
    # for i in server.poll():
    #     print(i)
    ...
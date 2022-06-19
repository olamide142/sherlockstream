import logging
import functools

import zmq

from sherlock.sherlock_types import TYPES
from sherlock.log4sherlock import SHERLOCK_LOG_LEVEL, Log4Sherlock

logger = Log4Sherlock().getLogger()

@functools.lru_cache(maxsize=1)
def getPublisher():
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("ipc:///tmp/sherlock_stream_network")
    print('[+] Sherlock publisher ready')
    publisher.send_string('ok')
    return publisher

def functionCalled(sessionId, hashId):
    """ Helper code to be injected into primary source
        and publish the event to the server
    """
    
    sql = f"""
        INSERT INTO function_call (session_id, hash_id) 
        VALUES ({sessionId}, '{hashId}')
    """
    publisher = getPublisher()
    publisher.send_string(sql)
    
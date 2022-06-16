import logging

from sherlock.sherlock_types import TYPES
from sherlock.log4sherlock import SHERLOCK_LOG_LEVEL, Log4Sherlock
from sherlock.sherlock_data.persistence import Log2DB

logger = Log4Sherlock().getLogger()
db = Log2DB.instance() 

def functionCalled(hashId):
    """ Helper code to be injected into primary source """
    sql = f"""
        INSERT INTO program_flow (session_id, hash_id) 
        VALUES ({db.getSession()[0]}, '{hashId}')
    """
    db.insertQuery(sql)
import logging

from sherlock.sherlock_types import TYPES
from sherlock.log4sherlock import SHERLOCK_LOG_LEVEL, Log4Sherlock

logger = Log4Sherlock().getLogger()

def functionCalled(name, line):
    """ Helper code to be injected into primary source """
    logger.log(
        SHERLOCK_LOG_LEVEL, str(TYPES['FunctionCall'](name, line))
    )
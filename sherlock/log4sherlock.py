'''Manage all logs generated by sherlock stream'''
import logging
from sherlock import Sherlock
Sherlock(__file__)

def startLogger():
    logging.basicConfig(filename='sherlock.log', format='%(message)s', level=logging.INFO)
    logging.info('Sherlock Stream Logging Started')

if __name__ == '__main__':
    startLogger()
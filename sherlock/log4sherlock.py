import logging

def startLogger():
    logging.basicConfig(filename='sherlock.log', format='%(message)s', level=logging.INFO)
    logging.info('Sherlock Stream Logging Started')

if __name__ == '__main__':
    startLogger()
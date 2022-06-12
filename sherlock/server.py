import time

def follow(file, sleep_sec=0.1):
    """ Yield each line from a file as they are written.
    `sleep_sec` is the time to sleep after empty reads. """
    line = ''
    while True:
        tmp = file.readline()
        if tmp is not None:
            line += tmp
            if line.endswith("\n"):
                yield line
                line = ''
        elif sleep_sec:
            time.sleep(sleep_sec)

def tailLog(logPath='sherlock.log'):
    with open(logPath, 'r') as file:
        for line in follow(file):
            print(line, end='')

if __name__ == '__main__':
    tailLog("/home/victor/workspace/UniPortal/sherlock.log")
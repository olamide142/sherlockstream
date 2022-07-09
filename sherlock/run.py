#!/usr/bin/python
import os
os.system('rm -rf /home/victor/workspace/sherlockstream/venv/lib/python3.8/site-packages/flake8*/')
os.system('rm -rf /home/victor/workspace/sherlockstream/venv/lib/python3.8/site-packages/pyflake*/')
os.system('rm -rf /home/victor/workspace/sherlockstream/sherlock_db*')
os.system('rm /tmp/sherlock_stream_network')

# os.system('rm -rf /home/victor/workspace/sherlockstream/venv/lib/python3.8/site-packages/pygame*/')
# os.system('rm -rf sherlock_db sherlock.log ')
os.system('pip3 install flake8')
import time
time.sleep(2)
lines = """

from sherlock import Sherlock
Sherlock(__file__)
from flake8.main import cli

cli.main()

"""
with open('/home/victor/workspace/sherlockstream/venv/lib/python3.8/site-packages/flake8/__main__.py', 'w') as f:
    f.write(lines)

time.sleep(1)
os.system('python -m flake8 /home/victor/workspace/sherlockstream/sherlock/log4sherlock.py | tee log.txt')

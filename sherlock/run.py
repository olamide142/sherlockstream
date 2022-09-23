import os
import time

# os.system("git stash")
# time.sleep(2)

os.system("pip uninstall MarkupSafe itsdangerous click Werkzeug Jinja2 flask")
os.system("pip install MarkupSafe itsdangerous click Werkzeug Jinja2 flask")
file = None
path = "/home/lams/workspace/flask/venv/bin/flask"
with open(path, 'r') as f:
    
    file = f.readlines()

with open(path, 'w') as f:

    for i, j in enumerate(file):
        if i in [1]:
            f.write(j)
            f.write("from sherlock import Sherlock\n")
            f.write("Sherlock(__file__)\n")
            continue

        f.write(j)
os.system('export PYTHONPATH="${PYTHONPATH}:/home/lams/workspace/sherlockstream"')
os.system("flask run")

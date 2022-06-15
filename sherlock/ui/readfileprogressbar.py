from copy import deepcopy
from time import sleep
from io import BytesIO
from rich.progress import wrap_file

import rich
import inspect
rich.print(inspect.getsource(wrap_file))

def show_lines():
        
    with wrap_file(
        file := BytesIO(open('sherlock.log', 'rb').read()), 
        len(deepcopy(file).readlines())
        ) as file:

        for line in file:
            print(line.decode("utf-8"), end="")
            sleep(0.0001)

show_lines()

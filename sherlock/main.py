'''Main entry to sherlock stream'''
import os
import sys

from sherlock.import_decoder import get_paths
from sherlock.transformer import convert_file_to_ast, function_decorator
from sherlock.sherlock_data.persistence import Log2DB
from sherlock.utils import backup_original, get_full_path, sherlockUnhalt

"""
export PYTHONPATH="${PYTHONPATH}:/home/victor/workspace/sherlockstream"
"""

class _SherlockStream:
    '''Calling Sherlock Stream from source code'''
    def __init__(self, entry_file=None):
        self.entry_file = entry_file
        # self.db = Log2DB.instance()
        self.main(self.entry_file)

        
    def main(self, entry_file):
        
        entry_file = get_full_path(entry_file)
        parsed_files = set()
        unparsed_files = set() 
        unparsed_files.add(entry_file)

        while len(unparsed_files) > 0:
            print(unparsed_files)
            current_file = unparsed_files.pop()
            if current_file not in parsed_files:
                current_ast = convert_file_to_ast(current_file)
                unparsed_files = get_paths(current_ast, unparsed_files)
            print(current_file)
            backup_original(current_file)
            function_decorator(current_file)
            parsed_files.add(current_file)
        
        #to avoid getting stuck in a recursion
        sherlockUnhalt(entry_file)
        

if __name__ == '__main__':
    _SherlockStream(sys.argv[0])
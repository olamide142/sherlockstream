'''Main entry to sherlock stream'''
import os
import sys
import atexit

from sherlock.import_decoder import get_paths
from sherlock.transformer import convert_file_to_ast, function_decorator
from sherlock.utils import backup_original, get_full_path, sherlock_unhalt,\
     recover_original, add_neighbours

"""
export PYTHONPATH="${PYTHONPATH}:/home/victor/workspace/sherlockstream"
"""

class _SherlockStream:
    '''Calling Sherlock Stream from source code'''
    def __init__(self, entry_file=None):
        self.entry_file = entry_file
        self.parsed_files = set()
        self.unparsed_files = set()
        atexit.register(self.clean_up)
        self.main(self.entry_file)


    def clean_up(self):
        recover_original(self.parsed_files)


    def main(self, entry_file):

        self.unparsed_files.add(entry_file)
        entry_file = get_full_path(entry_file)

        while len(self.unparsed_files) > 0:

            print(len(self.unparsed_files))
            current_file = self.unparsed_files.pop()

            if current_file.endswith('__init__.py'):
                unparsed_files = add_neighbours(current_file, 
                                                self.unparsed_files, 
                                                self.parsed_files)

            if current_file not in self.parsed_files:
                current_ast = convert_file_to_ast(current_file)
                self.unparsed_files = get_paths(current_ast, self.unparsed_files)
            else: continue

            backup_original(current_file)
            function_decorator(current_file)
            self.parsed_files.add(current_file)
        
        #to avoid getting stuck in a recursion
        sherlock_unhalt(entry_file)

        os.system(" ".join(sys.argv))

        
if __name__ == '__main__':
    _SherlockStream(sys.argv[0])
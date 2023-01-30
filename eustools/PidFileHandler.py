import os
from logging import FileHandler

PID = ''.join(['.pid_',str(os.getpid())])
def new_filename(filename): return ''.join([filename, PID])

class PidFileHandler(FileHandler):
    # change the default filename to include the process pid
    # so that the same filename can be used with multiple processes without conflict
    def __init__(self, filename, mode='a', encoding=None, delay=False, errors=None):
        super().__init__(new_filename(filename), mode, encoding, delay, errors)


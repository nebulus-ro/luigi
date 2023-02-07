import os

def find_folder(start_with, path):
    for dir in os.listdir(path):
        if os.path.isdir(os.path.join(path, dir)) and dir.startswith(start_with):
            yield dir

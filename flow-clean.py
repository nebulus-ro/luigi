import os
import sys
import zipfile
from tools import tools

FLAG_ZIP = '-a'
# check for flags: -a archiving, else deleting
# collect possible sessions
params = sys.argv[1:]
isZip = FLAG_ZIP in params
prefs = [arg for arg in params if arg != FLAG_ZIP]
action = 'Archive' if isZip else 'Delete'
print(f'{action} sessions: {prefs if prefs else "ALL"}')

def delete_folder_contents(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                delete_folder_contents(file_path)
                os.rmdir(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


# get first level
# ! do not touch the first level files (may be archives)
root = os.path.join('.', 'sessions')

# prepare sessions
sessions = []
if not prefs:
    sessions = [filename for filename in os.listdir(root) if os.path.isdir(os.path.join(root, filename))]
else:
    for pref in prefs:
        isUnique, filename = tools.get_session(pref)
        if isUnique: sessions.append(filename)
# process sessions
for sess in sessions:
    print(' -', sess)
    file_path = os.path.join(root, sess)
    if os.path.isdir(file_path):
        if isZip:
            with zipfile.ZipFile(file_path + '.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipdir(file_path, zipf)
        delete_folder_contents(file_path)
        os.rmdir(file_path)
print()
print('Done')

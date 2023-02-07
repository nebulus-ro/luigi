import platform
import os
import sys
import importlib
import luigi
import uuid
import pickle
from tools.tools import find_folder

guidHead = sys.argv[1]
userId = sys.argv[2]

guids = list(find_folder(guidHead, './sessions'))
if guids:
    if len(guids) > 1:
        print(f'Too many sessions start with: {guidHead}. Try a longer sequence.')
        exit()
else:
    print(f'No session starts with: {guidHead}')
    exit()        

guid = guids[0]

print("Resume session:", guid)
folder_name = f'sessions/{guid}'

# load context 
with open(f'{folder_name}/context.pickle', 'rb') as handle:
    context = pickle.load(handle)

taskSource = context['taskSource']
taskName = context['taskName']
print("Head task:", taskSource, taskName)
print("User:", userId)

module = importlib.import_module(f'tasks.{taskSource}')
task_class = getattr(module, taskName)
print(task_class)

# add some settings
config = luigi.configuration.LuigiConfigParser.instance()
config.set('session', 'id', guid)

# start the flow
config = luigi.configuration.LuigiConfigParser.instance()

# print the tree
import luigi.tools.deps_tree as deps_tree
print(deps_tree.print_tree(task_class()))

luigi.build([task_class()], local_scheduler=True, detailed_summary=False)
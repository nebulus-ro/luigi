import platform
import os
import sys
import importlib
import luigi
import uuid
import pickle

guid = sys.argv[1]
extSource, extName = sys.argv[2].split('.')
param = None
if len(sys.argv) == 4:
    userId = sys.argv[3]
elif len(sys.argv) == 5:
    userId = sys.argv[4]
    param = sys.argv[3]

print("Resume session:", guid)
folder_name = f'sessions/{guid}'

# load context 
with open(f'{folder_name}/context.pickle', 'rb') as handle:
    context = pickle.load(handle)

taskSource = context['taskSource']
taskName = context['taskName']
print("Head task:", taskSource, taskName)
print('Extension:', extSource, extName)
print("User:", userId)

module = importlib.import_module(f'tasks.{extSource}')
task_class = getattr(module, extName)
print(task_class)

# add some settings
config = luigi.configuration.LuigiConfigParser.instance()
config.set('session', 'id', guid)

# start the flow
config = luigi.configuration.LuigiConfigParser.instance()

# print the tree
import luigi.tools.deps_tree as deps_tree
if param is None:
    print(deps_tree.print_tree(task_class()))
else:
    print(deps_tree.print_tree(task_class(param)))

if param is None:
    luigi.build([task_class()], local_scheduler=True, detailed_summary=False)
else:
    luigi.build([task_class(param)], local_scheduler=True, detailed_summary=False)

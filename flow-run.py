import platform
import os
import sys
import importlib
import luigi
import uuid
import pickle

taskSource, taskName = sys.argv[1].split('.')
userId = sys.argv[2]

print("Task:", taskSource, taskName)
print("User:", userId)

module = importlib.import_module(f'tasks.{taskSource}')
task_class = getattr(module, taskName)
print(task_class)

# create a context for 
context = {}
guid = str(uuid.uuid4())
context['sessionId'] = guid
folder_name = f'sessions/{guid}'
os.makedirs(folder_name, exist_ok=True)
context['domainRoot'] = os.path.dirname(os.path.abspath(__file__))
context['taskSource'] = taskSource
context['taskName'] = taskName


# add session id to configuration
config = luigi.configuration.LuigiConfigParser.instance()
config.set('session', 'id', guid)

# save context as pickle
with open(f'{folder_name}/context.pickle', 'wb') as handle:
    pickle.dump(context, handle, protocol=pickle.HIGHEST_PROTOCOL)
# start the flow
config = luigi.configuration.LuigiConfigParser.instance()

# create the arguments
params = {}
for i, arg in enumerate(sys.argv):
    if arg.startswith('--'):
        key = arg[2:]
        if i+1 < len(sys.argv) and not sys.argv[i+1].startswith('--'):
            params[key] = sys.argv[i+1]

# print the tree
import luigi.tools.deps_tree as deps_tree
task_obj = task_class(**params)
print(deps_tree.print_tree(task_obj))

# build the tree
luigi.build([task_obj], local_scheduler=True, detailed_summary=False)
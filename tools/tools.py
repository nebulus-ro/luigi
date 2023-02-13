import os
import importlib
import luigi
import pickle
import luigi.tools.deps_tree as deps_tree


def find_folder(start_with, path):
    for dir in os.listdir(path):
        if os.path.isdir(os.path.join(path, dir)) and dir.startswith(start_with):
            yield dir

# create the arguments
def get_task_params(args):
    params = {}
    for i, arg in enumerate(args):
        if arg.startswith('--'):
            key = arg[2:]
            if i+1 < len(args) and not args[i+1].startswith('--'):
                params[key] = args[i+1]
    return params

# check for a valid session
def get_session(prefix):
    guids = list(find_folder(prefix, './sessions'))
    if guids:
        if len(guids) > 1:
            print(f'Too many sessions start with: {prefix}. Try a longer sequence.')
            return False, None
    else:
        print(f'No session starts with: {prefix}')
        return False, None        
    guid = guids[0]
    return True, guid

# instantiating the root task
def get_roottask(context):
    module = importlib.import_module(f'tasks.{context["taskSource"]}')
    task_class = getattr(module, context['taskName'])
    task_obj = task_class(**context['taskParams'])
    return task_obj

def create_session(context):
    session_path = f'sessions/{context["sessionId"]}'
    os.makedirs(session_path, exist_ok=True)
    with open(f'{session_path}/context.pickle', 'wb') as handle:
        pickle.dump(context, handle, protocol = pickle.HIGHEST_PROTOCOL)

# load context 
def load_context(sessionId):
    with open(f'sessions/{sessionId}/context.pickle', 'rb') as handle:
        return pickle.load(handle)

# start luigi (for CLI with a context object and a sessionID)
def start_luigi(context, sessionId):
    # add session id to configuration
    # it is the way we communicate our modified environment to a luigi.task
    config = luigi.configuration.LuigiConfigParser.instance()
    config.set('session', 'id', sessionId)
    # instantiating the root task
    task_obj = get_roottask(context)
    # print the tree
    print('\n', deps_tree.print_tree(task_obj), '\n')
    # build/run the tree
    luigi.build([task_obj], local_scheduler=True, detailed_summary=False)


# just print the luigi tree (for CLI with a context object and a sessionID)
def status_luigi(context, sessionId):
    # add session id to configuration
    # it is the way we communicate our modified environment to a luigi.task
    config = luigi.configuration.LuigiConfigParser.instance()
    config.set('session', 'id', sessionId)
    # instantiating the root task
    task_obj = get_roottask(context)
    # print the tree
    print('\n', deps_tree.print_tree(task_obj), '\n')

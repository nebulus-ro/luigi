import os
import sys
import uuid
from tools import tools

# CLI.param1: starting task identification (module.name)
taskSource, taskName = sys.argv[1].split('.')
# CLI.param2: always the userId
userId = sys.argv[2]

print("Head Task:", taskSource, taskName)
print("User:", userId)

# create a context for the run and save it as a pickle
context = {}
sessionId = str(uuid.uuid4())
context['sessionId'] = sessionId
context['domainRoot'] = os.path.dirname(os.path.abspath(__file__))
context['taskSource'] = taskSource
context['taskName'] = taskName
context['userId'] = userId
context['taskParams'] = tools.get_task_params(sys.argv[3:])

# prepare a new session
tools.create_session(context, sessionId)

# now show the luigi tree and run the flow
tools.start_luigi(context, sessionId)
import sys
from tools import tools

# CLI.param1: starting task identification (session prefix)
prefix = sys.argv[1]
# CLI.param2: always the userId
userId = sys.argv[2]

# if just one session was found starting with the prefix the continue
isUnique, sessionId = tools.get_session(prefix)
if not isUnique: exit(2)

print("Resume session:", sessionId)

# load session's context
context = tools.load_context(sessionId)

print("Head task:", context['taskSource'], context['taskName'])
print("User:", userId)

# if not the same user task will not start
if not userId == context['userId']:
    print('ERROR: Current user is not the same as the initiator.')
    exit(1)

# now show the luigi tree and run the flow
tools.start_luigi(context, sessionId)
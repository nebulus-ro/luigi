import sys
from tools import tools

# CLI.param1: starting task identification (session prefix)
prefix = sys.argv[1]
# CLI.param2: always the userId
userId = sys.argv[2]
isHTML = "-html" in sys.argv

# if just one session was found starting with the prefix the continue
isUnique, sessionId = tools.get_session(prefix)
if not isUnique: exit(2)

print("Session:", sessionId)

# load session's context
context = tools.load_context(sessionId)

print("Head task:", context['taskSource'], context['taskName'])
print("User:", userId)

# if not the same user task will not start
if not userId == context['userId']:
    print('ERROR: Current user is not the same as the initiator.')
    exit(1)

# print the luigi tree
tools.status_luigi(context, sessionId, isHTML=isHTML)
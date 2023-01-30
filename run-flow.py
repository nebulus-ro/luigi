import platform
import os
import sys
import importlib

# system = platform.system()

# if system == "Windows":
#   print("RUN FLOW - Running on Windows")
#   # Windows specific commands
#   os.system("dir")
# elif system == "Linux":
#   print("RUN FLOW - Running on Unix-based system")
#   # Unix-based system specific commands
#   os.system("ls")


# if len(sys.argv) != 3:
#     print("Usage: run-flow.py <filename.taskname> <user>")
#     sys.exit(1)

taskSource, taskName = sys.argv[1].split('.')
userId = sys.argv[2]

print("Task:", taskSource, taskName)
print("User:", userId)

module = importlib.import_module(f'tasks.{taskSource}')
task_class = getattr(module, taskName)
task = task_class()
task.run()
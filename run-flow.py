import platform
import os

system = platform.system()

if system == "Windows":
  print("RUN FLOW - Running on Windows")
  # Windows specific commands
  os.system("dir")
elif system == "Linux":
  print("RUN FLOW - Running on Unix-based system")
  # Unix-based system specific commands
  os.system("ls")
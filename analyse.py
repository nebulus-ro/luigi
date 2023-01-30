import platform
import os

system = platform.system()

if system == "Windows":
  print("ANALYSE - Running on Windows")
  # Windows specific commands
  os.system("dir")
elif system == "Linux":
  print("ANALYSE - Running on Unix-based system")
  # Unix-based system specific commands
  os.system("ls")
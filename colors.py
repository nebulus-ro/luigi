import platform
import os

system = platform.system()

if system == "Windows":
	# Windows specific color code
	class bcolors:
		BLACK = '0'
		DARK_BLUE = '1'
		DARK_GREEN = '2'
		DARK_CYAN = '3'
		DARK_RED = '4'
		DARK_PURPLE = '5'
		DARK_YELLOW = '6'
		GRAY = '7'
		DARK_GRAY = '8'
		BLUE = '9'
		GREEN = 'A'
		CYAN = 'B'
		RED = 'C'
		PURPLE = 'D'
		YELLOW = 'E'
		WHITE = 'F'
elif system == "Linux":
	# Unix-based system specific color code
	class bcolors:
		BLACK = '\033[30m'
		DARK_BLUE ='\033[34m'
		DARK_GREEN = '\033[32m'
		DARK_CYAN = '\033[36m'
		DARK_RED = '\033[31m'
		DARK_PURPLE = '\033[35m'
		DARK_YELLOW = '\033[33m'
		GRAY = '\033[37m'
		DARK_GRAY ='\033[90m'
		BLUE = '\033[94m'
		GREEN = '\033[92m'
		CYAN = '\033[96m'
		RED = '\033[91m'
		PURPLE = '\033[95m'
		YELLOW = '\033[93m'
		WHITE = '\033[97m'

def set_color(color: bcolors):
	if system == "Windows":
		# in windows cmd is changing the entire console
		os.system(f"color {color}")
	else:
		print(color)

set_color(bcolors.GREEN)
print("HEADER text")

set_color(bcolors.BLUE)
print("OKBLUE text")

set_color(bcolors.YELLOW)
print("OKGREEN text")

set_color(bcolors.RED)
print("WARNING text")

set_color(bcolors.WHITE)

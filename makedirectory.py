import os
import sys


path1 = raw_input("Enter directory name: ")

try:
	os.makedirs(path1)

except OSError:
	if not os.path.isdir(path1)
		pass # success
	else:
		raise # Error occured 

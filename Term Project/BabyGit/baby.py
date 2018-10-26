'''
This class will handle:
	1) creation of a BabyGit repo (invoked by alias)
	2) pushing updates to your current repo
	3) pulling the most current updates from repo
	4) cloning a BabyGit repo from the server
'''
#!/usr/bin/python
from Client import *
import sys
import os


# Client instance
user = cli

def repoInit(directory, **name):
	
	if name:
		print(name)

	cwd_after_init = directory + "/.babygit"
	
	# Setup hidden babygit repo file if it does not exist
	try:
		absolute_path = directory + "/.babygit"
		os.makedirs(absolute_path, exist_ok=False)
	except:
		print("This directory is already initialized")
	
	# Create HEAD directory
	absolute_path = absolute_path + "/HEAD"
	os.makedirs(absolute_path, exist_ok=True)

	# now that the directories have been created, we need to upload them
	# to the server

	
	# Print if success
	success_msg = "Initialized empty BabyGit repository in " + cwd_after_init + "/"
	print(success_msg)
	

cwd = (os.getcwd())

args = sys.argv[1:]
command = args[0]

# Creating new BabyGit repos
if command == "init":
	
	absolute_path = cwd + "/" 
	
	if len(args) > 1:
		# Create repo as a new directory.
		repo_name = args[1]
		#absolute_path = absolute_path + repo_name
		#os.makedirs(absolute_path, exist_ok=False)
	
		# Init newly created repo
		repoInit(absolute_path, name=repo_name)		
	else:
		# create unnamed repo here
		repoInit(absolute_path)


'''
This class will handle:
	1) creation of a BabyGit repo (invoked by alias)
	2) pushing updates to your current repo
	3) pulling the most current updates from repo
	4) cloning a BabyGit repo from the server
'''
#!/usr/bin/python
import sys
import os


# Create a new client instance
user = Client()



def repoInit(directory):
	
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
	
	# Print if success
	success_msg = "Initialized empty BabyGit repository in " + cwd_after_init + "/"
	print(success_msg)
	

cwd = (os.getcwd())

args = sys.argv[1:]
command = args[0]

if command == "init":
	
	absolute_path = cwd + "/" 
	
	if len(args) > 1:
		# Create repo as a new directory.
		repo_name = args[1]
		absolute_path = absolute_path + repo_name
		os.makedirs(absolute_path, exist_ok=False)
	
		# Now that the main repo exists, create the .babygit directory
		# since this used twice, a method will be created for it
		repoInit(absolute_path)		
	else:
		# create unnamed repo here
		repoInit(absolute_path)


'''
This class will handle:
	1) creation of a BabyGit repo (invoked by alias)
	2) pushing updates to your current repo
	3) pulling the most current updates from repo
	4) cloning a BabyGit repo from the server

@author Ron Rounsifer, Bryce Hutton
@version 10.27.2018 (10.26.2018)
'''
#!/usr/bin/python
from client import *
import sys
import os
import gzip
import re


class Baby(Client):
	def __init__(self, initArgs):
		self.args = initArgs
		command = args[0]

		self.cwd = os.getcwd()
		self.directory = self.cwd + "/"
		self.head = (self.directory + "/repo\\.babygit\\HEAD") 

		parsed_lines = self.__headParse()
		self.baby_files = parsed_lines[1]
		self.last_version = parsed_lines[2]
		
		self.parseCommand(command)
		
	def parseCommand(self, command):
		print command
		if command == "init":
			repo_name = None
			# Assign name to repo if passed
			if len(args) == 2:
				repo_name = args[1]
			# Initialize the repository
			self.repoInit(repo_name)
		elif command == "stage":
			self.stage()
		elif command == "commit":

			self.commit()
		elif command == "push":
			pass
		
		

	#### Method Definitions ####
	def stage(self):
		#todo
		pass

	'''Commit changes to the file.'''
	def commit(self):
		# Initialize the repository
		#todo: Change the version.
		version = str(self.last_version+1)
		print(version)
		destfile = self.directory + "repo" + "\\.babygit" + "\\vers" + str(version)
		os.makedirs(destfile)
		fhead = open(self.head, "a")
		fhead.write("\nvers"+ version)
		fhead.close()

		'''For each file in the directory that is listed and staged in the git file'''
		for filename in os.listdir(self.cwd):
			#Todo: If statement a placeholder for checking if the file has been staged
			print filename
			if (filename in self.baby_files):
			#If the file is not a directory
				if os.path.isfile(os.path.join(self.directory,filename)):
					self.__compileFile(filename, destfile + "\\" +
					 filename + '.' + version + '.bby')


	# Function checks to see if the file is version controlled by baby
	def __headParse(self):
		header = open(self.head)
		temp = header.read()
		contents = temp.split()
		#print contents
		#lines = contents.split()
		listing_files = False
		version_counting = False
		last_version = 0
		current_head = 0
		listed_files = []
		#todo add functionality to find the currenthead
		for line in contents:
			if line == "STARTLIST":
				listing_files = True
			elif line == "ENDLIST":
				listing_files = False
			elif line == "LASTVER":
				print "here at last"
				version_counting = True
			else:
				if listing_files:
					listed_files.append(line)
				# Gets the number of the last version created.
				elif version_counting:
					x = int(re.search(r'\d+', line).group())
					print("vers:" + str(x))
					if x > last_version:
						last_version = x
		headargs = [current_head, listed_files, last_version]
		header.close()
		return headargs


	# Given a file and a destination this function compiles and creates a new file
	def __compileFile(self, filename, new_filename):
		fin = open(filename)
		#Todo: Add identifier for the file
		#todo: Maybe a specific identifier for each repo cloned
		#todo: Then an identifier for each version from that repo
		fout = gzip.open(new_filename, 'wb')
		fout.writelines(fin)
		fout.close()
		fin.close()



	def repoInit(self, name):
		'''Initialize a BabyGit repository
		
		[description]
		
		Arguments:
			directory {[type]} -- the current working directory of the user.
			name {str} -- the name of the repository to be made.
						  Defaults to current directory if not passed.
		'''

		# Now we must get the intialized repositories onto the server.
		# 
		# 2 options:
		#	1) Create files server side and pull to client
		#		- USING THIS MODEL
		#   2) Create files client side and send to server
		#		- if 2+ people make the same repo it could cause problems


		cwd = (os.getcwd())

		directory = cwd + "\\"
		
		# Initialize named repo created in the current directory
		if name != None:

			# Absolute path for repo to create
			repo_name = name
			directory = directory + repo_name
			directory_after_init = directory + "\\.babygit"
		
			# Setup hidden babygit repo file if it does not exist
			try:
				# Create .babygit directory
				absolute_path = directory + "\\.babygit"
				os.makedirs(absolute_path, exist_ok=False)

				# Create HEAD directory
				absolute_path = directory + "\\HEAD"
				os.makedirs(absolute_path, exist_ok=False)

			except:
				print("This directory is already initialized." +
					"\nDelete all BabyGit related files and try again.")

		# Initialize the current directory
		else:
			#todo figure out what you want repo_name to be named
			repo_name = "repo"
			directory_after_init = directory + "\\.babygit"
		
			# Setup hidden babygit repo file if it does not exist
			try:

				# Create .babygit directory
				absolute_path = directory + repo_name + "\\.babygit"
				print absolute_path
				os.makedirs(absolute_path, exist_ok=False)

				# Create HEAD directory
				absolute_path = absolute_path + "\\HEAD"
				os.makedirs(absolute_path, exist_ok=True)

			except:
				print("This directory is already initialized." +
					"\nDelete all BabyGit related files and try again.")
		

			# now that the directories have been created, we need to upload them
			# to the server

		
		# Print if success
		success_msg = "Initialized empty BabyGit repository in " + directory_after_init + "/"
		print(success_msg)


#### Script ####
args = []
args.append("commit")
#args = sys.argv[1:]
b = Baby(args)
'''
# Initialize a BabyGit repo
if command == "init":
	# Assign name to repo if passed
	if len(args) == 2:
		repo_name = args[1]
	else:
		repo_name = None
	# Initialize the repository
	repoInit(repo_name)
'''


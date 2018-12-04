'''
This class will handle:
	1) creation of a BabyGit repo (invoked by alias)
	2) pushing updates to your current repo
	3) pulling the most current updates from repo
	4) cloning a BabyGit repo from the server

@author Ron Rounsifer, Bryce Hutton
@version 10.27.2018 (10.26.2018)
'''
# !/usr/bin/python
from client import *
import sys
import os
import gzip
import re
import datetime


class Baby(Client):
    def __init__(self, initArgs):
        #todo: we can probably add most of these into two dictionaries.
        #todo: dictionary header information, dict directory information.
        self.args = initArgs
        command = self.args[0]
        self.host_address = "0.0.0.0"
        self.cwd = os.getcwd()
        self.directory = self.cwd + "/"
        self.bbydir = self.directory + ".babygit"
        self.head = (self.directory + ".babygit/HEAD.ibby")
        self.user = "Bryce"
        self.repoName = "babygit"
        #todo add user to parse
        # file_list_index is the index of where the list of files in version control in the header ends.
        self.file_list_end_index = None
        self.file_contents = None
        self.baby_files = None
        self.last_version = None
        self.local_head = None

        self.parseCommand(command)

    '''Parses the argument passed in with the baby command to the git function.'''
    def parseCommand(self, command):
        if command == "init":
            repo_name = None
            # Assign name to repo if passed
            if len(self.args) == 2:
                repo_name = self.args[1]
            # Initialize the repository
            self.repoInit(repo_name)
        else:
            self.__headParse()
        if command == "stage":
            if len(self.args) == 2:
                self.stage(self.args[1])
        elif command == "commit":
                self.commit()
        elif command == "push":
            self.push()
            pass
        elif command == "clone":
            pass
        elif command == "checkout":
            pass
        elif command == "branch":  # Are we adding branch to our program?
            pass

    #### Method Definitions ####
    '''Stage stages the file by adding it to the head. Doesn't add directories.'''
    #todo add ability to stage directories.
    def stage(self, filename):
        fhead = open(self.head, "w")
        if (os.path.isfile(filename)):
            self.file_contents.insert(self.file_list_end_index, filename)
            str1 = '\n'.join(self.file_contents)
            fhead.write(str1)
        else:
            print(filename + "does not exist in this directory.")
        fhead.close()
        pass

    '''Commit changes to the file.'''
    def commit(self):
        # Initialize the repository
        # todo: Change the version.
        version = str(self.last_version + 1)
        destfile = self.directory + ".babygit" + "\\vers" + str(version)
        os.makedirs(destfile)

        message = ""

        #If there was no comment added to the commit.
        if len(self.args) == 1:
            message = input("Please enter description for commit: ")
        elif len(self.args) == 2:
            message = self.args[1]
        else:
            print("Incorrect commit comment format. Either put comment in between "
                  "\"quotes\" or leave comment empty")

        fhead = open(self.head, "w")
        self.file_contents[1] = "vers"+version
        self.file_contents.append("vers"+version)
        str1 = '\n'.join(self.file_contents)
        fhead.write(str1)
        '''
        fhead = open(self.head, "a")
        fhead.write("\nvers" + version)
        '''
        fhead.close()
        comment = open(destfile + "/" ".comment.ibby", 'w')
        comment.write("REPO:" + self.repoName+ "\n")
        comment.write("TIME:" + str(datetime.datetime.now()) + "\n")
        comment.write("USER:"+self.user+ "\n")
        comment.write("VERS:"+version+ "\n")
        comment.write("-COMMENT-"+ "\n")
        comment.write(message+ "\n")
        comment.write("-ENDCOMMENT-"+ "\n")


        '''For each file in the directory that is listed and staged in the git file, compress it'''
        print("Committing files:")
        for filename in os.listdir(self.cwd):
            if (filename in self.baby_files):
                print("+ " + filename)
                # If the file is not a directory
                if os.path.isfile(os.path.join(self.directory, filename)):
                    self.__compileFile(filename, destfile + "/" +
                                       filename + '.' + version + '.bby')


    '''Pushes the file to the remote server.'''
    def push(self):
        os.chdir(self.bbydir)
        super(Baby, self).__init__(self.host_address, self.user)
        try:
            self.ftp.mkd(self.user + "vers" + str(self.last_version))
            self.ftp.cwd(self.user + "vers" + str(self.last_version))
        except:
            print("This version already exists on the server.")
            return
        self.pushLoop(self.cwd + "/.babygit/", self.cwd + "/.babygit/")
        self.ftp.quit()

    '''Recursive loop that pushes files and directories within babygit.'''
    def pushLoop(self, file, curdir):
        for filename in os.listdir(file):
            if os.path.isfile(os.path.join(curdir, filename)):
                self.uploadFile(filename)
            elif os.path.isdir(os.path.join(curdir, filename)):
                self.ftp.mkd(filename)
                self.ftp.cwd(filename)
                curdir1 = curdir + "/" + filename
                os.chdir(curdir1)
                self.pushLoop(file + filename, curdir1)
                self.ftp.cwd("..")
                os.chdir("..")

    # Function checks to see if the file is version controlled by baby
    def __headParse(self):
        header = open(self.head, 'r')
        temp = header.read()
        contents = temp.split()
        listing_files = False
        version_counting = False
        last_version = 0
        listed_files = []
        # todo add functionality to find the currenthead
        # Todo Occasionally after switching to a different command the headparse no longer goes through correctly.
        index = 0
        for line in contents:
            if line == "-STARTLIST":
                listing_files = True
            elif line == "-ENDLIST":
                listing_files = False
                self.file_list_end_index = index
            elif line == "-LASTVER":
                version_counting = True
            elif line == "-HOSTNAME":
                self.host_address = contents[index+1]
            elif line == "-LOCALHEAD":
                self.local_head = contents[index+1]
            else:
                if listing_files:
                    listed_files.append(line)
                # Gets the number of the last version created.
                elif version_counting:
                    x = int(re.search(r'\d+', line).group())
                    if x > last_version:
                        last_version = x
            index += 1
        self.file_contents = contents
        self.baby_files = listed_files
        self.last_version = last_version
        header.close()
        return

    # Given a file and a destination this function compiles and creates a new file
    def __compileFile(self, filename, new_filename):
        fin = open(filename, 'rb')
        # Todo: Add identifier for the file
        # todo: Maybe a specific identifier for each repo cloned
        # todo: Then an identifier for each version from that repo
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

        directory = cwd + "/"

        # Initialize named repo created in the current directory
        if name != None:

            # Absolute path for repo to create
            repo_name = name
            directory = directory + repo_name
            directory_after_init = directory + "/.babygit"

            # Setup hidden babygit repo file if it does not exist
            try:
                # Create .babygit directory
                absolute_path = directory + "/.babygit"
                os.makedirs(absolute_path, exist_ok=False)

                # Create HEAD.ibby directory
                absolute_path = directory + "/HEAD.ibby"
                os.makedirs(absolute_path, exist_ok=False)

            except:
                print("This directory is already initialized." +
                      "\nDelete all BabyGit related files and try again.")

        # Initialize the current directory
        else:
            # todo figure out what you want repo_name to be named
            repo_name = "repo"
            directory_after_init = directory + "/.babygit"

            # Setup hidden babygit repo file if it does not exist
            try:

                # Create .babygit directory
                absolute_path = directory + repo_name + "/.babygit"
                print(absolute_path)
                os.makedirs(absolute_path, exist_ok=False)

                # Create HEAD.ibby directory
                absolute_path = absolute_path + "\\HEAD.ibby"
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
args1 = []
#args1.append("commit")
#args1.append("testfile.txt")
args1 = sys.argv[1:]
b = Baby(args1)
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

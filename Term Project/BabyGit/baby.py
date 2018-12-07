"""
This class will handle:
	1) creation of a BabyGit repo (invoked by alias)
	2) pushing updates to your current repo
	3) pulling the most current updates from repo
	4) cloning a BabyGit repo from the server

@author Ron Rounsifer, Bryce Hutton
@version 12.04.2018 (10.26.2018)
"""
# !/usr/bin/python
from client import *
import sys
import os
import gzip
import re
import datetime
import shutil


class Baby(Client):

    def __init__(self, init_args):
        """Constructor

        Constructs a baby class.

        Args:
            init_args: command line arguments passed by user
        """
        # todo: we can probably add most of these into two dictionaries.
        # todo: dictionary header information, dict directory information.
        self.args = init_args
        command = self.args[0]
        self.host_address = "0.0.0.0"
        self.cwd = os.getcwd()
        self.directory = self.cwd + "/"
        self.bby_dir = self.directory + ".babygit"
        self.head = (self.directory + ".babygit/HEAD.ibby")
        self.user = "anon"
        self.repo_name = "babygit"
        # todo add user to parse
        # file_list_index is the index of where the list of files in version control in the header ends.
        self.file_list_end_index = None
        self.file_contents = None
        self.baby_files = None
        self.last_version = None
        self.local_head = None
        self.parseCommand(command)

    def parseCommand(self, command):
        """Parse user arguments

        Parses the argument passed in with the baby command to the git function.

        Args:
            command: the command entered by the user
        """
        command = command.lower()

        if command in ['init', 'make']:  # parse arguments and create repos before parsing head file
            local_switch = False

            # User must pass username to init repo
            if len(self.args) == 3:
                repo_name = self.args[1]
                self.user = self.args[2]
                self.repoInit(repo_name, local_switch)
                self.__headParse(repo_name)

            elif len(self.args) == 4:
                repo_name = self.args[1]
                self.user = self.args[2]
                local_flag = self.args[3]

                if local_flag in ['local', 'l', '-l']:
                    local_switch = True

                self.repoInit(repo_name, local_switch)
                self.__headParse(repo_name)

            else:

                print("WARNING: Incorrect command format. Try the format below.")
                print("baby init [name of repository] [username] [-l : only init locally]")

        elif command == "stage": # parse header file and args before staging changes to head file
            self.head = os.getcwd() + '/.babygit/HEAD.ibby'
            self.__headParse(None)

            if len(self.args) == 2:
                self.stage(self.args[1])

        elif command == "commit":  # parse header file and commit changes

            self.head = os.getcwd() + '/.babygit/HEAD.ibby'
            self.__headParse(None)
            if len(self.args) == 2:
                self.user = self.args[1]
            self.commit()

        elif command == "push":  # parse header file and push to remote repo

            self.head = os.getcwd() + '/.babygit/HEAD.ibby'
            self.__headParse(None)
            self.push()
            pass

        elif command == "clone":  # gather arguments and pull the remote repo

            remote_repo = self.args[1]
            self.user = self.args[2]
            self.repo_name = remote_repo
            self.clone(remote_repo)
            pass

        elif command == 'unzip':  # unzip files to work on

            self.decompressFiles()

        elif command == "user":  # change the current user in the session

            self.head = os.getcwd() + '/.babygit/HEAD.ibby'
            print(self.head)
            self.__headParse(None)
            self.userChange()

        elif command == "help":  # request for list of commands

            print("Command list:\ninit: initialize a repo.\nstage: stage a file."
                  "\ncommit: commit changes.\npush: push changes to remote. \nuser: change user")
            # todo add the rest of the commands as we complete them.

        else:
            print("Command not recognized. Use command \"help\" for more information.")

    def repoInit(self, name, local):
        """Initialize a BabyGit repository

        Args:
            directory:  the current working directory of the user.
            name:   the name of the repository to be made.
                    Defaults to current directory if not passed.

        Returns:
            None
        """
        cwd = (os.getcwd())
        directory = cwd + "/"

        self.repo_name = name
        only_a_local_repo = local

        # Absolute path for repo to create
        directory = directory + self.repo_name
        directory_after_init = directory + "/.babygit"

        # Setup hidden babygit repo file if it does not exist
        try:
            # Create .babygit directory
            absolute_path = directory + "/.babygit"
            os.makedirs(absolute_path, exist_ok=False)

            # Create template HEAD.ibby file
            head_file_path = absolute_path + "/HEAD.ibby"
            self.createInitialHeadFile(head_file_path)
            self.head = head_file_path

        except Exception as e:
            print("This directory may already be initialized." +
                  "\nTry deleting all BabyGit related files and try again.")
            print(e)
            return

        # Print if success
        success_msg = f"""Initialized local empty BabyGit repository in {directory_after_init}/"""
        print(success_msg)

        # Create the remote repo if wanted
        if not only_a_local_repo:
            os.chdir(cwd)
            super(Baby, self).__init__(self.host_address, self.user)

            # Try to make a directory server-side.
            # Alert user if it already exists.
            try:

                # Create remote directories
                self.ftp.mkd(self.repo_name)
                self.ftp.cwd(self.repo_name)
                self.ftp.mkd('.babygit')
                self.ftp.cwd('.babygit')

                # Only try to send the head file if it exists
                if os.path.isfile(head_file_path):
                    self.head = head_file_path
                    os.chdir(cwd + '/' + self.repo_name + '/.babygit/')
                    try:
                        self.ftp.storbinary('STOR HEAD.ibby', open('HEAD.ibby', 'rb'))
                    except Exception as e:
                        print("Could not upload head file to remote repository.")

                # Close connection
                self.ftp.quit()

            except Exception as e:
                print("This repository may already exist.")
                print(e)
                return

            # Print if success
            success_msg = "Initialized an empty remote BabyGit repository for you."
            print(success_msg)

    def createInitialHeadFile(self, path):
        """Create empty head file

        Called by the repoInit() method. Creates a blank slate head file
        for each new BabyGit repository that is created.

        Args:
            path: the location of the header file
        """
        template = "-LOCALHEAD\nvers0\n" + \
                   "-REMOTEHEAD\nvers0\n" + \
                   "-USER\n" + \
                   str(self.user) + "\n" + \
                   "-REPONAME\n" + \
                   str(self.repo_name) + "\n" + \
                   "-HOSTNAME\nlocalhost\n" + \
                   "-LISTEDFILES\n" + \
                   "-STARTLIST\n" + \
                   "-ENDLIST\n" + \
                   "-LASTVER\nvers0\n"

        with open(path, 'w+') as f:
            f.write(template)

    def stage(self, filename):
        """Stages file
        Stages the file by writing it to the head file.

        Args:
            filename: the file to stage
        """
        fhead = open(self.head, "w")
        # if the file isn't a directory, rewrite the head with the new file added.
        # todo add ability to stage directories.
        if (os.path.isfile(filename)):
            self.file_contents.insert(self.file_list_end_index, filename)
            str1 = '\n'.join(self.file_contents)
            fhead.write(str1)
        else:
            print(filename + " does not exist in this directory.")
        fhead.close()
        pass



    def commit(self):
        """Commit changes.

        Commits the changes to the file by adding this version as the last version of the head file before running
        through all babygit files and compressing them.

        Returns:
            None
        """
        # Initialize the repository
        # todo: Change the version, pref to hash of time & user to make unique.
        version = str(self.last_version + 1)
        destfile = self.directory + ".babygit" + "/vers" + str(version)
        os.makedirs(destfile)

        message = ""

        # create a comment for the commit.
        if len(self.args) == 2:
            message = input("Please enter description for commit: ")
        else:
            print("Incorrect commit comment format.\nbaby commit [username]")

        # Update the last version in the head file.
        fhead = open(self.head, "w")
        self.file_contents[1] = "vers" + version
        self.file_contents.append("vers" + version)
        str1 = '\n'.join(self.file_contents)
        fhead.write(str1)
        fhead.close()

        # Create a comment file w/ relevant information.
        comment = open(destfile + "/" ".comment.ibby", 'w')
        comment.write("REPO:" + self.repo_name + "\n")
        comment.write("TIME:" + str(datetime.datetime.now()) + "\n")
        comment.write("USER:" + self.user + "\n")
        comment.write("VERS:" + version + "\n")
        comment.write("-COMMENT-" + "\n")
        comment.write(message + "\n")
        comment.write("-ENDCOMMENT-" + "\n")

        # For each file in the directory that is listed and staged in the git file, compress it
        print("Committing files:")
        for filename in os.listdir(self.cwd):
            if (filename in self.baby_files):
                print("+ " + filename)
                # If the file is not a directory
                # todo add directory commit
                if os.path.isfile(os.path.join(self.directory, filename)):
                    self.__compileFile(filename, destfile + "/" +
                                       filename + '.' + version + '.bby')

    def clone(self, repo_name):
        try:
            super(Baby, self).__init__(self.host_address, self.user)
            self.ftp.cwd(repo_name + '/')
            if os.path.isdir(repo_name):
                os.chdir(repo_name)
            else:
                os.mkdir(repo_name + '/')
                os.chdir(repo_name)

        except Exception as e:
            print(e)
        self.cloneLoop()

    def cloneLoop(self):
        for filename in self.ftp.nlst():

            directory = True
            try:
                self.ftp.cwd(filename)
                os.mkdir(filename)
                os.chdir(filename)
                self.cloneLoop()
                self.ftp.cwd('..')
                os.chdir('..')
            except Exception as e:
                directory = False

            if not directory:
                local_path = os.path.join(os.getcwd() + '/', filename)
                f = open(local_path, 'wb')
                self.ftp.retrbinary('RETR ' + filename, f.write)
                f.close()

    def decompressFiles(self):
        """Unzip downloaded

        This helper method is used to unzip the files that the user wishes to work on.
        Only a valid command inside of the desired directory of the version the user wishes
        to view/edit.
        """
        for file in os.listdir('.'):
            if file[0] == '.':
                pass
            elif file[-4:] == '.bby':
                with gzip.open(file, 'r') as f_in, open(file[:-6], 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                    path_to_uncompressed_file = os.path.abspath(file[:-6])
                    this_directory = os.getcwd()
                    os.chdir('..')
                    os.chdir('..')
                    shutil.move(path_to_uncompressed_file, os.getcwd())
                    os.chdir(this_directory)

    def push(self):
        """Push files to remote repository.

        Creates an FTP connection with the remote repository before calling the pushLoop() method
        that recursively pushes all files in the current directory to the remote repository.

        Returns:
            None
        """

        os.chdir(self.bby_dir)
        repo_name = self.file_contents[7]

        try:
            super(Baby, self).__init__(self.host_address, self.user)
            self.ftp.cwd(repo_name + '/.babygit')
        except Exception as e:
            print(e)

        self.pushLoop(self.cwd + "/.babygit/", self.cwd + "/.babygit/")
        self.ftp.quit()

    def pushLoop(self, file, curdir):
        """ Recurse through all files in directory.

        Recursively loop that pushes files and directories within babygit.

        Args:
            File: The file to start the recursive loop on
            curdir: The users current directory

        Returns:
            None
        """
        for file_name in os.listdir(file):
            # If the file is of type File
            # upload to remote repository
            if os.path.isfile(os.path.join(curdir, file_name)):
                self.uploadFile(file_name)
            # If the file is of type Directory:
            #   1 - Make a new directory server-side
            #   2 - Switch client and server cwd to this directory
            #   3 - Recurse through files in this new directory
            #   4 - Return to previous directory after complete recursion.
            elif os.path.isdir(os.path.join(curdir, file_name)):

                # Only make directory if it doesn't exist
                if file_name in self.ftp.nlst():
                    self.ftp.cwd(file_name)
                else:
                    self.ftp.mkd(file_name)
                    self.ftp.cwd(file_name)

                curdir1 = curdir + "/" + file_name
                os.chdir(curdir1)
                self.pushLoop(file + file_name, curdir1)
                self.ftp.cwd("..")
                os.chdir("..")

    def userChange(self):
        """Change user.

        Changes the users name in the head file.

        Returns:
            None
        """
        fhead = open(self.head, "w")
        new_name = None
        if len(self.args) == 1:
            new_name = input("Username: ")
            print(new_name)
            print(type(new_name))
        elif len(self.args) == 2:
            new_name = self.args[1]
        else:
            print("Too many arguments entered. Try again.")
            fhead.close()
            return
        self.file_contents[5] = new_name
        str1 = '\n'.join(self.file_contents)
        fhead.write(str1)
        fhead.close()
        print("Username changed to " + new_name)

    def __headParse(self, repo_name):
        """ Parse head file

        Parses through the head file and grabs relevant information

        Returns:
            None
        """
        # Set head file location.
        # self.head = os.getcwd() + '/HEAD.ibby'
        header = open(self.head, 'r')
        temp = header.read()
        contents = temp.split()
        listing_files = False
        version_counting = False
        last_version = 0
        listed_files = []
        # todo add functionality to find the current head
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
                self.host_address = contents[index + 1]
            elif line == "-LOCALHEAD":
                self.local_head = contents[index + 1]
                last_version = int(re.search(r'\d+', self.local_head).group())
            elif line == "-USER":
                self.user = contents[index + 1]
            elif line == "-REPONAME":
                self.repo_name = contents[index + 1]
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

    def __compileFile(self, file_name, new_file_name):
        """Compile file/create new file

        Given a file and a destination this function compiles and creates a new file

        Args:
            file_name: Name of the file to compile
            new_file_name: the destination of the file being compiled

        Returns:
            None
        """
        fin = open(file_name, 'rb')
        # todo: add repo identifier for each repo cloned
        fout = gzip.open(new_file_name, 'wb')
        fout.writelines(fin)
        fout.close()
        fin.close()






#### Script ####
args1 = []
args1 = sys.argv[1:]
b = Baby(args1)

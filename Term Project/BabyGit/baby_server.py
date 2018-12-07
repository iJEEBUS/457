"""Server

The server class will host all of the files that a user wishes to 
manage with the BabyGit version control software.

@author Ron Rounsifer, Bryce Hutton
@version 10.27.2018 (10.26.2018)
"""
import os
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.authorizers import DummyAuthorizer


def main():
	"""Execution method
	
	Creates a Threaded server on the localhost with on the port 1515.
	Runs infinitely and accepts all client connections.
	"""
	cwd = os.getcwd()
	directory = 'D:\\github\\457\\Term Project\\BabyGit\\testrepo'

	# Make the directory if it does not exist
	if not os.path.isdir(directory):
		os.mkdir(directory)

	# Authorize the incoming client connection requests
	authorizer = DummyAuthorizer()

	# List of all users that can make changes to the remote repository.
	authorizer.add_user("Bryce", "12345", directory, perm="elradfmw")
	authorizer.add_user("Ron", "54321", directory, perm="elradfmw")

	# Create and define the client handler
	handler = FTPHandler
	handler.authorizer = authorizer
	server = ThreadedFTPServer(('',1515), handler)
	server.serve_forever()
	
if __name__ == "__main__":
	main()

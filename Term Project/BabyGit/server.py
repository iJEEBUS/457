import os
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.authorizers import DummyAuthorizer


def main():
	'''Execution method
	
	Creates a Threaded server on the localhost with on the port 1515.
	Runs infinitely and accepts all client connections.
	'''

	# Authorize the incoming client connection requests
	authorizer = DummyAuthorizer()
	authorizer.add_user("user", "12345", ".", perm="elradfmw")
	authorizer.add_anonymous('/Users/user/Desktop/')

	# Create and define the client handler
	handler = FTPHandler
	handler.authorizer = authorizer
	server = ThreadedFTPServer(('',1515), handler)
	server.serve_forever()
	
if __name__ == "__main__":
	main()

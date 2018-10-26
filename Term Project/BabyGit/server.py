import os
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.authorizers import DummyAuthorizer


def main():

	# Authorize the incoming client connection requests
	authorizer = DummyAuthorizer()
	authorizer.add_user("user", "12345", ".", perm="elradfmw")
	authorizer.add_anonymous('/Users/user/Desktop/')

	# Create and define the client handler
	handler = FTPHandler
	handler.authorizer = authorizer
	server = ThreadedFTPServer(('',1515), handler)
	server.serve_forever()
	
	# Create and run the threaded server instance
	# server = FTPServer(("127.0.0.1", 1515), handler)
	# server.serve_forever()

if __name__ == "__main__":
	main()

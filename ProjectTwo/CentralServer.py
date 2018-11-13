'''Server

The server class will host all of the files that a user wishes to 
manage with the BabyGit version control software.

@author Ron Rounsifer, Bryce Hutton
@version 11.12.2018 (10.26.2018)
'''
import os
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.authorizers import DummyAuthorizer

class ServerHandler(FTPHandler):

    def on_file_received(self, file):
        '''Populates databases with given information
        
        Given the xml file passed through, this method parses the information
         it contains and adds it to the corresponding data table in our database.
        
        Arguments:
            file File -- register / file_list file uploaded to server
        '''
        
        filename = os.path.basename(file.name)
        register = "register.xml"
        file_list = "filelist.xml"

        if filename == register:
            # Parse the xml file of the registering information
            # Add this information to the registered_users database table
            pass
        elif filename == file_list:
            # Parse the xml file of the filelist information
            # Add this to the file_list database table
            pass
        pass
        
def main():
    '''Execution method

    Creates a Threaded server on the localhost with on the port 1515.
    Runs infinitely and accepts all client connections.
    '''

    # Authorize the incoming client connection requests
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "12345", ".", perm="r")

    # Create and define the client handler
    handler = ServerHandler
    handler.authorizer = authorizer
    server = ThreadedFTPServer((""'', 1515), handler)
    server.serve_forever()


if __name__ == "__main__":
    main()

'''Server

The server class will host all of the files that a user wishes to 
manage with the BabyGit version control software.

@author Ron Rounsifer, Bryce Hutton
@version 11.12.2018 (10.26.2018)
'''
from ftplib import FTP
import os
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.authorizers import DummyAuthorizer

class ServerHandler(FTPHandler):
    registered_users = {}
    ftp = None

    def sendAckToPeer(self, hostname, port,  file):
        self.ftp = FTP()
        self.ftp.connect()
        self.ftp.login()
        self.ftp.cwd('.')

        self.ftp.storbinary('STOR' + file, open(file, 'rb'))



    def on_file_received(self, file):
        '''Populates databases with given information

        Given the xml file passed through, this method parses the information
         it contains and adds it to the corresponding data table in our database.

        Arguments:
            file File -- register / file_list file uploaded to server
        '''

        filename = os.path.basename(file)
        register = "registration.xml"
        file_list = "filelist.xml"

        root = xml.etree.ElementTree.parse(filename).getroot()

        if filename == register:
            # Parse the xml file of the registering information
            # Add this information to the registered_users database table
            root = xml.etree.ElementTree.parse(filename).getroot()
            username = root.attrib['name']
            local_host_address = root.attrib['host']
            connection_speed = root.attrib['speed']

            # Add the user to the dictionary if they
            # are not already in it
            if username not in self.registered_users.keys():
                self.registered_users[username] = {"hostname" : local_host_address, "speed" : connection_speed}
            else:
                # Create the error file and send it to the peer
                error_message = "This username is already registered."
                with open('failure.txt', 'w') as failure_file:
                    failure_file.write(error_message)
                    self.sendAckToPeer(failure_file)

                # Send the error file to the peer


        elif filename == file_list:
            if username not in self.registered_users.keys():
                print ("Please register your account before sharing files!")
            else:
                # Parse the xml file of the filelist information
                #  Add this to the file_list database table
                # SHOULD INCLUDE:
                # username, filenames, and file descriptions
                pass
        for x in self.registered_users:
            print(x)
        
def main():
    '''Execution method

    Creates a Threaded server on the localhost with on the port 1515.
    Runs infinitely and accepts all client connections.
    '''

    # Authorize the incoming client connection requests
    authorizer = DummyAuthorizer()
    # authorizer.add_user("user", "12345", ".", perm="rw")
    authorizer.add_anonymous('./data', perm="elradfmw")

    # Create and define the client handler
    handler = ServerHandler
    handler.authorizer = authorizer
    server = ThreadedFTPServer((""'', 1515), handler)
    server.serve_forever()


if __name__ == "__main__":
    main()

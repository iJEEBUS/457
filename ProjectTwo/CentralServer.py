"""Server

The server class will host all of the files that a user wishes to
manage with the BabyGit version control software.

@author Ron Rounsifer, Bryce Hutton
@version 11.17.2018 (10.26.2018)
"""
import os
import xml.etree.ElementTree
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.authorizers import DummyAuthorizer


class ServerHandler(FTPHandler):
    registered_users = {}
    shareable_files = {}

    def on_file_received(self, file):
        """Populates databases with given information

        Given the xml file passed through, this method parses the information
         it contains and adds it to the corresponding data table in our database.

        Arguments:
            file File -- register / file_list file uploaded to server
        """

        # make sure you are in the correct directory (data)
        if os.path.basename(os.getcwd()) != 'data':
            os.chdir('./data')

        filename = os.path.basename(file)
        register = "registration.xml"
        file_list = "filelist.xml"
        query_file = "query.xml"
        quit_file = "quit.xml"

        if filename == register:

            # Parse info from XML file
            root = xml.etree.ElementTree.parse(filename).getroot()
            username = root.attrib['name']
            local_host_address = root.attrib['host']
            connection_speed = root.attrib['speed']

            # Add to "registered_users" dictionary
            if username not in self.registered_users.keys():
                self.registered_users[username] = {"hostname": local_host_address, "speed": connection_speed}
                print("User " + "\"" + username + "\"" + " has joined")
            else:
                print("This username is already registered.")


        elif filename == file_list:

            if username not in self.registered_users.keys():
                print("Please register your account before sharing files!")
        elif filename == query_file:

            pass

        elif filename == quit_file:

            # Delete the user from the list of registered users
            root = xml.etree.ElementTree.parse(filename).getroot()
            username = root.attrib['name']
            del self.registered_users[username]

            # Remove quit file
            print("User " + "\"" + username + "\"" + " has left")


def main():
    """Execution method

    Creates a Threaded server on the localhost with on the port 1515.
    Runs infinitely and accepts all client connections.
    """

    # print(os.getcwd())
    # Authorize the incoming client connection requests
    authorizer = DummyAuthorizer()
    # authorizer.add_user("user", "12345", ".", perm="rw")
    authorizer.add_anonymous('./data', perm="elrafmw")

    # Create and define the client handler
    handler = ServerHandler
    handler.authorizer = authorizer
    server = ThreadedFTPServer((""'', 1515), handler)
    server.serve_forever()


if __name__ == "__main__":
    main()

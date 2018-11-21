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
    file_matches = []

    def sendQueryMatch(self, file, hostname, port, speed):
        """Creates a response to a user query

        If a file is found that matches the keyword search entered by the user
        then a query response is created and sent back the user.
        The response consists of the file location (hostname and port number),
        the filename, and the speed of download available.
        :param file:
        :param hostname:
        :param port:
        :param speed:
        """
        # Create XML file
        root = ET.Element("Response", filename=file, host=hostname, port=port, download_speed=speed)
        tree = ET.ElementTree(root)

        # Write the file
        tree.write("response.xml")

    def on_file_received(self, file):
        """Populates databases with given information

        Given the xml file passed through, this method parses the information
         it contains and adds it to the corresponding data table in our database.
        :param file:
        """

        filename = os.path.basename(file)
        register = "registration.xml"
        file_list = "filelist.xml"
        query = "query.xml"
        quit_file = "quit.xml"

        # Registers the user
        if filename == register:

            # Parse info from XML file
            root = xml.etree.ElementTree.parse(filename).getroot()
            username = root.attrib['name']
            local_host_address = root.attrib['host']
            port_number = root.attrib['port']
            connection_speed = root.attrib['speed']

            # Add user info to "registered_users" dictionary
            if username not in self.registered_users.keys():
                self.registered_users[username] = {"hostname": local_host_address, "port": port_number, "speed": connection_speed}
                print("User " + "\"" + username + "\"" + " has joined")
            else:
                print("This username is already registered.")
            os.remove(register)

        # Adds file info to "shareable files dictionary"
        elif filename == file_list:
            # Parse info from file
            root = xml.etree.ElementTree.parse(filename).getroot()
            username = root.attrib['name']

            if username not in self.registered_users.keys():
                print("Please register your account before sharing files!")
            else:
                # Given the user is registered, this will add the filename and the file
                # description to the shareable_files dictionary.

                host_address = self.registered_users[username]['hostname']
                port_number = self.registered_users[username]['port']

                all_files = root.findall('File')
                for f in all_files:
                    filename = f.attrib['name']
                    file_description = f.attrib['description']
                    self.shareable_files[filename] = {'host':  host_address,
                                                      'port': port_number,
                                                      'description':  file_description}

        # Queries the server for a file
        elif filename == query:
            root = xml.etree.ElementTree.parse(filename).getroot()
            search_term = root.attrib['term']

            for f in self.shareable_files:
                for descriptions in f['descriptions']:
                    split_description_list = descriptions.split(' ')
                    if search_term in split_description_list:
                        filename = f
                        host = self.shareable_files[filename]['host']
                        port = self.shareable_files[filename]['port']
                        download_speed = "ethernet"
                        self.sendQueryMatch(file, host, port, download_speed)

        # De-registers the user from the server
        elif filename == quit_file:

            # Delete the user from the list of registered users
            root = xml.etree.ElementTree.parse(filename).getroot()
            username = root.attrib['name']
            del self.registered_users[username]

            # Remove quit file
            os.remove(quit_file)
            print("User " + "\"" + username + "\"" + " has left")


def main():
    """Execution method

    Creates a Threaded server on the localhost with on the port 1515.
    Runs infinitely and accepts all client connections.
    """

    print(os.getcwd())
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

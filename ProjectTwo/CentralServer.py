"""Server

The server class will host all of the client that a user wishes to
manage with the BabyGit version control software.

@author Ron Rounsifer, Bryce Hutton
@version 11.17.2018 (10.26.2018)
"""
import os
import xml.etree.ElementTree
from ftplib import FTP
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.authorizers import DummyAuthorizer


class ServerHandler(FTPHandler):

    # FTP instance to send file to client
    ftp = None
    registered_users = {}
    shareable_files = {}
    keyword_match_instances = None

    def sendMatchesToPeer(self, user):
        root = xml.etree.ElementTree.Element('QueryResponse')

        for match in self.keyword_match_instances:
            download_speed = match[0]
            hostname = match[1]
            port = match[2]
            filename = match[3]
            child = xml.etree.ElementTree.SubElement(root, 'Match', speed=download_speed, hostname=hostname, port=port, filename=filename)
            tree = xml.etree.ElementTree.ElementTree(root)

            # Write the file
            tree.write('matches_found.xml')

            self.ftp = FTP()

            requesting_client_hostname = str(self.registered_users[user]['hostname'])
            requesting_client_port = int(self.registered_users[user]['port'])
            self.ftp.connect(requesting_client_hostname, requesting_client_port)
            self.ftp.login()
            self.ftp.cwd('.')

            query_response = "matches_found.xml"
            self.ftp.storbinary('STOR ' + query_response, open(query_response, 'rb'))

    def on_file_sent(self, file):
        """Close FTP connection

        Closes the FTP connection after the file has been sent successfully

        :param file:
        """
        self.ftp.close()

    def on_file_received(self, file):
        """Populates databases with given information

        Given the xml file passed through, this method parses the information
         it contains and adds it to the corresponding server table in our database.

        Arguments:
            file File -- register / file_list file uploaded to server
        """

        # make sure you are in the correct directory (server)
        if os.path.basename(os.getcwd()) != 'server':
            os.chdir('./server')

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
            local_port_number = root.attrib['port']
            connection_speed = root.attrib['speed']

            # Add to "registered_users" dictionary
            if username not in self.registered_users.keys():
                self.registered_users[username] = {"hostname": local_host_address, 'port': local_port_number,"speed": connection_speed}
                print("User " + "\"" + username + "\"" + " has joined")
            else:
                print("This username is already registered.")

        elif filename == file_list:
            root = xml.etree.ElementTree.parse(filename).getroot()
            all_files = list(root)

            for f in all_files:
                filename = f.attrib['filename']
                description = f.attrib['description']
                user = f.attrib['username']
                source_hostname = self.registered_users[user]['hostname']
                source_port = self.registered_users[user]['port']
                download_speed = self.registered_users[user]['speed']

                self.shareable_files[filename] = {'hostname': source_hostname, 'port': source_port, 'speed': download_speed, 'keywords': description}

        elif filename == query_file:
            root = xml.etree.ElementTree.parse(filename).getroot()
            keyword_to_search_for = root.attrib['keyword']
            querying_user = root.attrib['name']

            # loop through all of the descriptions
            for filename in self.shareable_files.keys():
                keywords = self.shareable_files[filename]['keywords']
                if keyword_to_search_for in keywords:

                    speed = self.shareable_files[filename]['speed']
                    hosting_hostname = self.shareable_files[filename]['hostname']
                    hosting_port = self.shareable_files[filename]['port']

                    self.keyword_match_instances = []
                    self.keyword_match_instances.append([speed, hosting_hostname, hosting_port, filename])
                    print(speed, hosting_hostname, hosting_port, filename)

            if self.keyword_match_instances:
                self.sendMatchesToPeer(querying_user)

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
    authorizer.add_anonymous('./server', perm="elrafmw")

    # Create and define the client handler
    handler = ServerHandler
    handler.authorizer = authorizer
    server = ThreadedFTPServer((""'', 1515), handler)
    server.serve_forever()


if __name__ == "__main__":
    main()

import xml.etree.ElementTree
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.authorizers import DummyAuthorizer

class ServerHandler(FTPHandler):
    registered_users = {}

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
                self.registered_users[username] = {"hostname": local_host_address, "speed": connection_speed}
            else:
                print ("This username is already registered.")
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
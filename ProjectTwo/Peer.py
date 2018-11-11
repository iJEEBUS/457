import GUI
import os
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.authorizers import DummyAuthorizer

class Peer:

    def __init__(self):
        '''Constructor for new Peers

        Opens a data socket that will allow other peers to connect
        and download files.
        '''
        gui = GUI()
        gui.createGUI()
        self.directory_with_files = os.getcwd() + "/."

    def registerWithServer(self):
        ''' Registers the  peer with the server.

        Each peer must register with the server.
        Once registered, a local server will be hosted
        by the peer so other peers can connect and download files.

        Registration includes: hostname, port number, and file
                                                descriptions
        '''

        # Authorize peer connection requests
        authorizer = DummyAuthorizer()
        authorizer.add_user("user", "12345", ".", perm="r")
        authorizer.add_anonymous(self.directory_with_files)

        # Handle peers after connecting
        handler = FTPHandler
        handler.authorizer = authorizer
        local_server = ThreadedFTPServer(("",1515), handler)
        local_server.serve_forever()


    # def downloadFile(command, peer_name, peer_port):
    def downloadFile(self):
        print("Print the file!")



n = Peer()
n.downloadFile()
n.registerWithServer()
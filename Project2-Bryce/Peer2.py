from ftplib import FTP
import xml.etree.cElementTree as ET
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.authorizers import DummyAuthorizer

#PeerHandler class is the thread that handles the p2p connection from the peer server
class PeerHandler(FTPHandler):
    def sendFile(self):
        return


class Peer2(object):
    # FTP instance
    ftp = None

    # Connection status for infinite loop
    __CONNECTION_ALIVE = None

    def __init__(self):
        """Constructor for each peer thread made

        Creates a File Transfer Protocol connection.
        Sets connections status to True.
        """
        # self.ftp = FTP()
        # self.ftp.connect('localhost',1515)
        # self.ftp.login()
        # self.ftp.cwd('.')
        self.__CONNECTION_ALIVE = False
        self.localServer()

    def localServer(self):
        '''Local server for other peers to contact

        Will allow for other peers to download files from
        this peer.
        '''
        # Creates a threaded server similarly to the CentralServer
        authorizer = DummyAuthorizer()
        # lr lets you list files and retrieve them.
        authorizer.add_anonymous('./data', perm='lr')

        handler = PeerHandler
        handler.authorizer = authorizer
        # Server port is 1514 for testing purposes, as client port needs to
        # be different than server port if running on same machine, otherwise
        # it doesn't really matter.

        server = ThreadedFTPServer(('', 1513), handler)
        server.serve_forever()

    def connectToOtherPeer(self, peer_name, port):
        '''Connect to and download from another peer

        Arguments:
            peer_name {[type]} -- [description]
            port {[type]} -- [description]
        '''

        print("Attempting to connect to peer" + peer_name + " at port " + str(port))
        self.ftp = FTP()
        self.ftp.connect(peer_name, port)
        self.ftp.login()

        self.__CONNECTION_ALIVE = True

        return self.__CONNECTION_ALIVE

    def createRegistrationXML(self, username, hostname, speed):
        '''Creates Registration XML file

        Arguments:
            username str -- username of peer
            hostname str -- hostname of peer
            speed int -- connection speed of peer
        '''
        # Create the XML file
        root = ET.Element("User", name=username, host=hostname, speed=speed)
        # ET.SubElement(root, "user").text = username
        # ET.SubElement(root, "host").text = hostname
        # ET.SubElement(root, "speed").text = speed
        tree = ET.ElementTree(root)

        # Write XML file
        tree.write("registration.xml")

    def createFileListXML(self):
        pass

    def readCommand(self, command):
        commands = command.split()
        if commands[0] == "connect":
            if len(commands) < 3:
                self.connectToOtherPeer('', int(commands[1]))
            elif len(commands) == 3:
                self.connectToOtherPeer(commands[1], int(commands[2]))
            else:
                #TODO Change this to be within the UI
                print("Incorrect number of arguments.")
    def connectToCentralServer(self, server_name, port, user, local_host, speed):
        '''Connect to server and return connection status

        Creates a connection to the central server and queries for
        locations (host addresses) of files to download that contain
        a keyword.

        Arguments:
            server_name {str} -- The central servers host address
            port {int} -- The central servers port to connect to

        Returns:
            bool -- The client-server connection status
        '''
        string_server_name = str(server_name)
        int_port = int(port)
        print("Attempting connection to " + server_name + " on port " + port)
        self.ftp = FTP()
        self.ftp.connect(string_server_name, int_port)
        self.ftp.login()
        self.ftp.cwd('.')

        # Create registration XML file
        self.createRegistrationXML(user, local_host, speed)
        print("Registering: " + user + "...")
        registration_file = "registration.xml"
        self.ftp.storbinary('STOR ' + registration_file, open(registration_file, 'rb'))

        self.__CONNECTION_ALIVE = True

        return self.__CONNECTION_ALIVE


if __name__ == "__main__":
    p = Peer2()


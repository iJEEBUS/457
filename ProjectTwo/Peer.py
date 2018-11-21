from ftplib import FTP
import xml.etree.cElementTree as ET
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.authorizers import DummyAuthorizer
import threading
import os

class PeerHandler(FTPHandler):
    """p2p handler

    Handles the p2p connection from the peer to the server
    """
    def sendFile(self):
        return


class Peer(object):
    # FTP instance
    ftp = None
    peerftp = None

    # Connection status for infinite loop
    __CONNECTION_ALIVE = None
    __PCONNECTION_ALIVE = None

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
        self.__PCONNECTION_ALIVE = False
        self.single_thread = None
        self.local_hostname = "127.0.0.1"
        self.port_number = None
        # create a thread to handle the peer-server side.
        self.single_thread = threading.Thread(target=self.localServer).start()

    def localServer(self):
        '''Local server for other peers to contact

        Will allow for other peers to download files from
        this peer.
        '''
        # Creates a threaded server similarly to the CentralServer
        authorizer = DummyAuthorizer()
        # lr lets you list files and retrieve them.
        authorizer.add_anonymous('./files', perm='elr')
        print(os.getcwd())
        os.chdir("./files")
        print(os.getcwd())
        handler = PeerHandler
        handler.authorizer = authorizer
        self.port_number = 1514

        running_local_server = False
        while not running_local_server:
            try:
                server = ThreadedFTPServer(('', self.port_number), handler)
                running_local_server = True
                server.serve_forever()
            except OSError:
                self.port_number += 2


    def connectToOtherPeer(self, peer_name, port):
        """Connect to and download from another peer

        Arguments:
            peer_name {[type]} -- [description]
            port {[type]} -- [description]
        """

        #print("Attempting to connect to peer" + peer_name + " at port " + str(port))
        self.peerftp = FTP()
        self.peerftp.connect(peer_name, port)
        self.peerftp.login()

        self.__PCONNECTION_ALIVE = True

        return "Connected to peer" + peer_name + " at port " + str(port)

    def createRegistrationXML(self, username, hostname, port, speed):
        """Creates Registration XML file

        Arguments:
            username str -- username of peer
            hostname str -- hostname of peer
            speed int -- connection speed of peer
        """
        # Create the XML file
        root = ET.Element("User", name=username, host=hostname, port=port, speed=speed)
        tree = ET.ElementTree(root)

        # Write XML file
        tree.write("registration.xml")

    def createQuitXML(self, username):

        # Create XML file
        root = ET.Element("Quit", name=username)
        tree = ET.ElementTree(root)

        os.chdir("../data")
        # Write the file
        tree.write("quit.xml")

    # Receive file from the server in the form of an iostream.
    def receiveServerList(self):
        pass

    def createFileListXML(self):
        pass

    # read command takes input in from the UI and decides what function should be called from it.
    def readCommand(self, command):
        commands = command.split()
        action_command = commands[0].lower()

        if action_command == "connect":
            if len(commands) < 3:
                return self.connectToOtherPeer('', int(commands[1]))

            elif len(commands) == 3:
                return self.connectToOtherPeer(commands[1], int(commands[2]))

            else:
               return "Error, too many arguments"
        elif action_command in ["retr", "download"]:
            if len(commands) == 2:
                return self.downloadFile(commands[1])

            else:
                return "Error, command does match format: download file.*"
        elif action_command == "quit":
            return self.disconnectFromCentralServer(action_command)
        else:
            return commands[0] + " is not a valid command."

    def downloadFile(self, fileTarget):
        if self.__PCONNECTION_ALIVE == False:
            return False
        cwd = os.getcwd()
        fileDest = open(os.path.join(cwd, fileTarget), 'wb')
        self.peerftp.retrbinary('RETR ' + fileTarget, fileDest.write)
        fileDest.close()
        return "File \"" + fileTarget + "\" is being downloaded."

    def disconnectFromCentralServer(self, command, user):
        """ Disconnect server

        Disconnects from ftp central server by sending an XML file to the server
        to tell it which client is exiting.
        Proceeds to close the connection after the file is sent and acknowledged by the server.
        """
        # Create XML and send XML to server
        self.createQuitXML(user)
        quit_file = "quit.xml"

        self.ftp.storbinary('STOR ' + quit_file, open(quit_file, 'rb'))
        os.remove("quit.xml")
        self.ftp.quit()
       # print(">> " + command)
        return "Disconnected from server."


    def connectToCentralServer(self, server_name, port, user, local_host, speed):
        """Connect to server and return connection status

        Creates a connection to the central server and queries for
        locations (host addresses) of files to download that contain
        a keyword.

        Arguments:
            server_name {str} -- The central servers host address
            port {int} -- The central servers port to connect to

        Returns:
            bool -- The client-server connection status
        """
        string_server_name = str(server_name)
        int_port = int(port)
        print("Attempting connection to " + server_name + " on port " + port)
        self.ftp = FTP()

        self.ftp.connect(string_server_name, int_port)

        self.ftp.login()
        self.ftp.cwd('.')

        # Create registration XML file
        self.createRegistrationXML(user, local_host, int_port, speed)

        print("Registering: " + user + "...")
        registration_file = "registration.xml"
        self.ftp.storbinary('STOR ' + registration_file, open(registration_file, 'rb'))
        print("Connected to " + server_name + " on port " + port)
        self.__CONNECTION_ALIVE = True

        os.remove(registration_file)

        return self.__CONNECTION_ALIVE


if __name__ == "__main__":
    p = Peer()


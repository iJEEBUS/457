"""Client

Clients are created to establish a connection with the server.
Once the connection is established, you may use the BabyGit 
version control system.

@author Ron Rounsifer, Bryce Hutton
@version 10.27.2018 (10.26.2018)
"""
from ftplib import FTP
import os


class Client(object):
    """Client Thread

    This class instantiated when a new Thread is spawned on the server

    Variables:
        ftp {FTP} -- FTP connection with the server
        CONNECTION_ALIVE {Boolean} -- tracks the connection between client and server
    """

    # FTP instance
    ftp = None

    # Connection status for infinite loop
    __CONNECTION_ALIVE = None

    def __init__(self, hostadr, user):
        """Constructor for each client thread

        Creates a File Transfer Protocol connection.
        Sets connections status to True.
        """
        self.ftp = FTP()
        print("Connecting to " + hostadr)
        self.ftp.connect(hostadr, 1515)

        # Passwords for the allowed users
        if user.lower() == 'bryce':
            self.ftp.login(user, "12345")
        else:
            self.ftp.login(user, "54321")

        self.ftp.cwd('.')
        self.__CONNECTION_ALIVE = True;

    def downloadFile(self, file):
        """Retrieve a file from the server

        This should be converted to the PULL command that you would use with Git.

        Arguments:
            file {str} -- the file to download (aka repository to download)
            """
        filename = file
        localFile = open(filename, 'wb')
        self.ftp.retrbinary('RETR ' + filename, localFile.write, 1024)
        self.ftp.quit()
        localFile.close()

    def uploadFile(self, filename):
        """Store a file on the server.

        This will be used to implement the PUSH command that you would use with Git.

        Arguments:
            file {str} -- the file to upload (will not be needed when push command implemented)
        """
        self.ftp.storbinary('STOR ' + filename, open(filename, 'rb'))

    def main(self):
        """Execution method

        Runs an infinite loop
        """

        # Request command from user until they end the connection
        while self.__CONNECTION_ALIVE:

            request = input(str(os.getcwd()) + ": ")

            requestList = request.split(" ")
            command = requestList[0]

            if command == "list":
                files = self.ftp.retrlines('LIST')

            elif command == "retr" and len(requestList) > 1:
                # Formatting: retr filename.txt
                # Download specified file to current local directory
                filename = requestList[1]
                self.downloadFile(filename)

            elif command == "stor" and len(requestList) > 1:
                # Formatting: stor filename.txt
                # Upload specified file to server
                filename = requestList[1]
                self.uploadFile(filename)

            elif command == "quit":
                self.__CONNECTION_ALIVE = False

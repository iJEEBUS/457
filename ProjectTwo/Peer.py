from ftplib import FTP
import xml.etree.cElementTree as ET

import os


import time
import xml.etree.ElementTree
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.authorizers import DummyAuthorizer



class Peer(object):
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
		self.__CONNECTION_ALIVE = False;

	def localServer():
		'''Local server for other peers to contact
		
		Will allow for other peers to download files from 
		this peer.
		'''
		authorizer = DummyAuthorizer()


	def connectToOtherPeer(peer_name, port):
		'''Connect to and download from another peer
		
		Arguments:
			peer_name {[type]} -- [description]
			port {[type]} -- [description]
		'''
		pass

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
		

	def createFileListXML():
		pass


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
		# Create connection to server
		string_server_name = str(server_name)
		int_port = int(port)
		print("Attempting connection to " + server_name + " on port " + port)
		self.ftp = FTP()
		self.ftp.connect(string_server_name,int_port)
		self.ftp.login()
		self.ftp.cwd('.')

		# Create registration XML file
		self.createRegistrationXML(user, local_host, speed)
		print("Registering: " + user + "...")
		registration_file = "registration.xml"

		# Send the registration file to the server
		self.ftp.storbinary('STOR ' + registration_file, open(registration_file, 'rb'))

		# Creates a temp server and waits for the server to send
		#  an acknowledgement that the user has registered successfully.
		timeout= time.time() + 60 # Set the time out to 60 seconds
		while time.time() < timeout:

			authorizer = DummyAuthorizer()
			authorizer.add_anonymous('.', perm="elradfmw")

			handler = PeerHandler
			handler.authorizer = authorizer
			temp_server = ThreadedFTPServer("", 1010)
			temp_server.serve_forever()



		self.__CONNECTION_ALIVE = True

		return self.__CONNECTION_ALIVE


class PeerHandler(FTPHandler):

	def on_file_received(self, file):
		'''
		When the server sends the acknowledgement file back to the peer
		it will either be named "success.txt" or "failure.txt".

		The success file will be empty.
		The failure file will have the error written to the file for further
		investigation.

		:param file :  acknowledgement file sent from the server
		'''

		# Extract just the files name
		filename = os.path.basename(file)
		registration_success = "success.txt"
		registration_failure = "failure.txt"

		# Check the servers response.
		# Delete success file if needed, leave failure file since
		# it contains any errors produced.
		if file == registration_success:
			print ("Your account has been registered by the server.")
			os.remove(file)
		elif file == registration_failure:
			print ("There was an error while registering your account.")
			print ("Check the file 'failure.txt' for any errors produced.")



if __name__ == "__main__":
	p = Peer()

from ftplib import FTP

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



	def connectToCentralServer(self, server_name, port):
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
		self.ftp.connect(string_server_name,int_port)
		self.ftp.login()
		self.ftp.cwd('.')
		self.__CONNECTION_ALIVE = True

		return self.__CONNECTION_ALIVE




if __name__ == "__main__":
	p = Peer()




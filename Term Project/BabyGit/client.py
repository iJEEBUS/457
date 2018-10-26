from ftplib import FTP
import os

class Client(object):

	ftp = None
	__CONNECTION_ALIVE = None

	def __init__(self):
		'''Constructor for each client thread
		
		Creates a File Transfer Protocol connection.
		Sets connections status to True.
		'''
		self.ftp = FTP()
		self.ftp.connect('localhost',1515)
		self.ftp.login()
		self.ftp.cwd('.')
		self.__CONNECTION_ALIVE = True;

	def downloadFile(self, file):
		'''Retrieve a file from the server
		
		This should be converted to the PULL command that you would use with Git.
		
		Arguments:
			file {str} -- the file to download (aka repository to download) 
		'''
		filename = file
		localFile = open(filename, 'wb')
		self.ftp.retrbinary('RETR ' + filename, localFile.write, 1024)
		self.ftp.quit()
		localFile.close()

	def uploadFile(self, file):
		'''Store a file on the server. 

		
		This will be used to implement the PUSH command that you would use with Git.
		
		Arguments:
			file {str} -- the file to upload (will not be needed when push command implemented)
		'''
		filename = file
		self.ftp.storbinary('STOR' + filename, open(filename, 'rb'))
		self.ftp.quit()


	def main(self):
		'''Execution method
		
		Runs an infinite loop 
		'''

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



# Create a client instance
c = Client()

c.main()





















	# def connectToServer(self):
	# 	try:
	# 		# Connect to the local host
	# 		self.ftp.connect('localhost', 1515)
	# 		self.ftp.login()
	# 		self.ftp.cwd('/Desktop/')
	# 		self.__CONNECTION_ALIVE = True
	# 	except:
	# 		print("Could not connect to server.\n Re-attempting connection in 3 seconds.")
	# 		time.sleep(3)

	# self.ftp.connect('localhost', 1515)
	# self.ftp.login()
	# command = input("Command: ")
	# if command == "list":
	# 	self.ftp.retrlines('LIST')
from ftplib import FTP

ftp = FTP('')
ftp.connect('localhost',1515)
ftp.login()
ftp.cwd('/Desktop/')
ftp.retrlines('LIST')

def uploadFile():
	filename = 'testfile.txt'
	ftp.storbinary('STOR' + filename, open(filename, 'rb'))
	ftp.quit()

def downloadFile():
	filename = 'testfile.txt'
	localFile = open(filename, 'wb')
	ftp.retrbinary('RETR ' + filename, localFile.write, 1024)
	ftp.quit()
	localFile.close()

downloadFile()

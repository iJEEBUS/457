def __init__():
	return

def connect(win):
	'''Executes on button 
	
	This method will extract the user inputs from the form and
	connect the user to the remote routing server.
	'''
	server_hostname = win.hostname_entry.get()
	port = port_entry.get()
	user = username_entry.get()
	local_hostname = hostname_entry.get()

def setSpeed(selection):
	'''Set the speed limit
	
	Arguments:
		selection
	'''
	speed = selection

def search():
    '''Query the server for a keyword
    
    This method is called when the "Search" button is pressed.
    It collects the keyword inputted by the user.
    Searches each file description server-side for the keyword.
    Returns a list of locations where the file is available for download.
    '''
    keyword = keyword_entry.get()

def go():
	'''Executes users command
	
	Runs the command that the client sends.
	Since retrievals will occur the command will open up data connection with the 
	client that is hosting the file before downloading said file. 
	Connection stays open until specified by the QUIT command.
	'''
	command = command_entry.get()
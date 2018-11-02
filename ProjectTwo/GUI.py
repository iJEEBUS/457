from tkinter import *
"""GUI

User interface for a peer-to-peer application that will allow 
users to download files from other users that are validated 
by the central server.

@author: Ron Rounsifer, Bryce Hutton
@version: 11.02.2018 (11.01.2018)
"""

def connect():
	'''Executes on button 
	
	This method will extract the user inputs from the form and
	connect the user to the remote routing server.
	'''
	server_hostname = hostname_entry.get()
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

##### Create the main window
window = Tk()
window.title("Napster Host")
window.configure(background="white")

##### Connection
# Connection Label
Label (window, text="Connection", bg="white", fg="black").grid(row=0, column=0, sticky=W)
# Server Hostname
Label (window, text="Server Hostname:", bg="white", fg="black").grid(row=1, column=0, sticky=W)
hostname_entry = Entry(window, width=20, bg="white")
hostname_entry.grid(row=1, column=1, sticky=W)
# Port Number
Label (window, text="Port:", bg="white", fg="black").grid(row=1, column=2, sticky=W)
port_entry = Entry(window, width=7, bg="white")
port_entry.grid(row=1, column=3, sticky=W)
# Connect
Button(window, text="Connect", width=15, command=connect).grid(row=1, column=5, sticky=E)
# Username
Label (window, text="Username:", bg="white", fg="black").grid(row=2, column=0, sticky=W)
username_entry = Entry(window, width=20, bg="white")
username_entry.grid(row=2, column=1, sticky=W)
# Hostname
Label (window, text="Hostname:", bg="white", fg="black").grid(row=2, column=2, sticky=W)
hostname_entry = Entry(window, width=20, bg="white")
hostname_entry.grid(row=2, column=3, sticky=W)
# Speed
Label (window, text="Speed:", bg="white", fg="black").grid(row=2, column=4, sticky=W)
speeds = ["Ethernet", "Option 2", "Option 3"]
default = StringVar(window)
default.set(speeds[0])
speeds_menu = OptionMenu(window, default, *speeds, command=setSpeed)
speeds_menu.grid(row=2, column=5)


## Adding a blank space between connection and search areas
Label(window, text="Blank Space", bg="white", fg="white").grid(row=3, column=0, sticky=W)
##### Search
# Search label
Label (window, text="Search", bg="white", fg="black").grid(row=4, column=0, sticky=W)
# Keyword
Label (window, text="Keyword:", bg="white", fg="black").grid(row=5, column=0, sticky=W)
keyword_entry = Entry(window, width=20, bg="white")
keyword_entry.grid(row=5, column=1, sticky=W)
# Search button
Button(window, text="Search", width=15, command=search).grid(row=5, column=2, sticky=W)

#TODO make this a response table
# Server response table to be implemented
Label (window, text="Table", width=20, bg="white").grid(row=6, column=0, sticky=W)
Label (window, text="Goes", width=20, bg="white").grid(row=7, column=0, sticky=W)
Label (window, text="Here", width=20, bg="white").grid(row=8, column=0, sticky=W)
Label (window, text="Please", width=20, bg="white").grid(row=9, column=0, sticky=W)
Label (window, text="Thank you", width=20, bg="white").grid(row=10, column=0, sticky=W)

##### FTP
## Adding a blank space between connection and search areas
Label(window, text="Blank Space", bg="white", fg="white").grid(row=11, column=0, sticky=W)
Label (window, text="Enter Command: ", bg="white", fg="black").grid(row=12, column=0, sticky=W)
command_entry = Entry(window, width=20, bg="white", fg="black").grid(row=12, column=1, sticky=W)
Button(window, text="Go", width=15, command=go).grid(row=12, column=2, sticky=W)

Label (window, text="Table", width=20, bg="white").grid(row=13, column=0, sticky=W)
Label (window, text="Goes", width=20, bg="white").grid(row=14, column=0, sticky=W)
Label (window, text="Here", width=20, bg="white").grid(row=15, column=0, sticky=W)
Label (window, text="Please", width=20, bg="white").grid(row=16, column=0, sticky=W)
Label (window, text="Thank you", width=20, bg="white").grid(row=17, column=0, sticky=W)

##### Run the window
window.mainloop()

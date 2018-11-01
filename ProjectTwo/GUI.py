from tkinter import *

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

##### Create the main window
window = Tk()
window.title("Napster Host")
window.configure(background="black")

##### Connection
# Connection Label
Label (window, text="Connection", bg="black", fg="white").grid(row=0, column=0, sticky=W)
# Server Hostname
Label (window, text="Server Hostname:", bg="black", fg="white").grid(row=1, column=0, sticky=W)
hostname_entry = Entry(window, width=30, bg="white")
hostname_entry.grid(row=1, column=1, sticky=W)
# Port Number
Label (window, text="Port:", bg="black", fg="white").grid(row=1, column=2, sticky=W)
port_entry = Entry(window, width=15, bg="white")
port_entry.grid(row=1, column=3, sticky=W)
# Connect
Button(window, text="Connect", width=15, command=connect).grid(row=1, column=5, sticky=E)
# Username
Label (window, text="Username:", bg="black", fg="white").grid(row=2, column=0, sticky=W)
username_entry = Entry(window, width=30, bg="white")
username_entry.grid(row=2, column=1, sticky=W)
# Hostname
Label (window, text="Hostname:", bg="black", fg="white").grid(row=2, column=2, sticky=W)
hostname_entry = Entry(window, width=30, bg="white")
hostname_entry.grid(row=2, column=3, sticky=W)
# Speed
Label (window, text="Speed:", bg="black", fg="white").grid(row=2, column=4, sticky=W)
speeds = ["Ethernet", "Option 2", "Option 3"]
default = StringVar(window)
default.set(speeds[0])
speeds_menu = OptionMenu(window, default, *speeds, command=setSpeed)
speeds_menu.grid(row=2, column=5)

##### Search
# Search label
Label (window, text="Search", bg="black", fg="white").grid(row=3, column=0, sticky=W)

# Keyword
Label (window, text="Keyword:", bg="black", fg="white").grid(row=4, column=0, sticky=W)
keyword_entry = Entry(window, width=30, bg="white")
keyword_entry.grid(row=4, column=1, sticky=W)

# Search button
Button(window, text="Search", width=15, command=search).grid(row=4, column=2, sticky=W)

##### FTP

##### Run the window
window.mainloop()

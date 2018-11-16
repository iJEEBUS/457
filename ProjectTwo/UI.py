from tkinter import *
from Peer import *
"""GUI

User interface for a peer-to-peer application that will allow 
users to download files from other users that are validated 
by the central server.

@author: Ron Rounsifer, Bryce Hutton
@version: 11.12.2018 (11.01.2018)
"""
class UI(object):

    peer = Peer()
    connection_speed = "Ethernet"  # Hardcoded for now

    """ Constructor for the UI """
    def __init__(self):
        self.create()

    def connectToServer(self):
        '''Executes on button

		This method will extract the user inputs from the form and
		connect the user to the remote routing server.
		'''
        # Server information
        server_hostname = self.hostname_entry.get()
        port = self.port_entry.get()

        # User information
        user = self.username_entry.get()
        local_hostname = self.local_hostname_entry.get()

        # Connect to server
        self.peer.connectToCentralServer(server_hostname, port, user, local_hostname, self.connection_speed)
        

    def setSpeed(self, selection):
        '''Set the speed limit

		Arguments:
			selection
		'''
        self.connection_speed = selection

    def search(self):
        '''Query the server for a keyword

	    This method is called when the "Search" button is pressed.
	    It collects the keyword inputted by the user.
	    Searches each file description server-side for the keyword.
	    Returns a list of locations where the file is available for download.
		'''
        keyword = keyword_entry.get()

    def go(self):
        '''Executes users command

		Runs the command that the client sends.
		Since retrievals will occur the command will open up data connection with the
		client that is hosting the file before downloading said file.
		Connection stays open until specified by the QUIT command.
		'''
        command = command_entry.get()

    def create(self):
        ##### Create the main window
        window = Tk()
        window.title("Napster Host")
        window.configure(background="white")

        ##### Connection panel
		# Labels
        Label (window, text="Connection", bg="white", fg="black").grid(row=0, column=0, sticky=W)
        Label (window, text="Server Hostname:", bg="white", fg="black").grid(row=1, column=0, sticky=W)
        Label (window, text="Port:", bg="white", fg="black").grid(row=1, column=2, sticky=W)
        Label (window, text="Username:", bg="white", fg="black").grid(row=2, column=0, sticky=W)
        Label (window, text="Hostname:", bg="white", fg="black").grid(row=2, column=2, sticky=W)
        Label (window, text="Speed:", bg="white", fg="black").grid(row=2, column=4, sticky=W)

        # Button
        Button(window, text="Connect", width=15, command=self.connectToServer).grid(row=1, column=5, sticky=E)

        # Text Inputs
        self.hostname_entry = Entry(window, width=20, bg="white")
        self.hostname_entry.grid(row=1, column=1, sticky=W)
        
        self.port_entry = Entry(window, width=7, bg="white")
        self.port_entry.grid(row=1, column=3, sticky=W)
        
        self.username_entry = Entry(window, width=20, bg="white")
        self.username_entry.grid(row=2, column=1, sticky=W)
        
        self.local_hostname_entry = Entry(window, width=20, bg="white")
        self.local_hostname_entry.grid(row=2, column=3, sticky=W)


        # Dropdown menu
        speeds = ["Ethernet", "Option 2", "Option 3"]
        default = StringVar(window)
        default.set(speeds[0])
        self.speeds_menu = OptionMenu(window, default, *speeds, command=self.setSpeed)
        self.speeds_menu.grid(row=2, column=5)


        ## Adding a blank space between connection and search areas
        Label(window, text="Blank Space", bg="white", fg="white").grid(row=3, column=0, sticky=W)


        ##### Search Panel
    	# Labels
        Label (window, text="Search", bg="white", fg="black").grid(row=4, column=0, sticky=W)
        Label (window, text="Keyword:", bg="white", fg="black").grid(row=5, column=0, sticky=W)
    	# Button
        Button(window, text="Search", width=15, command=self.search).grid(row=5, column=2, sticky=W)
        # Text inputs
        self.keyword_entry = Entry(window, width=20, bg="white")
        self.keyword_entry.grid(row=5, column=1, sticky=W)
        #Table
    	#TODO make this a response table
    	# Server response table to be implemented
        Label (window, text="Table", width=20, bg="white").grid(row=6, column=0, sticky=W)
        Label (window, text="Goes", width=20, bg="white").grid(row=7, column=0, sticky=W)
        Label (window, text="Here", width=20, bg="white").grid(row=8, column=0, sticky=W)
        Label (window, text="Please", width=20, bg="white").grid(row=9, column=0, sticky=W)
        Label (window, text="Thank you", width=20, bg="white").grid(row=10, column=0, sticky=W)

        ## Adding a blank space between connection and search areas
        Label(window, text="Blank Space", bg="white", fg="white").grid(row=11, column=0, sticky=W)


        ##### FTP panel
    	# Labels
        Label (window, text="Enter Command: ", bg="white", fg="black").grid(row=12, column=0, sticky=W)
        # Button
        Button(window, text="Go", width=15, command=self.go).grid(row=12, column=2, sticky=W)
        # Text inputs
        self.command_entry = Entry(window, width=20, bg="white", fg="black")
        self.command_entry.grid(row=12, column=1, sticky=W)
        # Table
    	#TODO make this a response table
        Label (window, text="Table", width=20, bg="white").grid(row=13, column=0, sticky=W)
        Label (window, text="Goes", width=20, bg="white").grid(row=14, column=0, sticky=W)
        Label (window, text="Here", width=20, bg="white").grid(row=15, column=0, sticky=W)
        Label (window, text="Please", width=20, bg="white").grid(row=16, column=0, sticky=W)
        Label (window, text="Thank you", width=20, bg="white").grid(row=17, column=0, sticky=W)

        ##### Run the window
        window.mainloop()


UI()
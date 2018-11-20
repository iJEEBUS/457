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

    def __init__(self):
        """ Constructor for the UI """
        self.serverButton = None
        self.hostname_entry = None
        self.port_entry = None
        self.username_entry = None
        self.local_hostname_entry = None
        self.speeds_menu = None
        self.keyword_entry = None
        self.command_entry = None
        self.searchListbox = None
        self.commandListbox = None
        self.create()

    # Puts search results (given as searchList in the form of a list), into the box.
    def searchResults(self, searchList):
        self.searchListbox.delete(0, END)

        for item in searchList:
            self.searchListbox.insert(END, item)

    def disconnectFromServer(self):
        """Executes on button

        This method will disconnect the peer from the server.
        """
        self.peer.disconnectFromCentralServer()
        self.serverButton.configure(text="Connect", command=self.connectToServer)

    def connectToServer(self):
        """Executes on button

        This method will extract the user inputs from the form and
        connect the user to the remote routing server.
        """
        # Server information
        server_hostname = self.hostname_entry.get()
        port = self.port_entry.get()

        # User information
        user = self.username_entry.get()
        local_hostname = self.local_hostname_entry.get()

        # Connect to server
        self.peer.connectToCentralServer(server_hostname, port, user, local_hostname, self.connection_speed)
        self.serverButton.configure(text="Disconnect", command=self.disconnectFromServer)

    def setSpeed(self, selection):
        """Set the speed limit

        Arguments:
            selection
            """
        self.connection_speed = selection

    def search(self):
        '''Query the server for a keyword

        This method is called when the "Search" button is pressed.
        It collects the keyword inputted by the user.
        Searches each file description server-side for the keyword.
        Returns a list of locations where the file is available for download.
        '''
        keyword = self.keyword_entry.get()

        # Put results into listbox using self.searchResults(list)

    def go(self):
        '''Executes users command

        Runs the command that the client sends.
        Since retrievals will occur the command will open up data connection with the
        client that is hosting the file before downloading said file.
        Connection stays open until specified by the QUIT command.
        '''
        command = self.command_entry.get()
        self.peer.readCommand(command)

    def create(self):
        # Create the main window
        window = Tk()
        window.title("Napster Host")
        window.configure(background="white")

        # Connection panel
        # Labels
        Label(window, text="Connection", bg="white", fg="black").grid(row=0, column=0, sticky=W)
        Label(window, text="Server Hostname:", bg="white", fg="black").grid(row=1, column=0, sticky=W)
        Label(window, text="Port:", bg="white", fg="black").grid(row=1, column=2, sticky=W)
        Label(window, text="Username:", bg="white", fg="black").grid(row=2, column=0, sticky=W)
        Label(window, text="Hostname:", bg="white", fg="black").grid(row=2, column=2, sticky=W)
        Label(window, text="Speed:", bg="white", fg="black").grid(row=2, column=4, sticky=W)

        # Button
        self.serverButton = Button(window, text="Connect", width=15, command=self.connectToServer)
        self.serverButton.grid(row=1, column=5, sticky=E)

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

        # Adding a blank space between connection and search areas
        Label(window, text="Blank Space", bg="white", fg="white").grid(row=3, column=0, sticky=W)

        # Search Panel
        # Labels
        Label(window, text="Search", bg="white", fg="black").grid(row=4, column=0, sticky=W)
        Label(window, text="Keyword:", bg="white", fg="black").grid(row=5, column=0, sticky=W)
        # Button
        Button(window, text="Search", width=15, command=self.search).grid(row=5, column=2, sticky=W)
        # Text inputs
        self.keyword_entry = Entry(window, width=20, bg="white")
        self.keyword_entry.grid(row=5, column=1, sticky=W)
        # Table
        # TODO here's listbox tutorial stuff http://effbot.org/tkinterbook/listbox.htm
        self.searchListbox = Listbox(window, height=5)
        self.searchListbox.grid(row=6, column=0, columnspan=6, sticky=NSEW, padx=10, pady=10)

        self.searchListbox.insert(END, 'test')

        # Adding a blank space between connection and search areas
        Label(window, text="Blank Space", bg="white", fg="white").grid(row=11, column=0, sticky=W)

        # FTP panel
        # Labels
        Label(window, text="Enter Command: ", bg="white", fg="black").grid(row=12, column=0, sticky=W)
        # Button
        Button(window, text="Go", width=15, command=self.go).grid(row=12, column=2, sticky=W)
        # Text inputs
        self.command_entry = Entry(window, width=20, bg="white", fg="black")
        self.command_entry.grid(row=12, column=1, sticky=W)
        # Table
        self.commandListbox = Listbox(window, height=5)
        self.commandListbox.grid(row=13, column=0, columnspan=6, sticky=NSEW, padx=10, pady=10)

        self.commandListbox.insert(END, 'test')

        # Run the window
        window.mainloop()


UI()
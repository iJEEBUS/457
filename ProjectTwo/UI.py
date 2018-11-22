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
        self.window = None
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
        self.username = None
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
        command = "quit"
        self.peer.disconnectFromCentralServer(command, self.username)
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
        self.username = user
        local_hostname = self.local_hostname_entry.get()


        # Connect to server
        if self.peer.connectToCentralServer(server_hostname, port, user, local_hostname, self.connection_speed):
            self.commandListbox.insert(END, "Connected to central routing server.")
            self.commandListbox.update()
        # self.serverButton.configure(text="Disconnect", command=self.disconnectFromServer)

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

        # Send the keyword to the server
        self.peer.queryServer(keyword, self.username)

        # TODO Display the returned data

        # Put results into listbox using self.searchResults(list)

        self.commandListbox.insert(END, "Connected to central routing server.")
        self.commandListbox.update()

    def go(self):
        '''Executes users command

        Runs the command that the client sends.
        Since retrievals will occur the command will open up data connection with the
        client that is hosting the file before downloading said file.
        Connection stays open until specified by the QUIT command.
        '''
        full_command = self.command_entry.get()
        lowercase_command_action = full_command.lower().split(' ')[0]
        outputted_command = '>> ' + full_command

        # Display command to GUI
        self.commandListbox.insert(END, outputted_command)
        self.commandListbox.update()

        if self.peer.readCommand(full_command, self.username):

            if lowercase_command_action == 'connect':
                host_address = full_command.split(' ')[1]
                port_number = full_command.split(' ')[2]
                self.commandListbox.insert(END, "Connected to " + host_address + ":" + port_number)

            if lowercase_command_action in ['retr','download']:
                filename = full_command.split(' ')[1]
                self.commandListbox.insert(END, "Successfully downloaded \"" + filename + "\" ")

            if lowercase_command_action == 'quit':

                self.commandListbox.insert(END, "Disconnected from server.")
                self.peer.disconnectFromCentralServer(self.username)

            self.commandListbox.update()


    def closeCompletely(self):
        # THIS WILL BE USED TO CLOSE THE THREADS ON EXIT.
        # When exited, the app hangs and does not respond because the thread is still running.
        #self.peer.single_thread.

        self.destroy()

    def create(self):
        # Create the main window
        window = Tk()
        window.title("Napster Host")
        window.resizable(False, False)
        window.configure(background="white")
        # window.protocol('WM_DELETE_WINDOW', self.closeCompletely)

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
        self.searchListbox = Listbox(window, height=10)
        self.searchListbox.grid(row=6, column=0, columnspan=6, sticky=NSEW, padx=10, pady=10)

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
        # Status text
        self.commandStatus = Label(window, text="", bg="white", fg="black")
        self.commandStatus.grid(row=12, column=3, columnspan=3, sticky=W)
        # Table
        self.commandListbox = Listbox(window, height=10)
        self.commandListbox.grid(row=13, column=0, columnspan=6, sticky=NSEW, padx=10, pady=10)

        # Run the window
        window.mainloop()


UI()
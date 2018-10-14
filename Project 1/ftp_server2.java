import java.io.*;
import java.net.*;
import java.util.*;

class ftp_server2 {

    private static final int BUFSIZE = 32;

    public static void main(String[] args) throws IOException {

	boolean CLIENT_CONNECTED = false;
        int port;
        byte[] inputBuffer;
	byte[] outputBuffer;

        // Create a socket that handles all connections requests
	// (port number is hardcoded)
	port = 1234; 
        ServerSocket welcomeSocket = new ServerSocket(port);

	// Create buffers for reading in and writing out data
	inputBuffer = new byte[BUFSIZE];
	outputBuffer = new byte[BUFSIZE];

	// Have the server up and listening forever
        while(true) {
	    
	   System.out.println("Waiting for client to connect...");	
	
	    // When a connection is attempted, accept it
            Socket client = welcomeSocket.accept();

	    System.out.println("Client from " + client.getInetAddress() + " connected");
	    CLIENT_CONNECTED = true;		

	    // This is where the connected clients get moved to
	    // their own threads
	    ClientHandler handler = new ClientHandler(client);
	    handler.run();
	    
	    
        }
    }
}

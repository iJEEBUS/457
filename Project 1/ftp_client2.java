import java.io.*;
import java.net.*;
import java.util.*;
import java.text.*;
import java.lang.*;
import javax.swing.*;

class ftp_client2 {

   private static int BUFSIZE = 32;

    public static void main(String[] argv) throws Exception {
        String sentence;
        String modifiedSentence;
        boolean connectionOpen = true;
        int num = 1;
        boolean notEnd = true;
        String statusCode;
        boolean clientGo = true;

	while (true) {
	    // Prompt user for a command
	    // Note: you must connect to a specific IP address and port number
	    // 	     before any other commands will work 
            System.out.print("Command: ");
            BufferedReader inFromUser = new BufferedReader(new InputStreamReader(System.in));
            sentence = inFromUser.readLine();
            StringTokenizer tokens = new StringTokenizer(sentence);

	    // Create connection to the specified server IP and port number
        if(sentence.startsWith("connect")) {
	   
	    String localSentence;
	    String userCommand;
		    
	    // Extract server IP and port number
            String serverIP = tokens.nextToken(); // skip connect command
            serverIP = tokens.nextToken();
            int port = Integer.parseInt(tokens.nextToken());

            System.out.println("Connecting to " + serverIP + " on port " + port);
		 
	    // Create the socket and keep the connection alive
            Socket controlSocket = new Socket(serverIP, port);
	    controlSocket.setKeepAlive(true);
	    connectionOpen = true;

            // While this connection exists, run this code
            while (connectionOpen) {
		
		// Create the buffer spaces
		byte[] inputBuffer = new byte[BUFSIZE];
		byte[] outputBuffer = new byte[BUFSIZE];

		// Open the data connection to the server
                DataOutputStream outToServer = new DataOutputStream(controlSocket.getOutputStream());
                DataInputStream inFromServer = new DataInputStream(new BufferedInputStream(controlSocket.getInputStream()));
		
		// Read the users newly inputted message and
		// load its bytes into the buffer
                localSentence = inFromUser.readLine();
		outputBuffer = localSentence.getBytes("ISO-8859-1");

		// Execute commands of the user		
		// Close the connection
		if (localSentence.equalsIgnoreCase("quit")) {
		 
		    // Send the string "quit" to the server
		    outToServer.write(outputBuffer, 0, outputBuffer.length);
		    outToServer.flush();
		    outToServer.close();
		    inFromServer.close();
		    System.out.println("Thank you for visiting.\nThis connection is now closed.");
		    connectionOpen = false;  
		} else if (localSentence.contains("list")) {
		    listFiles(outToServer, outputBuffer, inFromServer, inputBuffer);
		}


            }

        }
    }
}


    /*
    * This sends the list command to the server in order to list all of the files
    * that are in the current directory of the server. 
    *
    * @param out
    * @param outputBuff
    * @param in
    * @param inputBuff
    * @throws IOException 
    */
    private static void listFiles(DataOutputStream out,
				  byte[] outputBuff, 
				  DataInputStream in,
				  byte[] inputBuff) throws IOException {
        // Temporary buffers
	byte[] tempOutputBuffer = outputBuff;
	byte[] tempInputBuffer = inputBuff;

	// Send the list command to the server
	out.write(tempOutputBuffer, 0, tempOutputBuffer.length);
	out.flush();
	
	// Read the response from the server
	// This prints the list of the files in the current directory of the server
	int bytesRead = 0;

	// While there is data to read
	while ((bytesRead = in.read(inputBuff)) >= 0) {

	    // Create and print data to screen
	    String response = new String(tempInputBuffer, "ISO-8859-1");
	    System.out.print(response);
	    
	    // Clear the buffer
	    tempInputBuffer = new byte[BUFSIZE];

	    // Break the loop if the number of bytesRead is 
	    // less than what the buffer supports. This means
	    // the message has reached the end of its transmission.
	    if (bytesRead < tempInputBuffer.length) {
	        break;
	    }
	}

    }


}

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
            //System.out.print("Command: ");
            //BufferedReader inFromUser = new BufferedReader(new InputStreamReader(System.in));
            //sentence = inFromUser.readLine();
            //StringTokenizer tokens = new StringTokenizer(sentence);

	    // Create connection to the specified server IP and port number
//        if(sentence.startsWith("connect")) {
	if (true) {	   
	    String userCommand;
		    
	    // Extract server IP and port number
           // String serverIP = tokens.nextToken(); // skip connect command
           // serverIP = tokens.nextToken();
           // int port = Integer.parseInt(tokens.nextToken());

	    String serverIP = "192.168.1.8";
	    int port = 1234;
            System.out.println("Connecting to " + serverIP + " on port " + port);
		 
	    // Create the socket and keep the connection alive
            Socket controlSocket = new Socket(serverIP, port);
	    controlSocket.setKeepAlive(true);
	    connectionOpen = true;

            // While this connection exists, run this code
            while (connectionOpen){ 
		    System.out.print("Command: ");
		    BufferedReader inFromUser = new BufferedReader(new InputStreamReader(System.in));
            	    sentence = inFromUser.readLine();
            	    StringTokenizer tokens = new StringTokenizer(sentence);
		    tokens.nextToken();

	
		// Create the buffer spaces
		byte[] inputBuffer = new byte[BUFSIZE];
		byte[] outputBuffer = new byte[BUFSIZE];

		// Open the data connection to the server
                DataOutputStream outToServer = new DataOutputStream(controlSocket.getOutputStream());
                DataInputStream inFromServer = new DataInputStream(new BufferedInputStream(controlSocket.getInputStream()));
		
		// Read the users newly inputted message and
		// load its bytes into the buffer
		outputBuffer = sentence.getBytes("ISO-8859-1");

		// Execute commands of the user		
		// Close the connection
		if (sentence.equalsIgnoreCase("quit")) {
		 
		    // Send the string "quit" to the server
		    outToServer.write(outputBuffer, 0, outputBuffer.length);
		    outToServer.flush();
		    outToServer.close();
		    inFromServer.close();
		    System.out.println("Thank you for visiting.\nThis connection is now closed.");
		    connectionOpen = false;  
		} else if (sentence.contains("list")) {
		    listFiles(outToServer, outputBuffer, inFromServer, inputBuffer);
		}else if (sentence.contains("stor")){

			outToServer.write(outputBuffer, 0, outputBuffer.length);
			outToServer.flush();
			ServerSocket fileSocket = new ServerSocket(port+2);
			Socket fileDataSocket = fileSocket.accept();
			writeFile(fileDataSocket, outputBuffer, inputBuffer, tokens.nextToken());
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
	out.write(outputBuff, 0, outputBuff.length);
	out.flush();
	
	// Read the response from the server
	// This prints the list of the files in the current directory of the server
	int bytesRead = 0;
	// While there is data to read
	while ((bytesRead = in.read(inputBuff)) != -1) {
	    
	   	
	    // Create and print data to screen
	    String response = new String(inputBuff, "ISO-8859-1");
	    System.out.print(response);
	    
	    // Clear the buffer
	    inputBuff = new byte[BUFSIZE];

	    // Break the loop if the number of bytesRead is 
	    // less than what the buffer supports. This means
	    // the message has reached the end of its transmission.
	    //if (bytesRead < BUFSIZE) {
	    //    break;
	    //}
	if(bytesRead < inputBuff.length)
		break;
	}
	
    }
	//Method to write a files contents to a fileoutputstream, and to send it to the server
	private static void writeFile(Socket fileSocket, byte[] outputBuff, byte[] inputBuff, String fileName) throws IOException{
		DataOutputStream os = new DataOutputStream(fileSocket.getOutputStream());
    	System.out.println("Writing File" + fileName);
		//Send the stor command to the server

		outputBuff = new byte[BUFSIZE];
		//Turn filename into a file.
		File storFile = new File(fileName);
		//Create new dataInputStream with target provided from client in fileName
		FileInputStream fiStream = new FileInputStream(fileName);

		int bytesRead = 0;
		//Read bytes from the file into the output buff
		while((bytesRead = fiStream.read(outputBuff)) != -1){ 
			//Write to the outstream from the output buff
			//
			os.write(outputBuff, 0, bytesRead);
			os.flush();
			outputBuff = new byte[BUFSIZE];
			if (bytesRead < outputBuff.length)
				break;
		}
		os.close();
		fiStream.close();
		fileSocket.close();


	

	}


}

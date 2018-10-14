import java.io.*;
import java.net.*;
import java.util.*;

class ClientHandler extends Thread {
  private Socket client;
  private DataInputStream inFromClient;
  private DataOutputStream outToClient;
  private byte[] inputBuffer;
  private byte[] outputBuffer;
  private final int BUFSIZE = 32;
  
  public ClientHandler (Socket socket, 
		  DataInputStream in, 
		  DataOutputStream out ) {
    // Set up the referenece socket
    client = socket;
   Thread clientThread = new Thread(); 
      System.out.println("Creating buffers...");
      inputBuffer = new byte[BUFSIZE];
      outputBuffer = new byte[BUFSIZE];
      System.out.println("Creating Data connections.....");  
      inFromClient = in;
      outToClient = out;
      System.out.println("Multithreading success.....");

  }
  
  public void run(){
   
// Close the connection if the client disconnects
   try {
	String message = "";
     do { 
      message = ""; 
       while (inFromClient.read(inputBuffer) != -1) {
         message = new String(inputBuffer, "ISO-8859-1");
         System.out.println(message);
       }
     
       if (message.equals("LIST")) {
  	// Echo the message back to the client
        System.out.println("ECHO: " + message);  
       }
      
       // Repeat until 'QUIT' is sent by client
     } while (!message.toLowerCase().equals("quit"));
  
       if (client != null) {
         System.out.println("Closing down connection...");
	 client.close();
      }
   } catch (IOException io) {
     System.out.println("Unable to disconnect!");
    }
  }
} 

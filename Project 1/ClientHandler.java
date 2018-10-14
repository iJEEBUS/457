import java.io.*;
import java.net.*;
import java.util.*;

class ClientHandler extends Thread{
  private Socket client;
  private Scanner input;
  private PrintWriter output;
  
  public ClientHandler (Socket socket) {
    // Set up the referenece socket
    client = socket;
  
    try {
      System.out.println("Multithreading success.....");
      input = new Scanner(client.getInputStream());
      output = new PrintWriter(client.getOutputStream(), true);
    } catch (IOException io) {
      io.printStackTrace();}
  }
  
  public void run() {
   String received;
   
   do {
     // Accept the message from the client
     received = input.nextLine();

      // Echo the message back to the client
      output.println("ECHO: " + received);

      // Repeat until 'QUIT' is sent by client
   } while (!received.equals("QUIT"));
  
    // Close the connection if the client disconnects
    try {
      if (client != null) {
        System.out.println("Closing down connection...");
	client.close();
      }
    } catch (IOException io) {
      System.out.println("Unable to disconnect!");
    }
  }
 

}

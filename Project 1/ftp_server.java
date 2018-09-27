/**
 * This is the implementation of the server side of a connection
 * that allows for a file transfer protocol to be possible.
 *
 * @author Ron Rounsifer
 * @version 9.26.2018
 */
import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.IOException;
import java.net.*; // for Socket, ServerSocket, and InetAddress
import java.util.Scanner;

public class ftp_server {

	/**
   * Create instance of server and listens for incoming connections
   * from clients
   *
	 * @param args
	 */
	public static void main(String[] args) throws IOException {


        // Create the server socket with the specified port
        int servPort = 1234;
        ServerSocket servSocket = new ServerSocket(servPort);


        // Keep server up and listening for new connections
        while (true) {


            // Accept connection
            System.out.println("Waiting for client to connect...");
            Socket client = servSocket.accept();
            System.out.println("Client from " + client.getInetAddress() + " connected");

            // Print command
            DataInputStream in = new DataInputStream(new BufferedInputStream(client.getInputStream()));
            String command = convertStreamToString(in);
            System.out.println("Command: " + command);
        }
    }


    /**
     * A helper method that converts the bytes from the data input stream into
     * a string that we can use to control the flow of the program based on the
     * users input.
     *
     * @param is - DataInputStream : the byte data received from client
     * @return String - : the decoded version of the byte data
     */
    private static String convertStreamToString(DataInputStream is) {
	    Scanner scan = new Scanner(is).useDelimiter("\\A");
	    return scan.hasNext() ? scan.next() : "";
    }

    



  /**
   * Lists all of the files that are in the current directory of the 
   * server
   */
  private void listFiles() {}
  
  /**
   * Retrieves the specified file and sends it to the client
   */
  private void retrieveFile(String filename) {}
  
  /**
   * Stores a client side file on the server that is specified
   * by the filename.
   * 
   * NOTE: BEWARE OF DUPLICATE FILENAMES
   */
  private void storeFile(String filename) {}
 
  /**
   * Terminates the connection with the client
   */
   private void quit() {}
}

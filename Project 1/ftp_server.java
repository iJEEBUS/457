/**
 * This is the implementation of the server side of a connection
 * that allows for a file transfer protocol to be possible.
 *
 * @author Ron Rounsifer
 * @version 9.26.2018
 */
import java.io.*;
import java.net.*; // for Socket, ServerSocket, and InetAddress
import java.util.Scanner;

public class ftp_server {



    private static final int BUFSIZE = 32;

	/**
   * Create instance of server and listens for incoming connections
   * from clients
   *
	 * @param args
	 */
	public static void main(String[] args) throws IOException {

	    boolean CLIENT_CONNECTED = true;

        // Create the server socket with the specified port
        int servPort = 1234;
        ServerSocket servSocket = new ServerSocket(servPort);

        int messageSize;
        byte[] buffer = new byte[BUFSIZE];
        byte[] output_buffer;


        // Keep server up and listening for new connections
        for (;;) {

            // Accept connection
            System.out.println("Waiting for client to connect...");
            Socket client = servSocket.accept();
            CLIENT_CONNECTED = true;
            System.out.println("Client from " + client.getInetAddress() + " connected");

            while (CLIENT_CONNECTED) {

                // Print command
                DataOutputStream out = new DataOutputStream(new BufferedOutputStream(client.getOutputStream()));
                DataInputStream in = new DataInputStream(new BufferedInputStream(client.getInputStream()));

                while (in.read(buffer) != -1) {

                    String full_command = new String(buffer, "ISO-8859-1").toLowerCase();
//                    String function = new String(full_command.split(" ")[0]);
//                    String filename = (full_command.split(" ").length > 1) ? new String(full_command.split(" ")[1]) : "";

                    if (full_command.contains("quit")) {
                        System.out.println("Closing connection");
                        CLIENT_CONNECTED = false;
                    } else if (full_command.contains("list")) {
                        System.out.println("Command: " + full_command);
                        String cwd = ".";
                        String final_files = "";
                        File dir = new File(cwd);
                        File[] files = dir.listFiles();

                        if (files.length == 0) {
                            System.out.println("This directory is empty");
                        } else {
                            for (File f : files) {
                                final_files += f.getName() + "\n";
                            }

                            output_buffer = final_files.getBytes("ISO-8859-1");
                            out.write(output_buffer, 0, output_buffer.length);
                            out.flush();
                        }



                    } else {
                        System.out.println("Command: " + full_command);
                        buffer = new byte[BUFSIZE];

                    }





                }

            }




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
    private static String convertStreamToString(DataInputStream is) throws IOException {
	    String full_command = "";
	    return full_command;
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

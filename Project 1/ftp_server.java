/**
 * This is the implementation of the server side of a connection
 * that allows for a file transfer protocol to be possible.
 *
 * @author Ron Rounsifer
 * @version 9.26.2018
 */
import java.io.*;
import java.net.*; // for Socket, ServerSocket, and InetAddress

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
        byte[] output_buffer = new byte[BUFSIZE];


        // Keep server up and listening for new connections
        for (;;) {

            // Accept connection
            System.out.println("Waiting for client to connect...");
            Socket client = servSocket.accept();
            CLIENT_CONNECTED = true;
            System.out.println("Client from " + client.getInetAddress() + " connected");


            DataOutputStream out = new DataOutputStream(new BufferedOutputStream(client.getOutputStream()));
            DataInputStream in = new DataInputStream(new BufferedInputStream(client.getInputStream()));

            while (CLIENT_CONNECTED) {

                // Print command

                while (in.read(buffer) != -1) {

                    String full_command = new String(buffer, "ISO-8859-1").toLowerCase();

                    if (full_command.contains("quit")) {
                        CLIENT_CONNECTED = quit();

                    } else if (full_command.contains("list")) {
                        listFiles(out, output_buffer);
                    }
                }

            }
        }
    }

  /**
   * Lists all of the files that are in the current directory of the 
   * server
   */
  private static void listFiles(DataOutputStream os, byte[] out_buffer) throws IOException {
      System.out.println("Listing files.");
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

          out_buffer = new byte[final_files.getBytes("ISO-8859-1").length];
          out_buffer = final_files.getBytes("ISO-8859-1");
          os.write(out_buffer, 0, out_buffer.length);
          os.flush();
      }
  }
  
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
   private static Boolean quit() {
       System.out.println("Closing connection");
       return false;
   }
}

/**
 * This is the implementation of the server side of a connection
 * that allows for a file transfer protocol to be possible.
 *
 * @author Ron Rounsifer
 * @version 9.26.2018
 */
import java.net.*;

public class ftp_server {

	/**
   * Create instance of server and listens for incoming connections
   * from clients
   *
	 * @param args
	 */
	public static void main(String[] args) {}
  
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

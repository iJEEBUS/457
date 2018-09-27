/**
 * This is the implementation of the client side of the file 
 * transfer protocol. It allows the user to establish a connection
 * (the connection data is hardcoded into this program so no input
 * is needed). After establishing a connection the user can then 
 * submit commands in the form of:
 *        LIST - lists all of the files that are in the current 
                  directory of the server
 *        RETR - Retrieves a file by filename from the server
 *        STOR - Sends a file specified by its name to the server
 *        QUIT - Closes control connection with server
 *
 * @author Ron Rounsifer
 * @version 9.26.2018
 */
import java.net.*;

public class ftp_client {

	/**
   * Create instance of client and connect to the server
   *
	 * @param args
	 */
	public static void main(String[] args) {}
  
  /**
   * Lists all of the files that are in the current directory of the 
   * users location in the servers file system
   */
  private void listFiles() {}
  
  /**
   * Retrieves the specified file from the server and outputs
   * the contents to the users console.
   */
  private void retrieveFile(String filename) {}
  
  /**
   * Retrieves the specified file from the client and stores
   * it onto the server with the same filename
   * 
   * NOTE: BEWARE OF DUPLICATE FILENAMES
   */
  private void storeFile(String filename) {}
 
  /**
   * Terminates the connection with the server
   */
   private void quit() {}
}

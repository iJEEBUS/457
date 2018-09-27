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
	* Creates an instance of a client and connects to the server
	* that is hardcoded into the program.
	*
	* @param args
	*/
	public static void main(String[] args) {}
 
  /**
   * Terminates the connection with the server
   */
   private void quit() {}
}

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
import java.io.*;
import java.net.*;
import java.util.Date;
import java.util.Scanner;

public class ftp_client {

	/**
	* Creates an instance of a client and connects to the server
	* that is hardcoded into the program.
	*
	* @param args
	*/
	public static void main(String[] args) throws IOException {

		// connect to server and setup data connection
		Socket server = new Socket("127.0.0.1", 1234);
		System.out.println("Connected to " + server.getInetAddress());
		DataOutputStream out = new DataOutputStream(new BufferedOutputStream(server.getOutputStream()));

		// Prompt user for input
		Scanner scan = new Scanner(System.in);
		System.out.print("Enter a command: ");
		String input = scan.nextLine();
		byte[] buffer = input.getBytes();


		// Send the string to buffer then server
		out.write(buffer, 0, buffer.length);
		out.flush();



	}
 
  /**
   * Terminates the connection with the server
   */
   private void quit(DataOutputStream dos) throws IOException {
   	dos.close();

   }
}

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
import java.util.Scanner;

public class ftp_client {

	private static final int BUFSIZE = 32;



	/**
	* Creates an instance of a client and connects to the server
	* that is hardcoded into the program.
	*
	* @param args
	*/
	public static void main(String[] args) throws IOException {


		int messageSize;


		// connect to server
		Socket server = new Socket("127.0.0.1", 1234);
		server.setKeepAlive(true);

		// Setup data connection
		DataOutputStream out = new DataOutputStream(new BufferedOutputStream(server.getOutputStream()));
		DataInputStream in  = new DataInputStream(new BufferedInputStream(server.getInputStream()));

		System.out.println("Connected to " + server.getInetAddress());

		// input and output buffers
		byte[] input_buffer = new byte[BUFSIZE];
		byte[] output_buffer;

		boolean KEEP_ALIVE = true;

		while (KEEP_ALIVE) {


			// Prompt user for input
			Scanner scan = new Scanner(System.in);
			System.out.print("Enter a command: ");
			String input = scan.nextLine();
			output_buffer = input.getBytes("ISO-8859-1");


			// Close connection if QUIT command is entered
			if (input.equalsIgnoreCase("quit")) {

				// Send the string to output_buffer then server
				out.write(output_buffer, 0, output_buffer.length);
				out.flush();
				scan.close();
				server.close();
				KEEP_ALIVE = false;
				System.out.println("Connection closed.");

			} else if (input.contains("list")) {

				listFiles(out, output_buffer, in, input_buffer);

			} else {

				// unknown commands
				System.out.println("Not a valid command.");
			}

		}
	}

	/**
	 * Displays the files in the current directory that the user is in
	 * on the server.
	 *
	 * @param os
	 * @param out_buffer
	 * @param is
	 * @param in_buffer
	 * @throws IOException
	 */
	private static void listFiles(DataOutputStream os, byte[] out_buffer, DataInputStream is, byte[] in_buffer) throws IOException {

		// send list request to server
		os.write(out_buffer, 0, out_buffer.length);
		os.flush();


		// Read the incoming data stream and print out each filename.
		// Print out response.
		int bytesRead = 0;
		while ((bytesRead = is.read(in_buffer)) >= 0) {
				String response = new String(in_buffer, "ISO-8859-1");
				System.out.print(response);
				in_buffer = new byte[BUFSIZE];

			// Breaks loop when the amt of data read in is less
			// than the buffer can handle
			if (bytesRead < in_buffer.length) {
				break;
			}
		}
	}
}
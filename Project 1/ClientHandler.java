import java.io.*;
import java.net.*;

/**********************************************************************
 * A thread of this class will be created when a new user attempts
 * to connect to the server.
 *
 * @author Ron Rounsifer, Bryce Hutton
 * @version 10.16.2018 :: (9.24.2018)
 *********************************************************************/
class ClientHandler extends Thread {

    /** Control socket to read commands from the client */
    private Socket controlSocket;

    /** Stream to read commands from the client */
    private DataInputStream inFromClient;

    /** Stream to write information back to the client */
    private DataOutputStream outToClient;

    /** Buffer for data input stream */
    private byte[] inputBuffer;

    /** Buffer for data output stream */
    private byte[] outputBuffer;

    /** Buffer size */
    private final int BUFSIZE = 32;

    /**********************************************************************
     * Constructor for the client handler class.
     * Creates a new control socket for the client to use to interact
     * with the server.
     *
     * @param socket - the current client connection
     * @param in
     * @param out
     *********************************************************************/
    public ClientHandler (Socket socket, int port) {
        try {
            controlSocket = socket;
            inputBuffer = new byte[BUFSIZE];
            outputBuffer = new byte[BUFSIZE];
            inFromClient = new DataInputStream(new BufferedInputStream(this.controlSocket.getInputStream()));
            outToClient = new DataOutputStream(new DataOutputStream(this.controlSocket.getOutputStream()));
        } catch (IOException io) {
            io.printStackTrace();
        }
    }
  
  public void run(){
   
// Close the connection if the client disconnects
	try{
 	while(inFromClient.read(inputBuffer) != -1){
		String full_command = new String(inputBuffer, "ISO-8859-1").toLowerCase();
		if (full_command.contains("quit"))
			break;
		else if (full_command.contains("list"))
			listFiles(outToClient, outputBuffer);
		else if (full_command.contains("stor")) {
			ServerSocket fileSocket = new ServerSocket(1237);
			//Socket fileDataSocket = new Socket(controlSocket.getInetAddress(), 1237);
			Socket fileDataSocket = fileSocket.accept();
			writeFile(fileDataSocket, inputBuffer, "test.txt");
			fileDataSocket.close();
			fileSocket.close();
		}

	}
	}
	catch (IOException io){
		System.out.println("error.");
	}
	  
	  

  }
 

private static void listFiles(DataOutputStream os, byte[] out_buffer) throws IOException{
	System.out.println("Listing files.");
	String cwd = ".";
	String final_files = "";
	File dir = new File(cwd);
	File[] files = dir.listFiles();

	if (files.length == 0)
		System.out.println("This directory is empty.");
	else{
		for(File f : files)
			final_files += f.getName() + "\n";
	}

	out_buffer = new byte[final_files.getBytes("ISO-8859-1").length];
	out_buffer = final_files.getBytes("ISO-8859-1");
	os.write(out_buffer, 0, out_buffer.length);
	os.flush();
	}

private static void writeFile(Socket fileSocket, byte[] in_buffer, String fileName) throws IOException{
	DataInputStream in = new DataInputStream(new BufferedInputStream(fileSocket.getInputStream()));
	System.out.println("Writing Files.");

	//Clears the file without actually deleting the file.
	PrintWriter pw = new PrintWriter(fileName);
	pw.write("");
	pw.close();

	FileOutputStream foStream = new FileOutputStream(fileName);

	int bytesRead = 0;
	while ((bytesRead = in.read(in_buffer)) > 0){
		foStream.write(in_buffer, 0, bytesRead);
	}

	foStream.close();
	in.close();

	
}
}

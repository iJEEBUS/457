import java.io.*;
import java.net.*;
import java.util.*;

class ClientHandler extends Thread {
  private Socket client;
  private DataInputStream inFromClient;
  private DataOutputStream outToClient;
  private byte[] inputBuffer;
  private byte[] outputBuffer;
  private final int BUFSIZE = 32;
  
  public ClientHandler (Socket socket, 
		  DataInputStream in, 
		  DataOutputStream out ) {
    // Set up the referenece socket
    client = socket;
   Thread clientThread = new Thread(); 
      System.out.println("Creating buffers...");
      inputBuffer = new byte[BUFSIZE];
      outputBuffer = new byte[BUFSIZE];
      System.out.println("Creating Data connections.....");  
      inFromClient = in;
      outToClient = out;
      System.out.println("Multithreading success.....");

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
		else if (full_command.contains("stor"))
			writeFile(outToClient, inFromClient, outputBuffer, inputBuffer, "test.txt");

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

private static void writeFile(DataOutputStream os,DataInputStream in, byte[] out_buffer, byte[] in_buffer, String fileName) throws IOException{
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

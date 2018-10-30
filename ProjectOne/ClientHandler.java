package ProjectOne;
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
    private static int BUFSIZE = 1024;
    /**********************************************************************
     * Constructor for the client handler class.
     * Creates a 1 control socket, 2 buffers (in/out), and 2 data streams
     * (also in / out).
     *
     * @param socket - the current client connection
     * @param in
     * @param out
     *********************************************************************/
    public ClientHandler(Socket socket, int port) {
        try {
            // Control socket
            controlSocket = socket;
            // Buffers
            inputBuffer = new byte[BUFSIZE];
            outputBuffer = new byte[BUFSIZE];
            // Input streams
            inFromClient = new DataInputStream(
                    new BufferedInputStream(
                            this.controlSocket.getInputStream()));
            outToClient = new DataOutputStream(
                    new DataOutputStream(
                            this.controlSocket.getOutputStream()));
        } catch (IOException io) {
            io.printStackTrace();
        }
    }
    /**********************************************************************
     * Always prompts the user for a command.
     * When a command is entered then the needed portion of
     * code is executed that allows the client and server
     * to interact. Will only leave the while loop when
     * the user enters 'quit'.
     *********************************************************************/
    public void run() {
        // Close the connection if the client disconnects
        while(true){
            try {
                String full_command = inFromClient.readLine();
                // Breakdown full command into components
                String[] splitCommand = full_command.split(" ");
                String command = splitCommand[0];
                if (full_command.contains("quit")){
                    // Close all connections
                    this.controlSocket.close();
                    inFromClient.close();
                    outToClient.close();
                } else if (full_command.toLowerCase().contains("list")) {
                    // Create data socket
                    Socket listDataSocket = new Socket(controlSocket.getInetAddress(), 1236);
                    // Send files to client
                    listFiles(listDataSocket);
                    // Close socket connection
                    listDataSocket.close();
                } else if (full_command.toLowerCase().contains("stor") & splitCommand.length > 1) {
                    // Create data socket
                    Socket fileDataSocket = new Socket(controlSocket.getInetAddress(), 1236);
                    //
                    writeToFile(fileDataSocket, inputBuffer, splitCommand[1]);
                    // Close socket connection
                    fileDataSocket.close();
                } else if (full_command.toLowerCase().contains("retr") & splitCommand.length > 1) {
                    // Create data socket
                    Socket fileDataSocket = new Socket(controlSocket.getInetAddress(), 1236);
                    writeFromFile(fileDataSocket, splitCommand[1]);
                    // Close socket connection
                    fileDataSocket.close();
                }
                // Clear the buffers
                inputBuffer = new byte[BUFSIZE];
                outputBuffer = new byte[BUFSIZE];
            }catch (IOException io) {
                System.out.println();
            }
        }
    }
    /**********************************************************************
     * Collects all of the files in the current directory of the server.
     * Concatenate them into a string and output the string to the client.
     *
     * @param listDataSocket - socket to transmit data
     * @throws IOException
     *********************************************************************/
    private static void listFiles(Socket listDataSocket) throws IOException {
        String cwd = ".";
        String final_files = "";
        File dir = new File(cwd);
        File[] files = dir.listFiles();
        byte[] outputBuffer;
        // Data stream
        DataOutputStream os = new DataOutputStream(
                new DataOutputStream(
                        listDataSocket.getOutputStream()));
        // Print the files unless the directory is empty
        if (files.length == 0)
            System.out.println("This directory is empty.");
        else {
            for (File f : files)
                final_files += f.getName() + "\n";
        }
        // Write the files out to the client
        outputBuffer = new byte[final_files.getBytes("UTF-16").length];
        outputBuffer = final_files.getBytes("UTF-16");
        os.write(outputBuffer, 0, outputBuffer.length);
        os.close();
    }
    /**********************************************************************
     * Writes the contents of a specified file from the current directory
     * of the client to the current working directory of the server.
     *
     * @param fileDataSocket
     * @param in_buffer
     * @param fileName
     * @throws IOException
     *********************************************************************/
    private static void writeToFile(Socket fileDataSocket,
                                    byte[] in_buffer,
                                    String fileName) throws IOException {
        // Input stream
        DataInputStream in = new DataInputStream(
                new BufferedInputStream(
                        fileDataSocket.getInputStream()));
        System.out.println("Downloading  " + fileName + " from " + fileDataSocket.getInetAddress());
        //Clears the file without actually deleting the file.
        PrintWriter pw = new PrintWriter(fileName);
        pw.write("");
        pw.close();
        // Used to write file data
        FileOutputStream foStream = new FileOutputStream(fileName);
        // Write all of the data to a file
        int bytesRead = 0;
        while ((bytesRead = in.read(in_buffer)) > 0) {
            foStream.write(in_buffer, 0, bytesRead);
        }
        // Close streams
        foStream.close();
        in.close();
    }
    /**********************************************************************
     * Writes the contents of a specified file from the servers current
     * working directory to the current directory of the client.
     *
     * @param fileDataSocket - socket to transmit data between client
     *                         and server
     * @param fileName - the file to copy over
     * @throws IOException
     *********************************************************************/
    private static void writeFromFile(Socket fileDataSocket,
                                      String fileName) throws IOException {
        // Data stream
        DataOutputStream os = new DataOutputStream(fileDataSocket.getOutputStream());
        // Outgoing buffer
        byte[] outputBuffer = new byte[BUFSIZE];
        // Create file from filename
        File storFile = new File(fileName);
        if (!storFile.exists()){
            System.out.println("Could not find file");
            os.close();
            return;
        }
        System.out.println("Uploading " + fileName + " to host " + fileDataSocket.getInetAddress());
        // Used to write out file data
        FileInputStream fiStream = new FileInputStream(fileName);
        // Read the file data (as bytes) into the output buffer,
        // send the data to the server, clear output buffer
        int bytesRead = 0;
        while ((bytesRead = fiStream.read(outputBuffer)) != -1) {
            os.write(outputBuffer, 0, bytesRead);
            os.flush();
            outputBuffer = new byte[BUFSIZE];
            if (bytesRead < outputBuffer.length)
                break;
        }
        // Close streams
        os.close();
        fiStream.close();
    }
}
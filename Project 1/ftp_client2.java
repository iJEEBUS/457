import java.io.*;
import java.net.*;
import java.lang.*;
/**********************************************************************
 * The client part of this program. This will allow the user to
 * interact with the server via request they input using the
 * command line. The user can:
 *      1 - connect to a server (using the IP address and port #
 *          as arguments)
 *      2 - list all of the files in the servers current directory
 *      3 - Upload a file to the server
 *      4 - Downlad a file from the server
 *
 * @author Ron Rounsifer, Bryce Hutton
 * @version 10.17.2018 :: (9.24.2018)
 *********************************************************************/
class ftp_client2 {

    private static int BUFSIZE = 1024;

    public static void main(String[] argv) throws Exception {
        String request;
        String[] splitInput;
        boolean connectionOpen = true;

        for (;;) {

            // Greeting message
            System.out.print("\n" +
                    "\n* Command List *\n" +
                    "\n     connect [address] [port #] - connect to a server at the specified host and port number" +
                    "\n     list - lists the files in the servers current directory" +
                    "\n     stor [filename] - upload a file from your current directory to the server" +
                    "\n     retr [filename] - download a file from the server to your current directory" +
                    "\n     quit - close connection with the server" +
                    "\n\nCommand: ");

            // Receive user input and breakdown into components
            BufferedReader inFromUser = new BufferedReader(new InputStreamReader(System.in));
            request = inFromUser.readLine();
            splitInput = request.split(" ");

            // Create connection to the specified server IP and port number
            // Only execute if all needed info is given (IP and port number)
            if (splitInput.length == 3 & splitInput[0].equalsIgnoreCase("connect")) {

                // Extract server IP and port number
                String serverIP = splitInput[1];
                int port = Integer.parseInt(splitInput[2]);

                System.out.println("Connecting to " + serverIP + " on port " + port);

                // Create control socket - keep the connection alive
                Socket controlSocket = new Socket(serverIP, port);
                controlSocket.setKeepAlive(true);
                connectionOpen = true;

                // While this connection exists, run this code
                while (connectionOpen) {
                    System.out.print("Command: ");
                    request = inFromUser.readLine();
                    String[] splitCommand = request.split(" ");
                    String command = splitCommand[0];
                    String file;

                    // Create the buffer spaces
                    byte[] inputBuffer = new byte[BUFSIZE];
                    byte[] outputBuffer = new byte[BUFSIZE];

                    // Open the data connection to the server
                    DataOutputStream outToServer = new DataOutputStream(controlSocket.getOutputStream());
                    DataInputStream inFromServer = new DataInputStream(new BufferedInputStream(controlSocket.getInputStream()));

                    // Read the users request (as bytes) into the output buffer
                    outputBuffer = request.getBytes("UTF-16");

                    // Handles user input
                    if (command.equalsIgnoreCase("quit")) {

                        // Send the quit request to the server
                        outToServer.write(outputBuffer, 0, outputBuffer.length);
                        outToServer.flush();

                        // Close data connections
                        outToServer.close();
                        inFromServer.close();

                        // Set connection status
                        connectionOpen = false;

                        System.out.println("Thank you for visiting.\nThis connection is now closed.");

                    } else if (command.equalsIgnoreCase("list")) {

                        // Send request to the server
                        outToServer.write(outputBuffer, 0, outputBuffer.length);
                        outToServer.flush();

                        // Create socket for sending data
                        ServerSocket listSocket = new ServerSocket(1234 + 2);
                        Socket listDataSocket = listSocket.accept();

                        // Send data
                        listFiles(listDataSocket, inputBuffer);

                        // Close data socket
                        listDataSocket.close();
                        listSocket.close();

                    } else if (command.equalsIgnoreCase("stor") & splitCommand.length > 1) {

                        // Assign filename value
                        file = splitCommand[1];

                        // send request to server
                        outToServer.write(outputBuffer, 0, outputBuffer.length);
                        outToServer.flush();

                        // Create socket for sending data
                        ServerSocket fileSocket = new ServerSocket(1234 + 2);
                        Socket fileDataSocket = fileSocket.accept();

                        // Send data
                        writeFromFile(fileDataSocket, outputBuffer, file);

                        // Close data socket
                        fileDataSocket.close();
                        fileSocket.close();

                    } else if (command.equalsIgnoreCase("retr") & splitCommand.length > 1) {

                        // Assign filename value
                        file = splitCommand[1];

                        // Send request to server
                        outToServer.write(outputBuffer, 0, outputBuffer.length);
                        outToServer.flush();

                        // Create socket for sending data
                        ServerSocket fileSocket = new ServerSocket(1234 + 2);
                        Socket fileDataSocket = fileSocket.accept();

                        // Send data
                        writeToFile(fileDataSocket, inputBuffer, file);

                        // Close data socket
                        fileDataSocket.close();
                        fileSocket.close();
                    }
                }
            }
        }
    }


    /**********************************************************************
     * Sends the list command to the server in order to list all of the
     * files that are in the current directory of the server.
     *
     * @param listDataSocket - socket used to transmit data between
     *                         client and server
     * @param inputBuff - the buffer for incoming data
     * @throws IOException
     *********************************************************************/
    private static void listFiles(Socket listDataSocket,
                                  byte[] inputBuff) throws IOException {

        // Create input stream for data
        DataInputStream in = new DataInputStream(
                                new BufferedInputStream(
                                        listDataSocket.getInputStream()));

        // Read all data into buffer, print when complete, clear buffer
        int bytesRead = 0;
        while ((bytesRead = in.read(inputBuff)) != -1) {

            String response = new String(inputBuff, "UTF-16");
            System.out.print(response);
            inputBuff = new byte[BUFSIZE];

            // Break loop when there are less # of bytes
            // being read in than possible (this means
            // the end of the message has been reached)
            if (bytesRead < inputBuff.length)
                break;
        }
    }


    /**********************************************************************
     * Writes the contents of a specified file from the users current
     * working directory to the current directory of the server.
     *
     * @param fileDataSocket - socket to transmit data between client
     *                         and server
     * @param outputBuff - buffer for outgoing data
     * @param fileName - the file to copy over
     * @throws IOException
     *********************************************************************/
    private static void writeFromFile(Socket fileDataSocket,
                                      byte[] outputBuff,
                                      String fileName) throws IOException {

        // Output stream to write to the server
        DataOutputStream os = new DataOutputStream(fileDataSocket.getOutputStream());

        // Buffer for outgoing data
        byte[] outputBuffer = new byte[BUFSIZE];

        // Create a file from given filename
        File storFile = new File(fileName);
        if (!storFile.exists()){
            System.out.println("Could not find file");
            os.close();
            return;
        }

        System.out.println("Uploading file: " + fileName);

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
        os.close();
        fiStream.close();
    }


    /**********************************************************************
     * Writes the contents of a specified file from the current directory
     * of the server to the users current working directory.
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

        System.out.println("Downloading file: " + fileName);

        // Clear file without actually deleting file
        PrintWriter pw = new PrintWriter(fileName);
        pw.write("");
        pw.close();

        // Used to write file data
        FileOutputStream foStream = new FileOutputStream(fileName);

        // Write the data to a local file
        int bytesRead = 0;
        while ((bytesRead = in.read(in_buffer)) > 0)
            foStream.write(in_buffer, 0, bytesRead);

        // Close streams
        foStream.close();
        in.close();
    }
}

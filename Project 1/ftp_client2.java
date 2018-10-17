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

    private static int BUFSIZE = 32;

    public static void main(String[] argv) throws Exception {
        String sentence;
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
            sentence = inFromUser.readLine();
            splitInput = sentence.split(" ");

            // Create connection to the specified server IP and port number
             if(splitInput.length == 3 & splitInput[0].equalsIgnoreCase("connect")) {

                // Extract server IP and port number
                 String serverIP = splitInput[1];
                 int port = Integer.parseInt(splitInput[2]);

                System.out.println("Connecting to " + serverIP + " on port " + port);

                // Create the socket and keep the connection alive
                Socket controlSocket = new Socket(serverIP, port);
                controlSocket.setKeepAlive(true);
                connectionOpen = true;

                // While this connection exists, run this code
                while (connectionOpen) {
                    System.out.print("Command: ");
                    sentence = inFromUser.readLine();
                    String[] splitCommand = sentence.split(" ");
                    String command = splitCommand[0];
                    String file;

                    // Create the buffer spaces
                    byte[] inputBuffer = new byte[BUFSIZE];
                    byte[] outputBuffer = new byte[BUFSIZE];

                    // Open the data connection to the server
                    DataOutputStream outToServer = new DataOutputStream(controlSocket.getOutputStream());
                    DataInputStream inFromServer = new DataInputStream(new BufferedInputStream(controlSocket.getInputStream()));

                    // Read the users request (as bytes) into the output buffer
                    outputBuffer = sentence.getBytes("ISO-8859-1");

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
                        listFiles(listDataSocket, outputBuffer, inputBuffer);

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
                        writeFromFile(fileDataSocket, outputBuffer, inputBuffer, file);

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


    /*
    * This sends the list command to the server in order to list all of the files
    * that are in the current directory of the server. 
    *
    * @param out
    * @param outputBuff
    * @param in
    * @param inputBuff
    * @throws IOException 
    */
    private static void listFiles(Socket listDataSocket,
                                  byte[] outputBuff,
                                  byte[] inputBuff) throws IOException {
        // Temporary buffers
        byte[] tempOutputBuffer = outputBuff;
        byte[] tempInputBuffer = inputBuff;
        DataInputStream in = new DataInputStream(new BufferedInputStream(listDataSocket.getInputStream()));


        // Read the response from the server
        // This prints the list of the files in the current directory of the server
        int bytesRead = 0;
        // While there is data to read
        while ((bytesRead = in.read(inputBuff)) != -1) {


            // Create and print data to screen
            String response = new String(inputBuff, "ISO-8859-1");
            System.out.print(response);

            // Clear the buffer
            inputBuff = new byte[BUFSIZE];

            // Break the loop if the number of bytesRead is
            // less than what the buffer supports. This means
            // the message has reached the end of its transmission.
            //if (bytesRead < BUFSIZE) {
            //    break;
            //}
            if (bytesRead < inputBuff.length)
                break;
        }

    }

    //Method to write a files contents to a fileoutputstream, and to send it to the server
    private static void writeFromFile(Socket fileDataSocket, byte[] outputBuff, byte[] inputBuff, String fileName) throws IOException {
        DataOutputStream os = new DataOutputStream(fileDataSocket.getOutputStream());

        //Send the stor command to the server

        outputBuff = new byte[BUFSIZE];
        //Turn filename into a file.
        File storFile = new File(fileName);
        if (!storFile.exists()){
            System.out.println("Could not find file");
            os.close();
            return;
        }

        System.out.println("Uploading file: " + fileName);
        //Create new dataInputStream with target provided from client in fileName
        FileInputStream fiStream = new FileInputStream(fileName);

        int bytesRead = 0;
        //Read bytes from the file into the output buff
        while ((bytesRead = fiStream.read(outputBuff)) != -1) {
            //Write to the outstream from the output buff
            //
            os.write(outputBuff, 0, bytesRead);
            os.flush();
            outputBuff = new byte[BUFSIZE];
            if (bytesRead < outputBuff.length)
                break;
        }
        os.close();
        fiStream.close();


    }

    private static void writeToFile(Socket fileDataSocket, byte[] in_buffer, String fileName) throws IOException {
        DataInputStream in = new DataInputStream(new BufferedInputStream(fileDataSocket.getInputStream()));
        System.out.println("Downloading file: " + fileName);

        //Clears the file without actually deleting the file.
        PrintWriter pw = new PrintWriter(fileName);
        pw.write("");
        pw.close();


        FileOutputStream foStream = new FileOutputStream(fileName);

        int bytesRead = 0;
        while ((bytesRead = in.read(in_buffer)) > 0) {
            foStream.write(in_buffer, 0, bytesRead);
        }

        foStream.close();
        in.close();

    }


}

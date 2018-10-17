import java.io.*;
import java.net.*;
/**********************************************************************
 * The server part of this program. Will run in an infinite loop
 * that is always waiting for connection requests. When a connection
 * request is encountered, the server creates a new thread, and moves
 * the clien to the new thread.
 *
 * @author Ron Rounsifer, Bryce Hutton
 * @version 10.17.2018 :: (9.24.2018)
 *********************************************************************/
class ftp_server2 {

    private static int port = 1234;

    public static void main(String[] args) throws IOException {

        // Checks if user entered port and set it
        // if they did
        if (args.length > 0)
            port = Integer.parseInt(args[0]);

        // Create the welcoming socket for all connections
        ServerSocket welcomeSocket = new ServerSocket(port);

        System.out.println("Server now running on port " + port);

        // Have the server up and listening forever
        for (;;) {
            System.out.println("Waiting for client to connect...");

            // Accept all incoming connections
            Socket client = welcomeSocket.accept();

            // Move connections threads, start threads
            ClientHandler handler = new ClientHandler(client, 1235);
            handler.start();

            System.out.println("Client from " + client.getInetAddress() + " connected");
        }
    }
}

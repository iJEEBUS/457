import java.io.*;
import java.net.*;
import java.util.*;

class ftp_server2 {
    private static int port = 1234;

    public static void main(String[] args) throws IOException {

        ServerSocket welcomeSocket = new ServerSocket(port);

        // Have the server up and listening forever
        while(true) {
            System.out.println("Waiting for client to connect...");

            // Accept all incoming connections
            Socket client = welcomeSocket.accept();

            // Move connections to their own threads
            ClientHandler handler = new ClientHandler(client, 1235);
            handler.start();
            System.out.println("Client from " + client.getInetAddress() + " connected");
        }
    }
}

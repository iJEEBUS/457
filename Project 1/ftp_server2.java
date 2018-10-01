import java.io.*;
import java.net.*;
import java.util.*;

class ftp_server2 {

    public static void main(String[] args) throws IOException {

        int port;
        String fromClient;
        String clientCommand;
        byte[] buffer;

        // setup welcome socket for client to handshake
        ServerSocket welcomeSocket = new ServerSocket(12000);

        while(true) {
            Socket controlSocket = welcomeSocket.accept();

            DataOutputStream sendData = new DataOutputStream(controlSocket.getOutputStream());
            BufferedReader clientInput = new BufferedReader(new InputStreamReader(controlSocket.getInputStream()));

            fromClient = clientInput.readLine();

            StringTokenizer tokens = new StringTokenizer(fromClient);

            clientCommand = tokens.nextToken();


        }
    }
}
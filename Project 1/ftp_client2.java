import java.io.*;
import java.net.*;
import java.util.*;
import java.text.*;
import java.lang.*;
import javax.swing.*;

class ftp_client2 {

    public static void main(String argv[]) throws Exception {
        String sentence;
        String modifiedSentence;
        boolean isOpen = true;
        int num = 1;
        boolean notEnd = true;
        String statusCode;
        boolean clientGo = true;

        // Get the command from the users input
        System.out.print("Command: ");
        BufferedReader inFromUser = new BufferedReader(new InputStreamReader(System.in));
        sentence = inFromUser.readLine();
        StringTokenizer tokens = new StringTokenizer(sentence);

        if(sentence.startsWith("connect")) {
            String serverIP = tokens.nextToken(); // skip connect command
            serverIP = tokens.nextToken();
            int port = Integer.parseInt(tokens.nextToken());

            System.out.println("Connecting to " + serverIP + " on port " + port);

            Socket controlSocket = new Socket(serverIP, port);

            // While this connection exists, run this code
            while (isOpen && clientGo) {
                DataOutputStream outToServer = new DataOutputStream(controlSocket.getOutputStream());
                DataInputStream inFromServer = new DataInputStream(new BufferedInputStream(controlSocket.getInputStream()));

                sentence = inFromUser.readLine();


            }

        }

    }
}

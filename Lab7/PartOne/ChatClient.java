import java.net.*;
import java.io.*;
import java.awt.event.*;

public class ChatClient {
		
   public ChatFrame gui;

   private Socket socket;
   private DataInputStream in;
   private DataOutputStream out;
		
   public ChatClient(String name, String server, int port) {

      // GUI Create GUI and handle events:
      // After text input, sendTextToChat() is called,
      // When closing the window, disconnect() is called. 
 
     gui = new ChatFrame("Chat with Sockets");
      gui.input.addKeyListener (new EnterListener(this,gui));
      gui.addWindowListener(new ExitListener(this));
	


      // create a socket, register and listen to the server

      try {
          // create socket and register
          socket = new Socket(server,port);

          // Data connections
          in = new DataInputStream(socket.getInputStream());
          out = new DataOutputStream(socket.getOutputStream());
          out.writeUTF(name);
          while (true) {
              gui.output.append("\n"+in.readUTF());
          }
      }	catch (Exception e)	{
          e.printStackTrace();
      }
   }
   

   protected void sendTextToChat(String str) {
      try {
          // write the message to the chat
          String message = str;
          out.writeUTF(message);
          out.flush();
      } catch (IOException e) {
         e.printStackTrace();
      }
   }

   protected void disconnect() {
      try {

          // close socket
          this.socket.close();
          this.in.close();
          this.out.close();

      } catch (IOException e) {
         e.printStackTrace();
      }
   }
		
   public static void main (String args[])throws IOException {
      if (args.length!=3) 
         throw new RuntimeException ("Syntax: java ChatClient <name> <serverhost> <port>"); 
      int port=Integer.parseInt(args[2]);
      ChatClient c=new ChatClient(args[0], args[1], port);
   }
}


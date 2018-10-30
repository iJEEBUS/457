package Lab7.PartOne;
import java.net.*;
import java.io.*; 
import java.util.*;

public class ChatHandler extends Thread { 
    
   Socket socket; 
   DataInputStream in; 
   DataOutputStream out;
   String name;
   protected static Vector handlers = new Vector ();
    
   public ChatHandler (String name, Socket socket) throws IOException { 
      this.name = name;
      this.socket = socket; 
      this.in = new DataInputStream (this.socket.getInputStream());
      this.out = new DataOutputStream (this.socket.getOutputStream());
   } 
    
   public void run () { 

      try { 
         broadcast(name+" entered");
         handlers.addElement (this);

         // Broadcast the client input to the chat
         while (true) {
             String message = in.readUTF();
             broadcast(message);
         } 

      } catch (IOException ex) { 
         System.out.println("-- Connection to user lost.");
      } finally {
         try {
             handlers.removeElement (this);
             socket.close();
             broadcast(this.name + " disconnected.");
         } catch (IOException ex) { 
            System.out.println("-- Socket to user already closed ?");
         }  
      }
   }
    

   protected static void broadcast (String message) { 
      synchronized (handlers) { 
         Enumeration e = handlers.elements (); 
         while (e.hasMoreElements()) {
            ChatHandler handler = (ChatHandler) e.nextElement();
            try {
                handler.out.writeUTF(message);
                handler.out.flush();
            } catch (IOException ex) { 
               handler.stop (); 
            } 
         }
      }
   } 
}


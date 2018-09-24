import java.net.InetAddress;

public class IPFinder2 {

	/**
	 * Takes the hosts that the use inputs as arguments and returns all of their
	 * associated IP addresses.
	 *
	 * @param args - hostname(s) - the hosts to scan for IP addresses
	 */
	public static void main(String[] args) {
		
		try {

			// Name and IP address of local host parsed into strings
			InetAddress local_host = InetAddress.getLocalHost();
			String local_host_string = local_host.toString();
			String local_ip_string = local_host.getHostAddress();
			String local_name_string = local_host.getHostName();

			// Printing out local host data
			System.out.println("\nLocal Hostname and its IP Address: " + local_host_string);
			System.out.println("Host IP address: \n\t" + local_ip_string);
			System.out.println("Local Host Name: \n\t" + local_name_string);

		} catch (Exception e) {
			System.out.println("Unable to determine this host's address");
		}

		// Iterate hosts passed through the command line arguments
		for (int i = 0; i < args.length; i++) {
			
			try {

				// Array of InetAddress instances for the specified hosts
				InetAddress[] addressList = InetAddress.getAllByName(args[i]);

				// Print inputted target host, target hosts name, and all of
				// the IP addresses that it is associated with.
				System.out.println(args[i] + ":");
				System.out.println("\t" + addressList[i].getHostName());
				for (int j = 0; j < addressList.length; j++) {
					System.out.println("\t" + addressList[j].getHostAddress());
				}

			} catch (Exception e) {
				System.out.println("Unable to find address for " + args[i]);
			}	
		}
		System.out.println("\n");
	}
}

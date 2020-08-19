import java.util.*;
import java.lang.*;
import java.io.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class Mine {

  static double start_time;
  static Map<String, String> block;
  static String address;
  static String host = "solo.ckpool.org";
  static int port = 3333;

  public static void main(String[] args) throws IOException {

    // Prompt user for input (address to bitcoin wallet)
    Scanner address_scanner = new Scanner(System.in);

    System.out.println("Enter your Bitcoin wallet address.\n");

    System.out.println("If you\'re not sure how to get this, first download the Bitcoin.com app from the App Store.");
    System.out.println("Then, create an account. Once you log into the app, select the button labeled, \"RECEIVE\"");
    System.out.println("at the top of the main page. Tap \"BTC\", and copy the address beneath the QR code displayed.\n");

    System.out.println("If you do not want to collect bitcoin for yourself right now, simply leave this field blank");
    System.out.println("(press return), and any coins mined will instead be awarded to my personal address: ");

    address = address_scanner.nextLine();

    if (address.trim().isEmpty()) {
      address = "1CY7gXG8Zz1ExxfxxNf1J5DV78FCoo1pCP";
    }

    // Ask the Python Mining Client to fetch a new block
    String command = "python3 mining_client.py" + " " + "connect_and_fetch_block" + " " + address + " " + host + " " + port;
    System.out.printf("Java is prompting the Python Client with the command-line command: " + Colors.CYAN + "%s%n" + Colors.RESET, command);
    Process p = Runtime.getRuntime().exec(command);
    BufferedReader command_line_in = new BufferedReader(new InputStreamReader(p.getInputStream()));
    
    String ret = "";

    for (int i = 0; i < 4; i++) {
      ret = command_line_in.readLine();
      System.out.println(ret);
    }

    command_line_in.close();
    System.out.println(Colors.YELLOW + "The Python Mining Client has finished downloading a new block.\n" + Colors.RESET);

    try {
      // Read the data of the block fetched by the Python script
      File json_obj = new File("block.json");
      Scanner json_reader = new Scanner(json_obj);
      String block_data = json_reader.nextLine();
      json_reader.close();
      String[] block_data_array = block_data.split("\\s+");

      block = new HashMap<String, String>() {{
        put("version", block_data_array[0]);
        put("previous_block_hash", block_data_array[1]);
        put("merkle_root", block_data_array[2]);
        put("time", block_data_array[3]);
        put("bits", block_data_array[4]);
        put("job_id", block_data_array[5]);
        put("extranonce2", block_data_array[6]);
        put("target", block_data_array[7]);
      }};

      System.out.printf("Mining the block with the following information:%n\033[0;36mVersion: \033[0;31m%s%n\033[0;36mPrevious Block Hash: \033[0;31m%s%n\033[0;36mMerkle Root: \033[0;31m%s%n\033[0;36mTime: \033[0;31m%s%n\033[0;36mBits: \033[0;31m%s%n%n\033[0m", block.get("version"), block.get("previous_block_hash"), block.get("merkle_root"), block.get("time"), block.get("bits"));
      System.out.printf("The target is: " + Colors.CYAN + "%s%n" + Colors.RESET, block.get("target"));
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    }

    int num_threads = 15;
    start_time = System.currentTimeMillis();

    System.out.println(Colors.CYAN + "Mining..." + Colors.RESET);
    
    for (int i = 0; i < num_threads; i ++) {
      Multithreading thread = new Multithreading();
      thread.start();
    }
  }
}
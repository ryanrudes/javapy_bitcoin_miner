import java.util.*;
import java.lang.*;
import java.io.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class Miner {

  static double start_time;
  static Map<String, String> block;
  static String address;
  static String host = "solo.ckpool.org";
  static int port = 3333;

  public static String mine(String[] block_data) throws IOException {

    block = new HashMap<String, String>() {{
      put("version", block_data[0]);
      put("previous_block_hash", block_data[1]);
      put("merkle_root", block_data[2]);
      put("time", block_data[3]);
      put("bits", block_data[4]);
      put("target", block_data[5]);
      put("job_id", block_data[6]);
      put("extranonce2", block_data[7]);
    }};

    System.out.println(Colors.BLUE + ">>> " + Colors.WHITE + "Mining the block with the following information:");
    System.out.println(Colors.BLUE + "  - " + Colors.PURPLE + "Version: " + Colors.CYAN + block.get("version") + Colors.RESET);
    System.out.println(Colors.BLUE + "  - " + Colors.PURPLE + "Previous Block Hash: " + Colors.CYAN + block.get("previous_block_hash") + Colors.RESET);
    System.out.println(Colors.BLUE + "  - " + Colors.PURPLE + "Merkle Root: " + Colors.CYAN + block.get("merkle_root") + Colors.RESET);
    System.out.println(Colors.BLUE + "  - " + Colors.PURPLE + "Time: " + Colors.CYAN + block.get("time") + Colors.RESET);
    System.out.println(Colors.BLUE + "  - " + Colors.PURPLE + "Bits: " + Colors.CYAN + block.get("bits") + Colors.RESET);

    System.out.printf(Colors.BLUE + ">>> " + Colors.WHITE + "Target: " + Colors.CYAN + "%s%n" + Colors.RESET, block.get("target"));

    int num_threads = 15;
    start_time = System.currentTimeMillis();

    System.out.println(Colors.BLUE + ">>> " + Colors.WHITE + "Mining..." + Colors.RESET);
    
    for (int i = 0; i < num_threads; i ++) {
      Multithreading thread = new Multithreading();
      thread.start();
    }

    return "PLACEHOLDER";
  }
}
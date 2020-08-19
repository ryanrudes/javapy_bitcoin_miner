import java.util.*;
import java.lang.*;
import java.io.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

class Multithreading extends Thread {

  static int best_score = 0;
  static String best_hash;
  static int hashes_since_last_report, integer_nonce;
  final String header_without_nonce = Miner.block.get("version") + Miner.block.get("previous_block_hash") + Miner.block.get("merkle_root") + Miner.block.get("time") + Miner.block.get("bits");
  String nonce, header_hex, hash_hex;
  byte[] header_bin, hash_bin;
  int num_leading_zeros, num_trailing_zeros;
  MessageDigest digester;

  static final long max_nonce = 4294967295L;
  static final int max_search_time = 600;
  static final int report_frequency = 1000;
  double duration, hashrate, completion;
  String time_remaining, time_until_termination;

  final int target_trailing_zeros = get_num_trailing_zeros(Miner.block.get("target"));
  // final int target_leading_zeros = get_num_leading_zeros(Miner.block.get("target"));

  final protected static char[] hex_array = "0123456789abcdef".toCharArray();

  static byte[] hex_string_2_byte_array(String s) {

    int len = s.length();
    byte[] data = new byte[len / 2];

    for (int i = 0; i < len; i += 2) {
      data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4) + Character.digit(s.charAt(i + 1), 16));
    }

    return data;
  }

  static int get_num_leading_zeros(String s) {
    int i = 0;

    while (true) {
      if (s.charAt(i) != '0') {
        return i;
      }

      i += 1;
    }
  }

  static int get_num_trailing_zeros(String s) {
    StringBuilder input1 = new StringBuilder();
    input1.append(s);
    input1.reverse();
    int i = 0;

    while (true) {
      if (input1.charAt(i) != '0') {
        return i;
      }

      i += 1;
    }
  }

  static String seconds_to_hms(int seconds) {
    int hours = Math.floorDiv(seconds, 3600);
    seconds %= 3600;
    int minutes = Math.floorDiv(seconds, 60);
    return String.format("%02d", hours) + ":" + String.format("%02d", minutes) + ":" + String.format("%02d", seconds % 60);
  }

  static String bytes2hex(byte[] bytes) {

    char[] hex_chars = new char[bytes.length * 2];
    int v;

    for (int i = 0; i < bytes.length; i++) {
      v = bytes[i] & 0xFF;
      hex_chars[i * 2] = hex_array[v >> 4];
      hex_chars[i * 2 + 1] = hex_array[v & 0x0F];
    }

    return new String(hex_chars);
  }

  public void run() {
    MessageDigest digester = null;

    try {
      digester = MessageDigest.getInstance("SHA-256");
    } catch (java.security.NoSuchAlgorithmException e) {
      e.printStackTrace();
    }

    while (true) {

      nonce = Integer.toHexString(integer_nonce);
      nonce = "00000000".substring(nonce.length()) + nonce;
      header_hex = header_without_nonce + nonce;
      hash_hex = bytes2hex(digester.digest(digester.digest(hex_string_2_byte_array(header_hex))));
      hash_hex = new StringBuilder(hash_hex).reverse().toString();

      // num_leading_zeros = get_num_leading_zeros(hash_hex);
      num_trailing_zeros = get_num_trailing_zeros(hash_hex);
      
      if (num_trailing_zeros >= best_score) {
        best_score = num_trailing_zeros;
        best_hash = hash_hex;
      }

      if (num_trailing_zeros >= target_trailing_zeros) {
        try {
          // Ask the Python Mining Client to submit a hash
          String command = "python3 mining_client.py" + " " + "submit_results" + " " + Miner.address + " " + Miner.host + " " + Miner.port + " " + Miner.block.get("job_id") + " " + Miner.block.get("extranonce2") + " " + Miner.block.get("time") + " " + nonce;
          System.out.printf("Java is prompting the Python Client with the command-line command: " + Colors.CYAN + "%s%n" + Colors.RESET, command);
          Process p = Runtime.getRuntime().exec(command);
          BufferedReader command_line_in = new BufferedReader(new InputStreamReader(p.getInputStream()));
          String ret = command_line_in.readLine();
          System.out.println(ret);
          command_line_in.close();
        } catch (IOException i) {
          i.printStackTrace();
        }
      }

      hashes_since_last_report ++;

      if (hashes_since_last_report % report_frequency == 0) {
        hashes_since_last_report = 0;
        duration = (System.currentTimeMillis() - Miner.start_time) / 1000.0;
        hashrate = integer_nonce / duration;
        completion = (double) integer_nonce / (double) max_nonce * 100.0;
        time_remaining = seconds_to_hms((int)(max_nonce / hashrate));
        time_until_termination = seconds_to_hms(max_search_time - (int) duration);

        System.out.printf("Nonce: %s, Hash: %s, Score: %s, Best Score: %s, Best Hash: %s, Hashes Tried: %s, Hashrate: %s HPS, Duration: %s seconds, Completion: %s%%, Time Remaining: %s seconds, Time Until Expected Mining Of The Block: %s\r", nonce, hash_hex, num_leading_zeros, best_score, best_hash, integer_nonce + 1, hashrate, duration, completion, time_remaining, time_until_termination);
      }

      if (integer_nonce >= max_nonce) {
        System.out.println();
        System.exit(0);
      } else {
        integer_nonce ++;
      }
    }
  }
}
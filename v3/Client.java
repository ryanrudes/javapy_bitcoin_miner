import java.io.*;
import java.net.*;
import java.util.*;
import java.nio.charset.StandardCharsets;

class Client {

  static Socket socket = null;
  static DataInputStream din;
  static DataOutputStream dout;
  static byte[] buffer = new byte[157*10];

  public static void sendUTF(String message) throws IOException {
    dout.writeUTF(message);
    dout.flush();
  }

  public static void sendByte(int b) throws IOException {
    dout.writeByte(b);
    dout.flush();
  }

  public static String receive() throws IOException {
    din.read(buffer);
    String received_message = new String(buffer, StandardCharsets.UTF_8);
    return received_message;
  }

  public static void close() throws IOException {
    sendUTF("Disconnecting");
    din.close();
    dout.close();
    socket.close();
  }

  public Client(String host, int port) throws IOException {
    try {
      socket = new Socket(host, port);
    } catch (ConnectException e) {
      System.out.println(Colors.BLUE + ">>> " + Colors.RED_BOLD + "CONNECTION REFUSED" + Colors.RED + ": either the server is not running or your request to connect has been denied." + Colors.RESET);
      System.exit(0);
    }

    din = new DataInputStream(socket.getInputStream());
    dout = new DataOutputStream(socket.getOutputStream());
  }

  public static void main(String[] args) throws UnknownHostException, IOException, ClassNotFoundException {

    String host = "0.0.0.0";
    int port = 8080;

    String[] block_data;
    String received_message;

    Client client = new Client(host, port);
    received_message = client.receive();
    System.out.println(Colors.BLUE + "--> " + Colors.WHITE + "Received a message from the Python server: " + Colors.CYAN + received_message + Colors.RESET);

    client.sendUTF("Connect to web socket");
    System.out.println(Colors.BLUE + "<-- " + Colors.WHITE + "Sent a request to the Python server to connect to the web socket." + Colors.RESET);

    client.sendUTF("Fetch block");
    System.out.println(Colors.BLUE + "<-- " + Colors.WHITE + "Sent a request to the Python server for a new block." + Colors.RESET);

    received_message = client.receive();
    System.out.println(Colors.BLUE + "--> " + Colors.WHITE + "Received a message from the Python server: " + Colors.CYAN + received_message + Colors.RESET);
    block_data = received_message.split("\\s+");

    Miner miner = new Miner();
    miner.mine(block_data);

    client.close();
  }

}
import socket
from termcolor import colored
import mining_api

try:
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind(('0.0.0.0', 8080))
  server.listen(5)

  print (colored(">>> ", "blue") + colored("Successfully started the Python server.", "green"))
except:
  print (colored(">>> ", "blue") + colored("Failed to start the Python server.", "red"))

done = False

while True:
  connection, address = server.accept()
  print (colored(">>> ", "blue") + colored("The Java client has successfully connected to the Python server.", "green"))
  connection.send("You have successfully connected to the Python server.".encode('utf-8'))
  print (colored("<-- ", "blue", attrs = ["bold"]) + colored("Notified the Java client of a successful connection.", "white"))
  
  try:
    while True:
      message = connection.recv(1024).decode()
      message = ''.join([character for character in message if 32 <= ord(character) and 126 >= ord(character)])

      if not message:
        break
      else:
        print (colored("--> ", "blue", attrs = ["bold"]) + colored("Received a message from the Java client: ", "white") + colored(message, "cyan"))

        if message == "Fetch block":
          version, prevhash, merkle_root, ntime, nbits, target, job_id, extranonce2 = mining_api.fetch_block(sock, address)
          # merkle_root = mining_api.compute_merkle_root(merkle_branch)
          header = version + " " + prevhash + " " + merkle_root + " " + ntime + " " + nbits + " " + target + " " + job_id + " " + extranonce2
          connection.send(header.encode('utf-8'))
          print (colored("<-- ", "blue", attrs = ["bold"]) + colored("Sent the Java client the header of the fetched block: ", "white") + colored(header, "cyan"))
        elif message == "Connect to web socket":
          host = "solo.ckpool.org"
          port = 3333
          address = "1CY7gXG8Zz1ExxfxxNf1J5DV78FCoo1pCP"

          try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            print (colored(">>> ", "blue") + colored("Successfully established a connection to the host via the wallet address: ", "green") + colored(address, "green", attrs = ["bold"]) + colored(".", "green"))
          except Exception as e:
            print (colored("Failed to connect to the host. The following unexpecteded error has occurred:\n{}".format(e), "red"))
        elif message == "Disconnecting":
          print (colored("--> ", "blue") + colored("The Java client is disconnecting from the server.", "yellow"))
  except KeyboardInterrupt:
    done = True
    print (colored("\nClosing the Python Server...", "yellow"))
    server.close()
    print (colored("The Python server has been closed.", "yellow"))
    print (colored("The Java client has disconnected.", "yellow"))
    break
  except Exception as e:
    if str(e) == "[Errno 54] Connection reset by peer":
      print (colored("The Java client has disconnected.", "yellow"))
      print (colored("It appears the Java client disconnected improperly. Ensure that future socket connections, include their data input/output streams are properly closed via .close()"))
    else:
      print (colored("An unexpected error has occurred: " + str(e), "red"))
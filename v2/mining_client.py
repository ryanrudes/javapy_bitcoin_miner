import socket
import json
from termcolor import colored
import hashlib
import binascii
import sys

def connect(address, host, port):
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print (colored("Successfully established a connection to the host via the wallet address: ", "yellow") + colored(address, "green", attrs = ["underline"]) + colored(".", "yellow"))
    return sock
  except Exception as e:
    if e == socket.gaierror:
      print (colored("Check that there were no typos in the hostname and/or port entered. If there are none, there may be something wrong with you internet. Check your current connection.", "red"))
    else:
      print (colored("Failed to connect to the host due to the following unexpected error: {}".format(e), "red"))

    exit()

def fetch_block(sock, address):
  try:
    sock.sendall(b'{"id": 1, "method": "mining.subscribe", "params": []}\n')
    lines = sock.recv(1024).decode().split("\n")
    response = json.loads(lines[0])
    sub_details, extranoncel, extranonce2_size = response["result"]
    sock.sendall(b'{"params": ["' + address.encode() + b'", "password"], "id": 2, "method": "mining.authorize"}\n')

    response = b''

    while response.count(b'\n') < 4 and not(b'mining.notify' in response):
      response += sock.recv(1024)

    responses = [json.loads(res) for res in response.decode().split('\n') if len(res.strip()) > 0 and 'mining.notify' in res]
  
    job_id, prevhash, coinb1, coinb2, merkle_branch, version, nbits, ntime, clean_jobs = responses[0]["params"]
    target = (nbits[2:] + "00" * (int(nbits[:2], 16) - 3)).zfill(64)
    extranonce2 = "00" * extranonce2_size

    coinbase = coinb1 + extranoncel + extranonce2 + coinb2
    coinbase_hash_bin = hashlib.sha256(hashlib.sha256(binascii.unhexlify(coinbase)).digest()).digest()

    merkle_root = coinbase_hash_bin
    for h in merkle_branch:
      merkle_root = hashlib.sha256(hashlib.sha256(merkle_root + binascii.unhexlify(h)).digest()).digest()

    merkle_root = binascii.hexlify(merkle_root).decode()

    merkle_root = "".join([merkle_root[i] + merkle_root[i + 1] for i in range(0, len(merkle_root), 2)][::-1])

    print (colored("Successfully found a transaction in need of verification.", "yellow"))
    block = '{} {} {} {} {} {} {} {}'.format(version, prevhash, merkle_root, ntime, nbits, job_id, extranonce2, target)
    return block
  except Exception as e:
    print (colored("An unexpected failure occurred. Failed to find a transaction in need of verification. The process terminated due to the following unexpected error:\n{}".format(e), "red"))
    exit()

def connect_and_fetch_block(address, host, port):
  print(colored("Attempting to connect to the host ", "yellow") + colored(host, "green", attrs = ["underline"]) + colored(" via port ", "yellow") + colored(port, "green", attrs = ["underline"]) + colored(" with address ", "yellow") + colored(address, "green", attrs = ["underline"]) + colored("...", "yellow"))

  # Format the command-line arguments to their proper types
  port = int(port)

  # Connect to the host
  sock = connect(address, host, port)

  # Fetch the most recent block
  block = fetch_block(sock, address)

  return block

def submit_results(address, host, port, job_id, extranonce2, time, nonce):
  # Format the command-line arguments to their proper types
  port = int(port)
  print (address, host, port)
  sock = connect(address, host, port)
  payload = '{"params": ["' + address + '", "' + job_id + '", "' + extranonce2 + '", "' + time + '", "' + nonce + '"], "id": 1, "method": "mining.submit"}\n'
  payload = bytearray(payload, 'utf-8')
  payload = bytearray(b'{"params": ["1CY7gXG8Zz1ExxfxxNf1J5DV78FCoo1pCP", "5eebeafb00018459", "0000000000000000", "5f3b0bef", "0000000f"], "id": 1, "method": "mining.submit"}\n')
  sock.send(payload)
  print (colored("Submitting a discovered hash with a significant number of trailing zeros!: {}".format(sock.recv(1024).decode()), "green"), end = "\r")

# Get command-line arguments
command = sys.argv[1]
print (colored("The Python Mining Client has received the following command: ", "yellow") + colored(command, "cyan"))

# Run approperiate command
if command == "connect_and_fetch_block":
  address, host, port = sys.argv[2:5]
  block = connect_and_fetch_block(address, host, port)
  with open("block.json", "w") as f:
    f.write(block)

  f.close()
elif command == "submit_results":
  address, host, port, job_id, extranonce2, time, nonce = sys.argv[2:9]
  submit_results(address, host, port, job_id, extranonce2, time, nonce)
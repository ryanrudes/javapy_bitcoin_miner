import socket
import json
from termcolor import colored
import hashlib
import binascii

def connect():
  print (colored("\nPrompting user for input...", "yellow"))
  address = input(
"""
Enter your Bitcoin wallet address. 

If you're not sure how to get this, first download the Bitcoin.com app from the App Store.
Then, create an account. Once you log into the app, select the button labeled, "RECEIVE"
at the top of the main page. Tap "BTC", and copy the address beneath the QR code displayed.

If you do not want to collect bitcoin for yourself right now, simply leave this field blank
(press return), and any coins mined will instead be awarded to my personal address: """)

  if address == "":
    address = "1CY7gXG8Zz1ExxfxxNf1J5DV78FCoo1pCP"

  host = "solo.ckpool.org"
  port = 3333

  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print (colored("Successfully established a connection to the host via the wallet address: {}.".format(address), "yellow"))
    return sock, address
  except Exception as e:
    print (colored("Failed to connect to the host. The following unexpecteded error has occurred:\n{}".format(e), "red"))
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

    block = {
      'version': version,
      'previous_block_hash': prevhash,
      'merkle_root': merkle_root,
      'time': ntime,
      'bits': nbits
    }

    return block, target, job_id, extranonce2
  except Exception as e:
    print (colored("An unexpected failure occurred. Failed to find a transaction in need of verification. The process terminated due to the following unexpected error:\n{}".format(e), "red"))
    exit()
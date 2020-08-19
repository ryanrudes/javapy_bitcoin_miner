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
    print (colored(">>> ", "blue") + colored("Successfully established a connection to the host via the wallet address: ", "yellow") + colored(address, "green", attrs = ["bold"]))
    return sock, address
  except Exception as e:
    print (colored("Failed to connect to the host. The following unexpecteded error has occurred:\n{}".format(e), "red"))
    exit()

def hash2(a, b):
  a1 = bytes.fromhex(a)[::-1]
  b1 = bytes.fromhex(b)[::-1]
  h = hashlib.sha256(hashlib.sha256(a1 + b1).digest()).digest()
  return binascii.hexlify(h[::-1]).decode()

def compute_merkle_root(hashList):
  if len(hashList) == 1:
    return hashList[0]

  newHashList = []

  for i in range(0, len(hashList) - 1, 2):
    newHashList.append(hash2(hashList[i], hashList[i+1]))

  if len(hashList) % 2 == 1:
    newHashList.append(hash2(hashList[-1], hashList[-1]))

  return compute_merkle_root(newHashList)

def fix(string):
  return ''.join([string[i:i + 8][::-1] for i in range(0, len(string), 8)])

def fetch_block(sock, address):
  try:
    """
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

    prevhash = fix(prevhash[::-1])
    print (merkle_branch)
    # merkle_branch = [hashlib.sha256(hash.encode()).hexdigest() for hash in merkle_branch]
    merkle_root = compute_merkle_root(merkle_branch)
    
    target = (nbits[2:] + "00" * (int(nbits[:2], 16) - 3)).zfill(64)
    extranonce2 = "00" * extranonce2_size

    
    coinbase = coinb1 + extranoncel + extranonce2 + coinb2
    coinbase_hash_bin = hashlib.sha256(hashlib.sha256(binascii.unhexlify(coinbase)).digest()).digest()

    merkle_root = coinbase_hash_bin
    for h in merkle_branch:
      merkle_root = hashlib.sha256(hashlib.sha256(merkle_root + binascii.unhexlify(h)).digest()).digest()

    merkle_root = binascii.hexlify(merkle_root).decode()

    merkle_root = "".join([merkle_root[i] + merkle_root[i + 1] for i in range(0, len(merkle_root), 2)][::-1])
    
    """


    #server connection
    sock.sendall(b'{"id": 1, "method": "mining.subscribe", "params": []}\n')
    lines = sock.recv(1024).decode().split('\n')
    response = json.loads(lines[0])
    sub_details,extranonce1,extranonce2_size = response['result']

    #authorize workers
    sock.sendall(b'{"params": ["'+address.encode()+b'", "password"], "id": 2, "method": "mining.authorize"}\n')

    #we read until 'mining.notify' is reached
    response = b''
    while response.count(b'\n') < 4 and not(b'mining.notify' in response):
        response += sock.recv(1024)


    #get rid of empty lines
    responses = [json.loads(res) for res in response.decode().split('\n') if len(res.strip())>0 and 'mining.notify' in res]

    job_id,prevhash,coinb1,coinb2,merkle_branch,version,nbits,ntime,clean_jobs \
        = responses[0]['params']

    #target https://bitcoin.stackexchange.com/a/36228/44319
    target = (nbits[2:]+'00'*(int(nbits[:2],16) - 3)).zfill(64)

    extranonce2 = '00'*extranonce2_size

    coinbase = coinb1 + extranonce1 + extranonce2 + coinb2
    coinbase_hash_bin = hashlib.sha256(hashlib.sha256(binascii.unhexlify(coinbase)).digest()).digest()

    merkle_root = coinbase_hash_bin
    for h in merkle_branch:
        merkle_root = hashlib.sha256(hashlib.sha256(merkle_root + binascii.unhexlify(h)).digest()).digest()

    merkle_root = binascii.hexlify(merkle_root).decode()

    #little endian
    merkle_root = ''.join([merkle_root[i]+merkle_root[i+1] for i in range(0,len(merkle_root),2)][::-1])

    print (colored(">>> ", "blue") + colored("Successfully found a transaction in need of verification.", "green"))

    return version, prevhash, merkle_root, ntime, nbits, target, job_id, extranonce2
  except Exception as e:
    print (colored("An unexpected failure occurred. Failed to find a transaction in need of verification. The process terminated due to the following unexpected error:\n{}".format(e), "red"))
    exit()

"""
2339d5ef 23945d14 8533628c 7fb73a9a a1d850fb 0010241a 00000000 00000000
00000000 00000000 a1420100 bf058d1a a9a37bf7 c8263358 41d54932 fe5d9332
00000000 00000000 0010241a a1d850fb 7fb73a9a 8533628c 23945d14 2339d5ef

2f6bca1608f5a47c3c5f8e30a9dd00108df885fd52d2a705ad0dda1149a072e1
1e270a9411add0da507a2d25df588fd80100dd9a03e8f5c3c74a5f8061acb6f2
edceb8a7411c230833f2c93c54e7d84d47e9c912ec8b560cefb5a203bf5344b5
"""
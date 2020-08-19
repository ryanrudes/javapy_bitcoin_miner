# Real-time Bitcoin Miner

import sys
import json
import hashlib
import binascii
import threading
import time
from termcolor import colored
import numpy as np
import mining_api

# Connect to the host
sock, address = mining_api.connect()

# Fetch the most recent block
block, target, job_id, extranonce2 = mining_api.fetch_block(sock, address)

def get_num_leading_zeros(string):
  i = 1

  while True:
    if string[-i] != "0":
      return i - 1

    i += 1

def seconds_to_hms(seconds):
  hours = seconds // 3600
  seconds %= 3600
  minutes = seconds // 60
  return str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds % 60).zfill(2)

def search():
  global best_score, best_hash, hashes_since_last_report, integer_nonce

  while True:
    if integer_nonce >= max_nonce:
      return
    else:
      integer_nonce += 1

    nonce = hex(integer_nonce)[2:].zfill(8)
    header_hex = block['version'] + block['previous_block_hash'] + block['merkle_root'] + block['time'] + block['bits'] + nonce
    header_bin = binascii.unhexlify(header_hex)
    hash = hashlib.sha256(hashlib.sha256(header_bin).digest()).digest()
    hash = binascii.hexlify(hash).decode()

    if hash <= target:
      payload = '{"params": ["' + address + '", "' + job_id + '", "' + extranonce2 + '", "' + block['time'] + '", "' + nonce + '"], "id": 1, "method": "mining.submit"}\n'
      payload = bytearray(payload, 'utf-8')
      sock.sendall(payload)
      print (colored("Success!: {}".format(sock.recv(1024).decode()), "green"), end = "\r")
      exit()

    num_leading_zeros = get_num_leading_zeros(hash)

    if num_leading_zeros >= best_score:
      best_score = num_leading_zeros
      best_hash = hash

    hashes_since_last_report += 1

    if hashes_since_last_report % report_frequency == 0:
      hashes_since_last_report = 0
      duration = time.time() - start_time
     
      if duration >= max_search_time:
        return        

      hashrate = integer_nonce / duration
      completion = np.round(integer_nonce / max_nonce * 100, 3)
      time_remaining = seconds_to_hms(int(max_nonce / hashrate))
      time_until_termination = seconds_to_hms(max_search_time - int(duration))
      
      print ("Nonce: {}, Hash: {}, Score: {}, Best Score: {}, Best Hash: {}, Hashes Tried: {}, Hashrate: {} HPS, Duration: {} seconds, Completion: {}%, Time Remaining: {} seconds, Time Until Expected Mining Of The Block: {}".format(nonce, hash, num_leading_zeros, best_score, best_hash, integer_nonce, int(hashrate), np.round(duration, 1), completion, time_remaining, time_until_termination), end = "\r")
      sys.stdout.flush()

num_threads = 15
threads = [threading.Thread(target = search) for i in range(num_threads)]

best_score = 0
report_frequency = 1000
hashes_since_last_report = 0
integer_nonce = 0
max_nonce = 4294967295
max_search_time = 600
start_time = time.time()

for thread in threads:
  thread.start()

for thread in threads:
  thread.join()

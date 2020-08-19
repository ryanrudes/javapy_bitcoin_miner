# JavaPy Crypto Miner
A fast CPU cryptocurrency miner which employs Python as a web client to fetch transaction data, and java as the optimized brute-force hashing engine.
Python and Java scripts communicate and transfer data via a Python server, which is attended to by a Java client.
All 3 version are having one issue; they are all handling incoming information from the mining pool improperly, leading the to mine block headers with improper data. This is because I was previously unaware of the nonse reversing and reording that occurs before being broadcasted to the pool's miners. This will be fixed soon.

Note that this is unlikely to make you any money, for although this is considerably fast for a CPU, it is still a few thousand - 1 million times slower than the state-of-the-art ASIC mining devices. v3 runs at approx. 1.6 MH/s on an iMac Late 2012 with a 2.9 GHz Quad-Core Intel Core i5 processor, and I also tested in on a mac laptop from 2017, on which it runs at approx. 4.5 MH/s. To put this into perspective, the entire mining network acheives **many** more orders of magnitude of hashes per second.

v3 does not ask for user input at the moment, so if you want to run the most recent version, you must manually enter `mining_api.py` and change the variable labeled `address` to your own public wallet address.

**When you run it, make sure your terminal window is large; if your are on a laptop, you have to zoom out of your terminal a bit. Otherwise, the long lines will print on separate lines. If the window is large enough, your terminal should not get overflooded with status updates.**

To run v1:
```
git clone javapy_bitcoin_miner
cd javapy_bitcoin_miner
cd v1
pip3 install -r requirements.txt
python3 mine.py
```

To run v2:
```
git clone javapy_bitcoin_miner
cd javapy_bitcoin_miner
cd v2
pip3 install -r requirements.txt
javac Colors.java Mine.java Multithreading.java
java Mine
```

To run v3:
1. ```
   git clone javapy_bitcoin_miner
   cd javapy_bitcoin_miner
   cd v3
   pip3 install -r requirements.txt
   ```
2.  In another terminal window: `cd` to the approperiate directory and run `python3 Server.py`
3.  In one terminal window: `cd` to the approperiate directory and run `javac Client.java Colors.java Miner.java Multithreading.java; java Miner`

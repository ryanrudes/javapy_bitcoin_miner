# JavaPy Crypto Miner
A fast CPU cryptocurrency miner which employs Python as a web client to fetch transaction data, and java as the optimized brute-force hashing engine.
Python and Java scripts communicate and transfer data via a Python server, which is attended to by a Java client.
All 3 version are having one issue; they are all handling incoming information from the mining pool improperly, leading the to mine block headers with improper data. This is because I was previously unaware of the nonse reversing and reording that occurs before being broadcasted to the pool's miners. This will be fixed soon.

Note that this is unlikely to make you any money, for although this is considerably fast for a CPU, it is a few thousand - 1 million times slower than the state-of-the-art ASIC mining devices.

The newer version does not ask for user input at the moment, so if you want to run the most recent version, you must manually enter the Python API file's code and change the variable labeled `address` to your own public wallet address.

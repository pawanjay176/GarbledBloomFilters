# GarbledBloomFilters
Private set intersection using garbled bloom filters in semi-honest setting

Implementation of the Private set intersection protocol in the paper https://eprint.iacr.org/2013/515.pdf

Test implementation:
* Run server.py
* Run client.py
(Currently configured for same machine with port 3000. Can change port number and host in OTRecv.py and OTSender.py)

Concepts used:
* Bloom Filters
* Secret sharing
* Oblivious transfer (OT)

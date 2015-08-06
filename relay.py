#!/usr/bin/env python
#
# Author Dario Clavijo 2015
# GPLv3

import hashlib,utils,socket,random,struct
import time

magic = 0xd9b4bef9
 
def makeMessage(magic, command, payload):
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[0:4]
    return struct.pack('<L12sL4s', magic, command, len(payload), checksum) + payload
 
def getVersionMsg():
    version = 60002
    services = 1
    timestamp = int(time.time())
    addr_me = utils.netaddr(socket.inet_aton("127.0.0.1"), 8333)
    addr_you = utils.netaddr(socket.inet_aton("127.0.0.1"), 8333)
    
    nonce = random.getrandbits(64)
    sub_version_num = utils.varstr('')
    start_height = 0
 
    payload = struct.pack('<LQQ26s26sQsL', version, services, timestamp, addr_me,
        addr_you, nonce, sub_version_num, start_height)
    return makeMessage(magic, 'version', payload)

def getTxMsg(payload):
  return makeMessage(magic, 'tx', payload)


def relayTx(tx,node): 
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket.timeout = 1
	
	#print node
	
	sock.connect(node)
 
	sock.send(getVersionMsg())
	#print sock.recv(1000) # receive version
	#print sock.recv(1000) # receive verack
	sock.send(getTxMsg(tx.decode('hex')))
	print "Sent to ", node	
	sock.close

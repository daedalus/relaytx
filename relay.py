#!/usr/bin/env python
#
# Author Dario Clavijo 2015
# GPLv3

import hashlib
import utils
import socket
import random
import struct
import time
import sys

socket.timeout(5)
magic = 0xd9b4bef9
 
def makeMessage(magic, command, payload):
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[0:4]
    return struct.pack('<L12sL4s', magic, command, len(payload), checksum) + payload


def getVersionMsg():
    version = 70002
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


def disect_ping(p, length):
    nonce = p[0:0 + 8].encode('hex')
    return [nonce]


def disect_pong(p, length):
    nonce = p[0:0 + 8].encode('hex')
    return [nonce]


def disect_reject(p, length):
    msg = p[:length]
    return msg


# FIXME
def disect_inv(p, length):
    return p.encode('hex')


# FIXME
def disect_verack(p, length):
    return p.encode('hex')


def disect_inventory_item(p):
    type = p[0:0 + 4].encode('hex')
    hash = p[4:4 + 32].encode('hex')
    return[type,hash]


def disect_netaddress(p):
    time     = p[0:0:4].encode('hex')
    services = p[4:4 + 8].encode('hex')
    ipv64    = p[12:12 + 16].encode('hex')
    port     = p[16:16 + 2].encode('hex')
    return [time,services,ipv64,port]


def disect_version(p, l):
    version    = p[0:0 + 4].encode('hex')	
    services   = p[4:4 + 8].encode('hex')
    timestamp  = p[12:12 + 8].encode('hex')
    addr_recv  = disect_netaddress(p[20:20 + 26].encode('hex'))
    addr_from  = disect_netaddress(p[26:26 + 26].encode('hex'))
    nonce      = p[20:20 + 26].encode('hex')
    user_agent = repr(p[:46])
    return [version, services, timestamp, addr_recv, addr_from, nonce, user_agent]


# FIXME
def disect_getheaders(payload, length):
    return p.encode('hex')


def disect_msg(r):	
    # decode message fields
    # maybe this can be done with a struct.unpack
    s = [r[0:4], r[4:4 + 12], r[16:16 + 4], r[20:20 + 4], r[24:]]
    if s[0].encode('hex') == 'f9beb4d9':
        length = struct.unpack("<I", s[2])[0]
        command = s[1].replace('\0','')
        checksum = s[3].encode('hex')
        payload = s[4][:length]
        if command == 'version':
            decoded = disect_version(payload,length)
        elif command == 'inv':
            decoded = disect_inv(payload,length)
        elif command == 'reject':
            decoded = disect_reject(payload,length)
            if decoded.find('bad-txns-inputs-spent') > 0:
                # return -1
                sys.exit()
        elif command == 'getheaders':
            decoded = disect_getheaders(payload,length)
        elif command == 'verack':
            decoded = disect_verack(payload,length)
        elif command == 'ping':
            decoded = disect_ping(payload,length)
        else:
            decoded = repr(payload)
        print(command, length, decoded)


def relayTx(tx, node): 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:	
        sock.connect(node)
        print("connected...")
        sock.send(getVersionMsg())
        disect_msg(sock.recv(1000))
        disect_msg(sock.recv(1000))
        sock.send(getTxMsg(tx.decode('hex')))
        disect_msg(sock.recv(1000))
        disect_msg(sock.recv(1000))
        sock.close()
    except:
        print("Socket Exception")


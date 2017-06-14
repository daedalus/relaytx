#!/usr/bin/env python
#
# Author Dario Clavijo 2015
# GPLv3

import relay
import sys
import random
import dns_resolver
import fileinput
import threading
#import logging

#FORMAT = '%(asctime)-15s %(message)s'
#logging.basicConfig(filename='/tmp/relay.log',level=logging.DEBUG,format=FORMAT)


threads = []

def newthread(target,args):

	#print target,args

        t = threading.Thread(target=target,args=args)
        threads.append(t)
        t.start()
        #print threading.currentThread().getName(),"Started"


nodes = []
limit = 1500


def addnode(nodes,node):
	node = node.replace('\n','').replace('\r','')
               #if c <= limit:
        if (node.find("]") > 0):
        	node = node.replace("]:","] ").split(" ")
       	else:
		node = node.split(':')

	if len(node) == 1:
		node.append('8333')

	if node not in nodes:
		nodes.append(node)

	return nodes

def loadnodes():
	#nodes = dns_resolver.nslookup('bitseed.xf2.org')

	nodes = []
	c = 0

	fp = open('/tmp/nodes.txt')

	for node in fp:
		nodes = addnode(nodes,node)
	fp.close()
	return nodes

def addnodes(nodes):
	nodes = addnode(nodes,'respends.thinlink.com:8333')
	nodes = addnode(nodes,'www.f2pool.com')

	# seeds
	nodes = addnode(nodes,'bitseed.xf2.org')
	nodes = addnode(nodes,'dnsseed.bluematt.me')
	nodes = addnode(nodes,'seed.bitcoin.sipa.be')
	nodes = addnode(nodes,'dnsseed.bitcoin.dashjr.org')
	nodes = addnode(nodes,'seed.bitcoinstats.com')

	return nodes

def prepare(nodes):

	random.shuffle(nodes)
	nodes = nodes[0:limit]
	nodes = addnodes(nodes)
	nodes = nodes[::-1]

	return nodes

def broadcast(nodes,tx):
	for node in nodes:
		print node
        	#print "Sending TX: %s to node: %s" % (tx,node[0])
		relay.relayTx(tx,(node[0],int(node[1])))

def main():
	if len(sys.argv)>1:
		tx = sys.argv[1]
		nodes = loadnodes()
		nodes = prepare(nodes)

		print nodes
		for i in range(0,4):
			#print tx
			newthread(target=broadcast,args=(nodes,tx,))	
			random.shuffle(nodes)
			#broadcast(tx)

main()

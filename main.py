#!/usr/bin/env python
#
# Author Dario Clavijo 2015
# GPLv3

import relay
import sys
import random
import dns_resolver
import fileinput

nodes = []
limit = 5000

def broadcast(tx):
	#nodes = dns_resolver.nslookup('bitseed.xf2.org')

	nodes = []
	c = 0

	fp = open('/tmp/nodes.txt')

	for node in fp:
		node = node.replace('\n','').replace('\r','')
		
		if c <= limit:
			if (node.find("[") > 0 and node.find("]") > 0):
				node = node.replace("]:","] ").split(" ")
			else:
				node = node.split(':')
			
			nodes.append(node)
			c += 1
		else:
			break

	#nodes = nodes[:100]
	
	random.shuffle(nodes)

	for node in nodes:
        	print "Sending TX: %s to node: %s" % (tx,node[0])
		relay.relayTx(tx,(node[0],int(node[1])))

def main():
	if len(sys.argv)>1:
		tx = sys.argv[1]
		broadcast(tx)
	else:
		for line in fileinput.input():
			broadcast(line.replace('\n',''))

main()

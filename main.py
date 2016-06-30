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


def broadcast(tx):
	nodes = dns_resolver.nslookup('bitseed.xf2.org')
	for node in nodes:
        	print "Sending TX: %s to node: %s" % (tx,node)
		relay.relayTx(tx,(node,8333))

def main():
	if len(sys.argv)>1:
		tx = sys.argv[1]
		broadcast(tx)
	else:
		for line in fileinput.input():
			broadcast(line.replace('\n',''))

main()

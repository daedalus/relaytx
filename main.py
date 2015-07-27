import relay
import sys

nodes = []


tx = None
node = None

if len(sys.argv)>0:
	tx = sys.argv[1]
if len(sys.argv)>1:
	node = (sys.argv[2],8333)

if node:
	try:
		print relay.relayTx(tx,node)
	except:
		print "Error",node
else:
	fp = open('nodes.txt')

	for line in fp:
		line = line.rstrip()
		tokens = line.split()
		nodes.append((tokens[0],tokens[1]))

	for node in nodes:
		try:
			print relay.relayTx(tx,node)
		except:
			print "Error",node

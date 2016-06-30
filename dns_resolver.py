import socket

def nslookup(hostname):
	ip_list = []
	ais = socket.getaddrinfo(hostname,0,0,0,0)
	for result in ais:
		ip_list.append(result[-1][0])
		#ip_list = list(set(ip_list))

	return ip_list

def test():
	print nslookup('bitseed.xf2.org')

import socket

def nslookup(hostname):
    ais = socket.getaddrinfo(hostname,0,0,0,0)
    return [result[-1][0] for result in ais]

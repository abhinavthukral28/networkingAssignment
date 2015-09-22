import socket, sys

server = socket.socket()
server.connect(("localhost", 1234))
data = []
size = int(server.recv(1024))

while(size):
    data = server.recv(1024)
    print data
    size -= 1
server.close()



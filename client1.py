import socket, sys, pickle

server = socket.socket()
server.connect(("localhost", 1234))

server.send("ls")
data = server.recv(4096)
d1 = pickle.loads(data)

for i in range(0, len(d1)):
    print d1[i]
server.close()

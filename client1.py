import socket, sys, pickle

server = socket.socket()
server.connect(("localhost", 1234))
stat = ''
cmd = 'ls'

server.send(cmd.encode())
stat = server.recv(1024).decode()
print(stat)
server.send("./".encode())
data = server.recv(4096)
d1 = pickle.loads(data)

for i in range(0, len(d1)):
    print(d1[i])
server.close()

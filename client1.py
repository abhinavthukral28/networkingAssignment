import socket, sys, pickle

server = socket.socket()
server.connect(("localhost", 1234))
data = ''
server.send('ls')
#size = int(server.recv(1024))

#if(cmd == 'ls'):
#for i in range(0, size/2):
data = server.recv(4096)
data1 = pickle.loads(data)
print data1
for i in range(0, len(data1)):
    print data1[i]     
server.close()



import socket, sys, pickle

#connect to server
server = socket.socket()
server.connect(("localhost", 1234))
stat = ''
path = './'

#send command to a server
server.send("ls")
stat = server.recv(1024)
print stat
server.send(path)
#get list of files
data = server.recv(4096)
#deserialize recieved list
d1 = pickle.loads(data)

#print file names
for i in range(0, len(d1)):
    print d1[i]
server.close()

import socket, sys, pickle

#connect to server
server = socket.socket()
server.connect(("localhost", 1234))

#send command to a server
server.send("ls")
#get list of files
data = server.recv(4096)
#deserialize recieved list
d1 = pickle.loads(data)

#print file names
for i in range(0, len(d1)):
    print d1[i]
server.close()

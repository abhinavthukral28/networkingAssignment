import socket, sys, pickle

#connect to server
server = socket.socket()
server.connect(("localhost", 1234))
stat = ''

#send comd
server.send("ls")
#recive status
stat = server.recv(1024)
print stat
#send dir
server.send('./')
#recieve files in dir
data = server.recv(4096)
#deserialize aray
d1 = pickle.loads(data)

#print
for i in range(0, len(d1)):
    print d1[i]
server.close()

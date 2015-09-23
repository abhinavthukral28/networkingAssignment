import socket, sys, pickle, os

#create socket
server = socket.socket()
server.bind(("localhost", 1234))
server.listen(1)

#get list of filenames in curr directory
path = "./"
dirs = os.listdir( path )


while True:
    #accept client
    remoteSocket, remoteAddr = server.accept()
    cmd = remoteSocket.recv(1024) #recieve command
    if(cmd == 'ls'):
        data = pickle.dumps(dirs) #serialize an array
        remoteSocket.send(data); #send an array
server.close()


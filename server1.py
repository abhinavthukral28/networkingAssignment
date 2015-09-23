import os, sys, socket, pickle

server = socket.socket()
server.bind(("localhost", 1234))
server.listen(1)

path = "./"
dirs = os.listdir(path)

while True:
    remoteSocket, remoteAddr = server.accept()
    cmd = remoteSocket.recv(1024)
    print cmd
    if cmd == 'ls':
        data = pickle.dumps(dirs)
        remoteSocket.send(data)
    remoteSocket.close()
server.close()
        

import socket, sys, pickle, os

server = socket.socket()
server.bind("localhost", 1234))
server.listen(1)

while True:
    remoteSocket, remoteAddr = server.accept()
    cmd = remoteSocket.recv(1024).decode()
    print(cmd)
    if(cmd == "ls):
        remoteSocket.send("Ls recieved".encode())
        path = remoteSocket.recv(1024).decode()
        dirs = os.listdir(path)
        data = pickle.dumps(dirs)
        remoteSocket.send(data)
server.close()

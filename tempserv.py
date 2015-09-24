import socket
import sys
#Setup the server to listen
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost",1234))
server.listen(1)
print("Server Started.\n")
remoteSocket, remoteAddress = server.accept()
while True:
    command = remoteSocket.recv(1024).decode()
    if(command == 'get'):
        fileName = remoteSocket.recv(1024).decode()
        fileType = remoteSocket.recv(1024).decode()
        fileLocation = remoteSocket.recv(1024).decode()
        #NEED to check if file exists
        if(True):
            #if file is found
            remoteSocket.send('OK'.encode())
            file = open (fileName+'.'+fileType, "rb") 	
            data = file.read(1024) 			            
            while (data):					
                remoteSocket.send(data)			
                data = file.read(1024)
            print('line 24')
            command = ' '
        else:
            remoteSocket.send('N_OK'.encode())
            command = ' '
    if(command == 'quit'):
        break;


  #  newFile = open('newCat'+".jpg",'wb') 				#Opens the file in binary, will write to this

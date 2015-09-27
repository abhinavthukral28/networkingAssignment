import socket, sys, pickle, os

#Setup the server to listen
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost",1234))
server.listen(1)
print("Server Started.\n")
os.chdir("serverFiles")
homeDir = os.getcwd();

while True:
    remoteSocket, remoteAddress = server.accept()
    command = remoteSocket.recv(1024).decode()
    print(command)
    
    if(command == 'ls'):
        #Rita
        path = remoteSocket.recv(4096).decode()
        dirs = os.listdir(path)
        data = pickle.dumps(dirs)
        remoteSocket.send(data)
        
        
    if(command == 'get'):
        #Mark
        fileName = remoteSocket.recv(1024).decode()
        fileType = remoteSocket.recv(1024).decode()
        fileLocation = remoteSocket.recv(1024).decode()
        fileExists = 'yes'
        #Find out if the file exists
        try:
            with open(fileLocation + fileName + '.' + fileType) as file:
                pass
        except IOError as e:
            fileExists = 'no'
        
        if(fileExists == 'yes'):
            #if file is found
            remoteSocket.send('OK'.encode())
            file = open (fileLocation + fileName + '.'+fileType, "rb") 	
            data = file.read(1024) 			            
            while (data):					
                remoteSocket.send(data)			
                data = file.read(1024)
            remoteSocket.shutdown(socket.SHUT_WR)
            remoteSocket.close()
            command = ' '
        else:
            remoteSocket.send('N_OK'.encode())
            command = ' '
            
            
    if(command == 'put'):
        #Rita
        fileName = remoteSocket.recv(1024).decode()
        fileType = remoteSocket.recv(1024).decode()
        fileLocation = remoteSocket.recv(1024).decode()
        
        newFile = open(fileLocation + fileName + '.'+ fileType,'wb') 				
        data = remoteSocket.recv(1024) 						
        while (data): 										
            newFile.write(data) 							
            data = remoteSocket.recv(1024)
        newFile.close()
        command = ' '
       
    if(command == 'cd'):
        #Abhinav
        # receive info about the requested path, if its valid send 'OK', if it isnt send 'N_OK'
        cdResponse = ""
        path = remoteSocket.recv(1024).decode()
        if(path == ".." and homeDir == os.getcwd()):
            cdResponse = "N_OK"

        elif(path == ".." and os.path.exists(path)):
            os.chdir(path)
            cdResponse = os.getcwd()

        elif(os.path.exists(homeDir + "/" + path)):
            os.chdir(homeDir + "/" + path)
            cdResponse = os.getcwd()
        else:
            cdResponse = "N_OK"

        remoteSocket.send(cdResponse.encode())
        print(os.getcwd())
        command = ' '

    if(command == 'mkdir'):
        #Jeremy
        #check if directory exists, if it doesnt send 'OK' if not send 'N_OK'
        break;
    


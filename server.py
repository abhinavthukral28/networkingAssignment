import socket, sys, pickle, os

addr = socket.gethostbyname(socket.gethostname())
port = 8080

#Setup the server to listen
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((addr,8080))
server.listen(1)
os.chdir('serverFiles')
print("Server Started.\n")
print("Server address: " + addr)
print("Server port:    " + str(port))

#Variables
homeDir = os.getcwd()
userVisibleDir = ''

while True:
    remoteSocket, remoteAddress = server.accept()
    command = remoteSocket.recv(1024).decode()
    
    if(command == ' '):
        #Send currentDir to user for prompt
        remoteSocket.send(os.getcwd().encode())
        command = remoteSocket.recv(1024).decode()
        
    if(command == 'ls'):
        #Ls
        dirs = os.listdir(os.getcwd())
        data = pickle.dumps(dirs)
        remoteSocket.send(data)
        
            
    if(command == 'get'):
        #Get
        print(os.getcwd())
        fileName = remoteSocket.recv(1024).decode()
        print(fileName)
        # fileType = remoteSocket.recv(1024).decode()
        fileExists = 'yes'
        #Find out if the file exists
        try:
            with open(fileName) as file:
                pass
        except IOError as e:
            fileExists = 'no'
        
        if(fileExists == 'yes'):
            #if file is found
            remoteSocket.send('OK'.encode())
            file = open (fileName, "rb")
            data = file.read(1024) 			            
            while (data):					
                remoteSocket.send(data)			
                data = file.read(1024)
            remoteSocket.shutdown(socket.SHUT_WR)
            remoteSocket.close()
            print('Sent ' + fileName +' from ' + os.getcwd() + '\n')
        else:
            remoteSocket.send('N_OK'.encode())
            
            
    if(command == 'put'):
        #Rita
        fileName = remoteSocket.recv(1024).decode()
        fileType = remoteSocket.recv(1024).decode()
        newFile = open(fileName + '.'+ fileType,'wb') 				
        data = remoteSocket.recv(1024) 						
        while (data): 										
            newFile.write(data) 							
            data = remoteSocket.recv(1024)
        newFile.close()
        print('Received ' + fileName + '.' + fileType + '\n')
       
    if(command == 'cd'):
    #cd command
        cdResponse = ""
        path = remoteSocket.recv(1024).decode()
        
        if (path == ".." and homeDir == os.getcwd()):
            cdResponse = "N_OK"

        elif (path == ".." and os.path.exists(path)):
            os.chdir(path)
            cdResponse = os.getcwd()

        elif (os.path.exists(os.getcwd() + "/" + path)):
            os.chdir(os.getcwd() + "/" + path)
            cdResponse = os.getcwd()
        else:
            cdResponse = "N_OK"

        remoteSocket.send(cdResponse.encode())

        
    if(command == 'mkdir'):
        #mkdir command
        path = remoteSocket.recv(1024).decode()
        try:
            os.makedirs(os.getcwd() + "/" + path)
            remoteSocket.send("OK".encode())


        except OSError:
            if not os.path.isdir(os.getcwd() + "/" + path):
                remoteSocket.send("OK".encode())

            else:
                remoteSocket.send("N_OK".encode())
                # Error occured

    if(command == 'quit'):
        remoteSocket.close()
        os.chdir(homeDir)
    


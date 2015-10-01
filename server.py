import socket, sys, pickle, os

addr = socket.gethostbyname(socket.gethostname())
port = 8080

#Setup the server to listen
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((addr,8080)) # binds socket address to port number 8080
server.listen(1) # server listens for incoming connection
os.chdir('serverFiles') # changes directory to server directory
print("Server Started.\n")
print("Server address: " + addr)
print("Server port:    " + str(port))

#Variables
homeDir = os.getcwd() # home directory is initial current working directory

while True:
    remoteSocket, remoteAddress = server.accept() # server accepts requests from client
    command = remoteSocket.recv(1024).decode() # server receives command request from client
    
    if(command == ' '):
        #Send currentDir to user for prompt
        remoteSocket.send(os.getcwd().encode())
        command = remoteSocket.recv(1024).decode() # server receives command request from client
        
    if(command == 'ls'):
        #Ls
        print("ls command recieved.")
        dirs = os.listdir(os.getcwd()) # retrieves list of directories in current working directory
        data = pickle.dumps(dirs) # store this list of directories
        remoteSocket.send(data) # send this list back to client
        
            
    if(command == 'get'):
        #Get
        print("get command recieved.")
        print(os.getcwd()) # prints current working directory
        fileName = remoteSocket.recv(1024).decode() # server receives fileName request from client
        print(fileName)
        # fileType = remoteSocket.recv(1024).decode()
        fileExists = 'yes'
        #Find out if the file exists
        try:
            with open(fileName) as file:
                pass
        except IOError as e: # throws exception error when no such file exists
            fileExists = 'no'
        
        if(fileExists == 'yes'):
            #if file is found
            remoteSocket.send('OK'.encode()) # send response to client
            file = open (fileName, "rb")
            data = file.read(1024) 	# read file data on server		            
            while (data):					
                remoteSocket.send(data)	# send file data to client		
                data = file.read(1024) # read file data on server
            remoteSocket.shutdown(socket.SHUT_WR) # shuts down socket when file is fully retrieved from server
            remoteSocket.close()
            print('Sent ' + fileName +' from ' + os.getcwd() + '\n')
        else:
            remoteSocket.send('N_OK'.encode()) # file does not exist
            
            
    if(command == 'put'):
        #Put
        print("put command recieved.")
        remoteSocket.send("recieved".encode()) # send response to client
        fileName = remoteSocket.recv(1024).decode() # receive fileName request from client
        remoteSocket.send("recieved".encode()) # send response to client
        fileType = remoteSocket.recv(1024).decode() # receive fileType request from client
        remoteSocket.send("recieved".encode()) # send response to client
        newFile = open(fileName + '.'+ fileType,'wb') # variable to read and write new file 				
        data = remoteSocket.recv(1024) # receive data from client for new server file 						
        while (data): 										
            newFile.write(data) # write new data for file to server 							
            data = remoteSocket.recv(1024) # receive data from client for new server file
        newFile.close() # close new file once completed
        print('Received ' + fileName + '.' + fileType + '\n')
       
    if(command == 'cd'):
    #cd command
        print("cd command recieved.")
        cdResponse = ""
        path = remoteSocket.recv(1024).decode() # receives path request from client
        
        if (path == ".." and homeDir == os.getcwd()): # if currently in the home directory and path is a higher level of directory
            cdResponse = "N_OK" # cannot change to a higher level of directory

        elif (path == ".." and os.path.exists(path)): # if not currently in the home directory and path is a higher level of directory
            os.chdir(path) # change directory to this path
            cdResponse = os.getcwd() # send current working directory as response to client

        elif (os.path.exists(os.getcwd() + "/" + path)): # if user wants to move down a level of directory (sub-directory)
            os.chdir(os.getcwd() + "/" + path) # change current working directory to sub-directory
            cdResponse = os.getcwd() # send current working directory as response
        else:
            cdResponse = "N_OK" # cannot change level of directory

        remoteSocket.send(cdResponse.encode()) # send response to client

        
    if(command == 'mkdir'):
        #mkdir command
        print("mkdir command recieved.")
        path = remoteSocket.recv(1024).decode() # receives path request from client
        #Check if we can make a directory with the given path name
        try:
            os.makedirs(os.getcwd() + "/" + path) # try to make directory with given path from the client
            remoteSocket.send("OK".encode()) # send response to client


        except OSError: # throw an exception error if directory cannot be made
            if not os.path.isdir(os.getcwd() + "/" + path): # if directory does not currently exist
                remoteSocket.send("OK".encode()) # create the directory

            else:
                remoteSocket.send("N_OK".encode()) # directory cannot be made
                # Error occured

    if(command == 'quit'): # quit command
        remoteSocket.close() # close the socket
        os.chdir(homeDir) # change to the home directory
    


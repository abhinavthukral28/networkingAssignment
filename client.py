import socket, sys, pickle

#Function definitions
def formatInput(rawInput): # takes raw input from user
    "Format the user input into command, fileName, fileType, changeDir, and makeDir"
    if(len(rawInput)<=1): # user does not enter anything and presses enter
        #Bad command
        return ' ', ' ', ' ', ' ', ' '
        
    if(rawInput[0:2] == 'ls'): # user selects ls
        #List directory command
        return 'ls', ' ', ' ', ' ', ' '
        
    if(rawInput[0:4] == 'get ' and len(rawInput) >= 7): # user selects a valid directory name
        #Get a file command
        file = rawInput[4:len(rawInput)] # files becomes the one selected by user
        i = len(file) -1; # iterator 
        if(checkForInvalidCharactersInFile(file)): # ensures file name is valid
            #Error checking for invalid characters
            print('File names can not contain / | * < > : ;\n\n')
            return ' ', ' ', ' ', ' ', ' '
            
        while(file[i] != '.'): # looks for a splice in the file name
            #Find the position of the . and splice the file name and type
            if(i==0): 
                #If no period is found
                print('You must specifiy a File Type\n\n')
                return ' ', ' ', ' ', ' ', ' '
            i -= 1 # counts down in the iterator
        fileName = file[0:i] # retrieve the name of file
        fileType = file[i+1:len(file)] # retrieve the type of file
        return 'get', fileName, fileType, ' ', ' ' # retrieve full path of file
    
    if(rawInput[0:4] == 'put ' and len(rawInput) >= 7): # if user selects the put command
        #Put a file command
        file = rawInput[4:len(rawInput)] # file becomes the user input
        i = len(file) -1; # iterator
        if(checkForInvalidCharactersInFile(file)): # checks for invalid characters
            #Error checking for invalid characters
            print('File names can not contain / | * < > : ;\n\n')
            return ' ', ' ', ' ', ' ', ' '
            
        while(file[i] != '.'): # looks for a splice in the file name
            #Find the position of the period and splice the file name and type
            if(i==0):
                #If no period is found
                print('You must specifiy a File Type\n\n')
                return ' ', ' ', ' ', ' ', ' '
            i -= 1
  
        fileName = file[0:i] # file of name without the splice
        fileType = file[i+1:len(file)] # type of file is given after the splice
        return 'put', fileName, fileType, ' ', ' ' # file name length in total
        
    if(rawInput[0:3] == 'cd ' and len(rawInput) >= 4): # user selects cd and enters valid file name
        #Cd command
        directory = rawInput[3:len(rawInput)] # name of directory
        return 'cd', ' ', ' ', directory, ' ' # changes directory to given name
        
    if(rawInput[0:6] == 'mkdir ' and len(rawInput) >= 7): # user selects the mkdir command
        #Mkdir command
        directory = rawInput[6:len(rawInput)] # name of directory
        return 'mkdir', ' ', ' ', ' ', directory # makes directory with given name
        
    if(rawInput[0:4] == 'quit'): # user selects to quit
        #Quit command
        return 'quit', ' ', ' ', ' ', ' ' # quits the program
        
    else:
        print('Invalid Command\n\n') # all other user input is invalid
        return ' ', ' ', ' ', ' ', ' '
        
def checkForInvalidCharactersInFile(text):
    "Returns true if the text contains invalid characters"
    i = len(text) - 1 # iterator
    while(i >= 0):
        if(text[i] == '/' or text[i] == '*' or text[i] == ';' or text[i] == ':' or text[i] == '>' or text[i] == '<' or text[i] == '|'): # looks for special characters in file
            return True
        i -= 1 # iterates through the length of the file name
    return False
    
def checkForInvalidCharactersInDirectory(text):
    "Returns true if the text contains invalid characters"
    i = len(text) - 1 # iterator
    while(i >= 0):
        if(text[i] == '*' or text[i] == ';' or text[i] == ':' or text[i] == '>' or text[i] == '<' or text[i] == '|'): # looks for special charactes in directory
            return True
        i -= 1 # iterates through lenght of directory name
    return False
    
#Variables                          
rawInput    = ' '                        #Unformatted user input
command     = ' '                        #Formatted command from the user
fileName    = ' '                        #Formatted fileName from the user   
fileType    = ' '                        #Formatted fileType from the user
changeDir   = ' '                        #Formatted directory the user would like to try and go to
makeDir     = ' '                        #Formatted directory the user would like to create

addr = ''
port = ''

addr = input("Please, enter server address:\n");
port = input("Please, enter server port: \n");

print('Connecting to server...\n\n')
while command == ' ':

    #Connect to the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((addr,int(port)))
    
    if(command == ' '):
    #Used to get the current directory from the server
        server.send(command.encode())
        currentDir = server.recv(1024).decode()
        command == ' '
        rawInput = input(currentDir + '>') 
        command, fileName, fileType, changeDir, makeDir = formatInput(rawInput)

        
    if(command == 'ls'):
    #Rita
        print('\n    Directory: ' + currentDir + '\n')
        server.send(command.encode()) # send command to server
        data = server.recv(4096) # receive response from server
        d1 = pickle.loads(data) # store the response
        for i in range(0, len(d1)):
            print('    ' + d1[i])
        command = ' '
        print('\n')
    
    if(command == 'get'):
    #Mark
        #Send the command, fileName, fileType, and fileLocation to the server
        server.send(command.encode()) # send command to server
        server.send((fileName + "." + fileType).encode()) # send filename to server
        # server.send(fileType.encode())
        print(fileName,fileType)
        response = server.recv(1024).decode() # receive response from server
        
        if( response == 'OK'):
            #If the server has the file
            newFile = open(fileName + '.'+fileType,'wb') 				
            data = server.recv(1024) # receive response from server 						
            while (data): 										
                newFile.write(data) # writes file from server to a new client location							
                data = server.recv(1024) # receive response from server
            newFile.close() # close file once it has finished writing to client location
            
        else:
            #If the server can't find the file
            print("Can't find the file on the server\n\n")
            command = ' '
            continue
        #It worked!
        print("File received.\n\n")
        command = ' '
        
    if(command == 'put'):
    #Put command
        stat = ''
        fileExists = 'yes'
        #Check to make sure the local file exists before communicating with the server
        try: 
            with open(fileName + '.' + fileType) as file:
                pass
        except IOError as e: # throw an exception error if no file is found
            fileExists = 'no'
        if(fileExists == 'no'):
            print('Can not find the file in your directory\n\n')
            command = ' '
            continue
        server.send(command.encode()) # send command request to server
        stat = server.recv(1024).decode() # server receives request from client
        server.send(fileName.encode()) # send filename request to server
        stat = server.recv(1024).decode() # server receives request from client
        server.send(fileType.encode()) # send filetype request to server
        stat = server.recv(1024).decode() # server receives request from client

        file = open (fileName + '.'+fileType, "rb") # read and write file to server	
        data = file.read(1024) 	# read the file		            
        while (data):					
            server.send(data)	# send data file to server		
            data = file.read(1024) # read the data file on server
        server.shutdown(socket.SHUT_WR)
        server.close()
        print('File sent to the server\n\n')
        command = ' '
        
        
    if(command == 'cd'):
    #Cd command
        server.send(command.encode()) # send command request to server
        server.send(changeDir.encode()) # send changeDir request to server
        d2 = server.recv(1024).decode() # receive response from server
        if( d2 == "N_OK"): # invalid directory path
            print("Invalid Path\n")
        print('\n')
        command = ' '
        
        
    if(command == 'mkdir'):
    #Mkdir command
        server.send(command.encode()) # send command request to server
        server.send(makeDir.encode()) # send makeDir request to server
        d3 = server.recv(1024).decode() # receive response from server
        if(d3 == "OK"): # valid directory name
            print("Directory(s) created\n\n")
        else:
            print("Directory not created\n\n")

        command = ' '
        
    if(command == 'quit'):
    #quit command
        server.send(command.encode()) # send command request to server
        print('Goodbye!\n\n')
        break

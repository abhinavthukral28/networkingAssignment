import socket, sys, pickle

#Function definitions
def formatInput(rawInput):
    "Format the user input into command, fileName, fileType, changeDir, and makeDir"
    if(len(rawInput)<=1):
        #Bad command
        return ' ', ' ', ' ', ' ', ' '
        
    if(rawInput[0:2] == 'ls'):
        #List directory command
        return 'ls', ' ', ' ', ' ', ' '
        
    if(rawInput[0:4] == 'get ' and len(rawInput) >= 7):
        #Get a file command
        file = rawInput[4:len(rawInput)]
        i = len(file) -1;
        if(checkForInvalidCharactersInFile(file)):
            #Error checking for invalid characters
            print('File names can not contain / | * < > : ;\n\n')
            return ' ', ' ', ' ', ' ', ' '
            
        while(file[i] != '.'):
            #Find the position of the . and splice the file name and type
            if(i==0):
                #If no period is found
                print('You must specifiy a File Type\n\n')
                return ' ', ' ', ' ', ' ', ' '
            i -= 1
        fileName = file[0:i]
        fileType = file[i+1:len(file)]       
        return 'get', fileName, fileType, ' ', ' '
    
    if(rawInput[0:4] == 'put ' and len(rawInput) >= 7):
        #Put a file command
        file = rawInput[4:len(rawInput)]
        i = len(file) -1;
        if(checkForInvalidCharactersInFile(file)):
            #Error checking for invalid characters
            print('File names can not contain / | * < > : ;\n\n')
            return ' ', ' ', ' ', ' ', ' '
            
        while(file[i] != '.'):
            #Find the position of the period and splice the file name and type
            if(i==0):
                #If no period is found
                print('You must specifiy a File Type\n\n')
                return ' ', ' ', ' ', ' ', ' '
            i -= 1
  
        fileName = file[0:i]
        fileType = file[i+1:len(file)]
        return 'put', fileName, fileType, ' ', ' '
        
    if(rawInput[0:3] == 'cd ' and len(rawInput) >= 4):
        #Cd command
        directory = rawInput[3:len(rawInput)]
        return 'cd', ' ', ' ', directory, ' '
        
    if(rawInput[0:6] == 'mkdir ' and len(rawInput) >= 7):
        #Mkdir command
        directory = rawInput[6:len(rawInput)]
        return 'mkdir', ' ', ' ', ' ', directory
        
    if(rawInput[0:4] == 'quit'):
        #Quit command
        return 'quit', ' ', ' ', ' ', ' '
        
    else:
        print('Invalid Command\n\n')
        return ' ', ' ', ' ', ' ', ' '
        
def checkForInvalidCharactersInFile(text):
    "Returns true if the text contains invalid characters"
    i = len(text) - 1
    while(i >= 0):
        if(text[i] == '/' or text[i] == '*' or text[i] == ';' or text[i] == ':' or text[i] == '>' or text[i] == '<' or text[i] == '|'):
            return True
        i -= 1
    return False
    
def checkForInvalidCharactersInDirectory(text):
    "Returns true if the text contains invalid characters"
    i = len(text) - 1
    while(i >= 0):
        if(text[i] == '*' or text[i] == ';' or text[i] == ':' or text[i] == '>' or text[i] == '<' or text[i] == '|'):
            return True
        i -= 1
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
        server.send(command.encode())
        data = server.recv(4096)
        d1 = pickle.loads(data)
        for i in range(0, len(d1)):
            print('    ' + d1[i])
        command = ' '
        print('\n')
    
    if(command == 'get'):
    #Mark
        #Send the command, fileName, fileType, and fileLocation to the server
        server.send(command.encode())
        server.send((fileName + "." + fileType).encode())
        # server.send(fileType.encode())
        print(fileName,fileType)
        response = server.recv(1024).decode()
        
        if( response == 'OK'):
            #If the server has the file
            newFile = open(fileName + '.'+fileType,'wb') 				
            data = server.recv(1024) 						
            while (data): 										
                newFile.write(data) 							
                data = server.recv(1024)
            newFile.close()
            
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
        fileExists = 'yes'
        #Check to make sure the local file exists before communicating with the server
        try:
            with open(fileName + '.' + fileType) as file:
                pass
        except IOError as e:
            fileExists = 'no'
        if(fileExists == 'no'):
            print('Can not find the file in your directory\n\n')
            command = ' '
            continue
        server.send(command.encode())
        server.send(fileName.encode())
        server.send(fileType.encode())

        file = open (fileName + '.'+fileType, "rb") 	
        data = file.read(1024) 			            
        while (data):					
            server.send(data)			
            data = file.read(1024)
        server.shutdown(socket.SHUT_WR)
        server.close()
        print('File sent to the server\n\n')
        command = ' '
        
        
    if(command == 'cd'):
    #Cd command
        server.send(command.encode())
        server.send(changeDir.encode())
        d2 = server.recv(1024).decode()
        if( d2 == "N_OK"):
            print("Invalid Path\n")
        print('\n')
        command = ' '
        
        
    if(command == 'mkdir'):
    #Mkdir command
        server.send(command.encode())
        server.send(makeDir.encode())
        d3 = server.recv(1024).decode()
        if(d3 == "OK"):
            print("Directory(s) created\n\n")
        else:
            print("Directory not created\n\n")

        command = ' '
        
    if(command == 'quit'):
        server.send(command.encode())
        print('Goodbye!\n\n')
        break

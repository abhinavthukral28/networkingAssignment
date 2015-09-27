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
            print('File names can not contain / | * < > : ;\n')
            return ' ', ' ', ' ', ' ', ' '
            
        while(file[i] != '.'):
            #Find the position of the . and splice the file name and type
            if(i==0):
                #If no period is found
                print('You must specifiy a File Type\n')
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
            print('File names can not contain / | * < > : ;\n')
            return ' ', ' ', ' ', ' ', ' '
            
        while(file[i] != '.'):
            #Find the position of the period and splice the file name and type
            if(i==0):
                #If no period is found
                print('You must specifiy a File Type\n')
                return ' ', ' ', ' ', ' ', ' '
            i -= 1
  
        fileName = file[0:i]
        fileType = file[i+1:len(file)]
        return 'put', fileName, fileType, ' ', ' '
        
    if(rawInput[0:3] == 'cd ' and len(rawInput) >= 4):
        
        directory = rawInput[3:len(rawInput)]
        #Error checking on directory to ensure it is a valid path
        #Directory will be concatinated with ./serverFiles/
        #So a valid return would be someFiles or someFiles/moreFiles/evenMore/youGetThePoint
        #Do all error checking for these possible commands (..), (cd /someFiles/), (cd someFiles), (cd /someFiles), (cd someFiles/)
        #To do this, check the first and last character to see if it is a /, and format accordingly
        #Also check to make sure it does not contain invalid characters, I made a function for this called checkForInvalidCharactersInDirectory
        #A side note, the highest level directory the user can see would be ./serverFiles/

        return 'cd', ' ', ' ', directory, ' '
        
    if(rawInput[0:6] == 'mkdir ' and len(rawInput) >= 7):
        directory = rawInput[6:len(rawInput)]
        #Same error checking as above for cd
        return ' ', ' ', ' ', ' ', directory
        
    if(rawInput[0:4] == 'quit'):
        return 'quit', ' ', ' ', ' ', ' '
        
    else:
        print('Invalid Command\n')
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
homeDir     = '.'           #The user can not go higher than this level
currentDir  = '.'           #Keep track of the current directory the user is in on the server
rawInput    = ' '                        #Unformatted user input
command     = ' '                        #Formatted command from the user
fileName    = ' '                        #Formatted fileName from the user   
fileType    = ' '                        #Formatted fileType from the user
changeDir   = ' '                        #Formatted directory the user would like to try and go to
makeDir     = ' '                        #Formatted directory the user would like to create


while command == ' ':
    #Connect to the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("localhost",1234))
    
    rawInput = input("Enter a command:\n")
    command, fileName, fileType, changeDir, makeDir = formatInput(rawInput)

    if(command == 'ls'):
    #Rita
        server.send(command.encode())
        server.send(currentDir.encode())
        data = server.recv(1024)
        d1 = pickle.loads(data)
        print('Files inside '+ currentDir + ' :\n')
        for i in range(0, len(d1)):
            print(d1[i])
        command = ' '
    
    if(command == 'get'):
    #Mark
        #Send the command, fileName, fileType, and fileLocation to the server
        server.send(command.encode())
        server.send(fileName.encode())
        server.send(fileType.encode())
        server.send(currentDir.encode())
        response = server.recv(1024).decode()
        
        if( response == 'OK'):
            #If the server has the file
            newFile = open(fileName + '.'+fileType,'wb') 				
            data = server.recv(1024) 						
            while (data): 										
                newFile.write(data) 							
                data = server.recv(1024)
            newFile.close()
            command = ' '
            
        else:
            #If the server can't find the file
            print("Can't find the specified file.\n")
            command = ' '
            
    if(command == 'put'):
    #Mark
        fileExists = 'yes'
        #Check to make sure the local file exists before communicating with the server
        try:
            with open(fileName + '.' + fileType) as file:
                pass
        except IOError as e:
            fileExists = 'no'
        if(fileExists == 'no'):
            print('Can not find the file \n')
            command = ' '
            continue
        server.send(command.encode())
        server.send(fileName.encode())
        server.send(fileType.encode())
        server.send(currentDir.encode())

        file = open (fileName + '.'+fileType, "rb") 	
        data = file.read(1024) 			            
        while (data):					
            server.send(data)			
            data = file.read(1024)
        server.shutdown(socket.SHUT_WR)
        server.close()
        command = ' '
        
    if(command == 'cd'):
        server.send(command.encode())
        server.send(changeDir.encode())
        d2 = server.recv(1024).decode()
        if(d2 != currentDir and d2 != "N_OK"):
            currentDir = d2

        else:
            print("Invalid Path")
        command = ' '
        
    if(command == 'mkdir'):
    #Jeremy
    #check with the server to make sure the path already doesn't exist
    #if it doesn't then make it
    #if it does print directory already exists
        command = ' '
        
    if(command == 'quit'):
        break
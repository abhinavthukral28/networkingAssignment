import socket
import sys

#Function definitions
def formatInput(rawInput):
    "Format the user input into command, fileName, fileType, changeDir, and makeDir"
    if(len(rawInput)<=1):
        return ' ', ' ', ' ', ' ', ' '
        
    if(rawInput[0:2] == 'ls'):
        return 'ls', ' ', ' ', ' ', ' '
        
    if(rawInput[0:3] == 'get' and len(rawInput) >= 5):
        file = rawInput[4:len(rawInput)]
        i = 0;
        while(file[i] != '.'):
            i += 1
        fileName = file[0:i]
        fileType = file[i+1:len(file)]
        return 'get', fileName, fileType, ' ', ' '
    
    if(rawInput[0:3] == 'put' and len(rawInput) >= 5):
        file = rawInput[4:len(rawInput)]
        i = 0;
        while(file[i] != '.'):
            i += 1
        fileName = file[0:i]
        fileType = file[i+1:len(file)]
        return 'put', fileName, fileType, ' ', ' '
        
    if(rawInput[0:2] == 'cd' and len(rawInput) >= 4):
        directory = rawInput[3:len(rawInput)]
        return ' ', ' ', ' ', directory, ' '
        
    if(rawInput[0:5] == 'mkdir' and len(rawInput) >= 7):
        directory = rawInput[6:len(rawInput)]
        print(directory)
        return ' ', ' ', ' ', ' ', directory
        
    else:
        print('Invalid Command\n')
        return ' ', ' ', ' ', ' ', ' '
        
#Variables
currentDir  = ' '           #Keep track of the current directory
rawInput    = ' '           #Unformatted user input
command     = ' '           #Formatted command from the user
fileName    = ' '           #Formatted fileName from the user   
fileType    = ' '           #Formatted fileType from the user
changeDir   = ' '           #Formatted directory the user would like to try and go to
makeDir     = ' '           #Formatted directory the user would like to create

#The server we are connecting to
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("localhost",1234))

while command == ' ':
    rawInput = input("Enter a command:\n")
    command, fileName, fileType, changeDir, makeDir = formatInput(rawInput)

    if(command == 'ls'):
    #Rita
        command = ' '
    
    if(command == 'get'):
    #Mark
        #Send the command, fileName, fileType, and fileLocation to the server
        server.send(command.encode())
        server.send(fileName.encode())
        server.send(fileType.encode())
        server.send(currentDir.encode())
        response = server.recv(1024).decode()
        print(response)
        if( response == 'OK'):
            #If the server has the file
            newFile = open(fileName+'gg.'+fileType,'wb') 				
            data = server.recv(1024) 						
            while (data): 										
                newFile.write(data) 							
                data = server.recv(1024)
            print('line81')
            newFile.close()
            command = ' '
        else:
            #If the server can't find the file
            print("Can't find the specified file.\n")
            command = ' '
    if(command == 'put'):
    #Mark
        command = ' '
        
    if(command == 'cd'):
    #Abhinav
        command = ' '
        
    if(command == 'mkdir'):
    #Jeremy
        command = ' '
        
# networkingAssignment
COMP 3203 Principles of Computer Networks
Fall 2015
Assignment: File transfer system (4 students)

***********************************************************************************************************
Authors: Abhinav Thukral, Mark Roy, Margarita Otochkina, Jeremy Haccoun Finkelstein

***********************************************************************************************************
Objective: To develop a client-server file transfer system in Python using the Socket API. 
The server is started on a specific port number (using TCP) and listens for requests.
The client is started with the IP address and port number of the server. It sends requests to the server.
The server handles the requests and returns replies to the client. The client handles the replies.

************************************************************************************************************
Instructions to run the program sucessfully (must be done in this order):

1. Run the server.py file using Terminal (Linux/Ubuntu) or Power Shell (Windows) window
2. Run the client.py file using a secondary Terminal (Linux/Ubuntu) or Power Shell (Windows) window
3. Type any of the commands listed followed by the proper name if necessary (see details below)

**Note:  Double-clicking server.py and client.py will run the program successfully.  If the 
user wishes, he/she may use the run commands python server.py and python client.py to run the program.

*************************************************************************************************************
The following commands were implemented to satisfy the corresponding requests:

1. ls : prints on the client window a listing of the contents of the current directory
on the server machine.

2. get 'remote-file': retrieves the 'remote-file' on the server and stores it on the
client machine. It is given the same name it has on the server machine.  This will 
only work if the 'remote-file' actually exists on the server.

3. put 'file-name': puts and stores the file from the client machine to the server
machine. On the server, it is given the same name it has on the client machine. This 
will only work if the 'file-name' actually exists on the client machine.

4. cd 'directory-name': changes the directory on the server.  This will only work if the
'directory-name' actually exists (i.e. the path specified is an actual path).

5. mkdir 'directory-name': creates a new sub-directory. You may name the new directory
any name as long as it does not currently exist.

*************************************************************************************************************
The system successfully adheres to the following requirements:

1. It handles files of any type (including binary).
2. It handles errors.
3. It is commented.
4. It can be run on two different machines (client machine & server machine)

**Note:  Since we are using Python, network byte ordering heterogeneity is not an issue.
**************************************************************************************************************

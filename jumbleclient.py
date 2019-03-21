from socket import *
serverName = 'localhost'    #set the server name
serverPort = 12000          #set the port number 
clientSocket = socket(AF_INET, SOCK_STREAM)     #create a TCP socket object
clientSocket.connect((serverName,serverPort))   #connect to the server
while True:
    start =  clientSocket.recv(1024)        #receive the word question from server 
    print(start.decode())                   #decode the received message and print
    userinput = input('Type your answer\n') #user input the answer
    while userinput == '':                  #if the input is empty, let user type the answer again
        userinput = input('invalid input\nPlease type your answer again\n')
    clientSocket.send(userinput.encode())   #send the user input to the server to process
    if userinput == 'Exit':             #if user input is 'Exit", stop the game
        print('Game Stop')
        clientSocket.close()            #close the socket
        break
    else:
        result = clientSocket.recv(1024)    #receive the correctness of user's answer from server
        print(result.decode())              #decode the result and print
clientSocket.close()                    #close the socket

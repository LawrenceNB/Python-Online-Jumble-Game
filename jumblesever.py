from socket import *
import time
import random
import _thread as thread
myPort = 12000                  #set the Port number
F = open('wordlist.txt')        #open the wordlist file
words = F.readlines()           #read the file
F.close()                       #close the file

sockobj = socket(AF_INET, SOCK_STREAM)  #create a TCP socket object
sockobj.bind(('', myPort))              #bind it to the server port number
sockobj.listen(5)                       #allow up to five pending connects
print('Server Start')

def now():
    return time.ctime(time.time())      #current time on the server


def handleClient(connectionSocket,address):
    while True:
        word = words[random.randrange(len(words))]          #pick a word randomly
        while len(word) > 5 or len(word) == 0:              #if the word is too long or empty
            word = words[random.randrange(0, len(words))]   #random pick a word again
        word = word.rstrip()    #remove the trailing spaces
        old_word = word
        word = list(word)       #convert word from string to list
        s = ''                  #initalize string s which will store random orderred characters from the word
        while word:
            s += (word.pop(random.randrange(len(word)))) #let the character add to the string s
            s += ' '                                     #use space to seprate every characters
        connectionSocket.send(s.encode())                #encode the string s and send to the client
        match_word = connectionSocket.recv(1024).decode()#receive the user input from the client
        new_word = match_word + '\n'
        if match_word == 'Exit':            #if user input 'Exit'
            print(address, "exit the game") #print which user has exited
            connectionSocket.close()        #close the socket
            break
        elif new_word in words and set(match_word) == set(old_word):#if user input match the word
            s = 'You win.'                                          #user get correct
            connectionSocket.send(s.encode())                       #encode and send the result message to client 
        else:                                   #else user answer wrong
            s = 'The answer is ' + old_word     #the answer message
            connectionSocket.send(s.encode())   #encode and send the answer message to the client
    connectionSocket.close()                    #close the socket

def dispatcher():                               #listen until process killed
    while True:                                 #wait for next connection
        connection, address = sockobj.accept()  # pass to thread for service
        print('Server connected by' , address, end=' ')
        print('at', now())
        thread.start_new_thread(handleClient,(connection,address)) 

dispatcher()    #call the dispatcher 


    


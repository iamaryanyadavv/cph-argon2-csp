import socket
import json
import argon2
from pyargon2 import hash

import signal
import resource
import os

# checking time limit exceed
def time_exceeded(signo, frame):
    print("Time's up !")
    raise SystemExit(1)
  
def set_max_runtime(seconds, userChoice, username, password):
    # setting up the resource limit
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    
    resource.setrlimit(resource.RLIMIT_CPU, (seconds, hard))
    if(userChoice=='1'):
        can_u = u.lower()
        #reversing username and adding to password as salt
        salt1 = u[::-1]
        salt = salt1+salt1+salt1+salt1+salt1+salt1+salt1+salt1
        hash_p = hash(p,salt)

        clientsocket.send(hash_p.encode()) #6 send
        clientsocket.recv(1024).decode() #7 recv
        clientsocket.send(u.encode()) #8 send
        print(clientsocket.recv(1024).decode()) #9 recv

    elif(userChoice=="2"):
        can_u = u.lower()
        # reversing username and adding to password as salt
        salt1 = u[::-1]
        salt = salt1+salt1+salt1+salt1+salt1+salt1+salt1+salt1
        hash_p = hash(p,salt)

        clientsocket.send(hash_p.encode()) #6 send
        clientsocket.recv(1024).decode() #7 recv
        clientsocket.send(u.encode()) #8 send
        print(clientsocket.recv(1024).decode()) #9 recv

    signal.signal(signal.SIGXCPU, time_exceeded)


# we are not using domain name to calculate salt because that is not possible with sockets
#I am using a random salt rn but we have to figure what to do with the salt

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = '127.0.0.1'
PORT = 5545

clientsocket.connect( (IP, PORT))

print(clientsocket.recv(1024).decode()) #1 recv
clientsocket.send('OK'.encode()) #2 send

user_choice = input("Please enter 1 to register and 2 to login\n")
clientsocket.recv(1024).decode()  # 3 recieve
clientsocket.send(user_choice.encode()) #4 send
clientsocket.recv(1024).decode()  # 5 recieve

#Registration
if user_choice == "1":
    u = input("Please enter a username \n")
    p = input("Please enter a password\n")
    set_max_runtime(2, "1", u, p)
    

#Login
if user_choice == "2":
    u = input("Please enter a username \n")
    p = input("Please enter a password\n")
    set_max_runtime(2, "2", u, p)
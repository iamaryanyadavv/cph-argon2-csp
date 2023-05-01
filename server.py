import socket
import json
import hashlib
import sqlite3

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = '127.0.0.1'
PORT = 5545

serversocket.bind( (IP, PORT))

serversocket.listen()

print('The server is up! Listening at', IP, PORT)
print()

# connection=sqlite3.connect('users.db')
# c = connection.cursor()

# c.execute("DELETE FROM users")
# print(c.fetchall())

# connection.commit()
# connection.close()

def handle_new_client(clientsocket, address):

    connection = sqlite3.connect('users.db')
    c = connection.cursor()

    print("New connection made! Client address:", address)
    intro = 'Welcome to a demo of client side hashing\n'

    clientsocket.send(intro.encode()) #1 send
    if clientsocket.recv(1024).decode() != 'OK':#2 recieve
        print('Something went wrong! Disconnecting')
        clientsocket.close()

    clientsocket.send("Waiting for hashed password........".encode())#3 send
    user_choice = clientsocket.recv(1024).decode() #4 recieve
    clientsocket.send("OK".encode())  #5 send
    
    if user_choice == "1":
        hash = clientsocket.recv(1024).decode() #6 recieve
        clientsocket.send('Password recvd'.encode()) #7 send
        username = clientsocket.recv(1024).decode() #8 recv

        byte_input = hash.encode()
        hash_object = hashlib.sha256(byte_input)
        hashed_password = hash_object.hexdigest()

        c.execute("""INSERT INTO users VALUES (?,?)""", (username, hashed_password))

        connection.commit()

        c.execute("SELECT * FROM users")
        print(c.fetchall())

        connection.commit()
        clientsocket.send('Registered Successfully!'.encode()) #9 send

        connection.close()

    #we have to store this hash to compare

    if user_choice == "2":
        hash = clientsocket.recv(1024).decode() #6 recieve
        clientsocket.send('Password recvd'.encode()) #7 send
        username = clientsocket.recv(1024).decode() #8 recv

        byte_input = hash.encode()
        hash_object = hashlib.sha256(byte_input)
        hashed_password = hash_object.hexdigest()

        c.execute("SELECT * FROM users WHERE username=?",(username,))
        user_row = c.fetchall()
        if user_row[0][1]==hashed_password:
            clientsocket.send('Logged in Successfully!'.encode()) #9 send
        else:
            clientsocket.send('Incorrect password. Login Failed!'.encode()) #9 send

        #compare using a dict
        #if comparison is true then login agreed

while True:
    (clientsocket, address) = serversocket.accept()
    handle_new_client(clientsocket, address)
    clientsocket.close()


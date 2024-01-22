from socket import *
import threading

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

#dictionary containing username string to client_socket mapping
client_sockets = {}

def client_manager(client_name):
    '''
    receives the message and sends the message to one of the users
    if no user is found then sends the error message to the sender
    '''
    while True:
        try:
            message = client_sockets[client_name].recv(4096).decode()
        except:
            print(f"Client socket of {client_name} closed")
            del client_sockets[client_name]
            return
        #find the sender and receiver
        i1 = message.find(' ')
        if (i1 == -1):
            print(message)
            continue
        To = message[:i1][:]
        print (f'message from {client_name} to {To}')
        message = client_name + ' - '+ message[i1+1:]
        if (To == 'info'):
            print('info')
            print(message)
        elif (To == 'error'):
            print('error')
            print(message)
        elif (To not in client_sockets):
            print('To not found')
            print(message)
        else:
            client_sockets[To].send(message.encode())


while True:
    connectionSocket, addr = serverSocket.accept()
    if (len(client_sockets) == 0):
        connectionSocket.send(" ".encode())
    else:
        connectionSocket.send( (" ".join(client_sockets.keys())).encode() )
    username = ""
    while username=="":
        username = connectionSocket.recv(1024).decode()
        if (username in client_sockets):
            connectionSocket.send(f'Username {username} already used closing the session'.encode())
            username = ""

    print(f'Registering new user {username}')
    client_sockets[username] = connectionSocket
    cm = threading.Thread(target = client_manager, args=(username,))
    cm.start()
    for user in client_sockets:
        if (user != username):
            client_sockets[user].send(f'info new user {username} entered the chat app'.encode())
from socket import *
import threading

INPUT_PROMPT_LENGTH = len('input message: ')
SERVER_NAME = '192.168.140.136'
SERVER_PORT = 12000
CLIENT_SOCKET = socket(AF_INET, SOCK_STREAM)
CLIENT_SOCKET.connect((SERVER_NAME,SERVER_PORT))

print(
    '''
    This is a chat app based on TCP
    Usage - 
    First enter a username to identify yourself
    username is a single word
    example - siddhu/arup/gautam
    prohibited usernames - info, error

    After entering the username you can send messages to others users
    connected to the server.
    To send a message type username message.
    note - message length is limited to 4096 bytes
    Example: to send a message to gautam
             gautam how are you?

    To close the program type exit
    '''
)
cur_users = CLIENT_SOCKET.recv(4096).decode().split()
print(f"Currently there {len(cur_users)} users")
if (len(cur_users)>0):
    print(f"User names - {cur_users}")

username = input('Input your username: ')
CLIENT_SOCKET.send(username.encode())
exit = False
def sender():
    '''
    This function is used to send the messages to the server
    '''
    global exit
    
    while True:
        message = input("input message: ")
        if (message == 'exit'):
            exit = True
            return
        try:
            CLIENT_SOCKET.send(message.encode())
        except Exception as e:
            print("Could not send the message :(")
            print(e)
            exit = True
            return


def receiver():
    global exit
    while True:
        try:
            recieved_message = CLIENT_SOCKET.recv(4096)
            recieved_message = recieved_message.decode()
        except:
            return
        if (exit):
            return
        print('\r')
        print(recieved_message, end='')
        print(' '*INPUT_PROMPT_LENGTH)
        print("input message: ", end='', flush=True)

rx = threading.Thread(target = receiver, args = ())
rx.start()
sender()

CLIENT_SOCKET.close()
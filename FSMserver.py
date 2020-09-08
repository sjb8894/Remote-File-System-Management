# FSM Server Program
import socket
import os
from subprocess import Popen, PIPE

port = 9999

# creates server socket
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# binds server socket to host and port number
server_sock.bind(('', port))

# readies server socket to accept client connection, sets to listening mode
server_sock.listen(5)

# Accepts msg from client-side, blocking
(client_sock, addr) = server_sock.accept()

while True:

    # receives client msg
    msg_from_client = client_sock.recv(4096).decode()

    # splits user input into list to check for cmd keyword
    parseMsg = msg_from_client.split()
    print(parseMsg)
    print("Server is listening..")

    # for x in parseMsg:
    if parseMsg[0] == "pwd":
        msg_from_client = os.getcwd()
        client_sock.send(msg_from_client.encode())

    elif parseMsg[0] == "ls":
        msg_from_client = os.listdir(os.getcwd())
        separator = ' '
        msg_from_client = separator.join(msg_from_client)
        client_sock.send(msg_from_client.encode())

    elif parseMsg[0] == "mkdir":

        if os.path.isdir(parseMsg[1]):
            client_sock.send(f"Directory {parseMsg[1]} already exists".encode())
        else:
            pipe = Popen(f"mkdir {parseMsg[1]} ", shell=True, stdout=PIPE).stdout
            client_sock.send(f"Directory {parseMsg[1]} created ".encode())

    elif parseMsg[0] == "write":
        f = open(parseMsg[1], "w+")
        for i in parseMsg[2:]:
            f.write(i + "\n")
        f.close()
        msg_from_client = "File created"
        client_sock.send(msg_from_client.encode())

    elif parseMsg[0] == "run":
        pipe = Popen(f"run {parseMsg[1]} ", shell=True, stdout=PIPE).stdout
        output = pipe.read()
        client_sock.send(output)

    elif parseMsg[0] == "cat":
        pipe = Popen(f"cat {parseMsg[1]} ", shell=True, stdout=PIPE).stdout
        output = pipe.read()
        client_sock.send(output)

    elif parseMsg[0] == "cd":
        if os.path.isdir(parseMsg[1]):
            os.chdir(parseMsg[1])
            client_sock.send(f"Directory changed to {parseMsg[1]}".encode())
        else:
            msg_from_client = "Invalid directory, please try again"
            client_sock.send(msg_from_client.encode())

    elif parseMsg[0] == "quit":
        break

    else:
        msg_from_client = "Command unable to be executed, please try again"
        client_sock.send(msg_from_client.encode())

client_sock.close()

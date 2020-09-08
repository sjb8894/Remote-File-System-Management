#FSM Client Program
import socket

host = 'localhost'
port = 9999

#creates socket
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connects socket to FSMserver
client_sock.connect((host, port))



while True:

    client_msg = input("Enter a command (pwd, cd, ls, mkdir, write, cat, run, quit): ")

    #handles case for client wanting to use write cmd
    if client_msg.split()[0] == "write":
        while True:
            x = input(">")
            client_msg = client_msg + "\n" + x
            if x is "":
                break

    client_sock.send(client_msg.encode())


    #quits program if quit msg displayed
    if client_msg == 'quit':
        msg_from_server = client_sock.recv(4096)
        break

    msg_from_server = client_sock.recv(4096)
    print(msg_from_server.decode())



#closes client side socket
client_sock.close()


import socket
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 40000  # the port used by the server to listen on

clients = []  # list for the clients
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:  # IPv4 argument, and UDP argument.  UDP/IP socket creation
    # attaching port number to host for socket. associate the socket with network interface and port number used for reaching the host.
    s.bind((HOST,
            PORT))  # attaching port number to host for socket. associate the socket with network interface and port number used for reaching the host.
    s.setblocking(0)  # it will not block, it will grab data from the stream.
    quitting = False
    print("Welcome to the Server!!")
    while not quitting:  # infinite while loop used to loop over blocking calls to conn.recv().
        try:  # we use try except  to throw an error if there's no data to receive.
            data, clientAddr = s.recvfrom(
                1024)  # 1KB of maximum buffer size for the data that is going to be received. we try and grab data and the address.
            if "Quit" in str(
                    data):  # if the string Quit is on a message(data), the client who send the data will quit from the server
                quitting = True
            if clientAddr not in clients:  # this condition will add the client address if is not already on the clients list created before.
                clients.append(clientAddr)
            print(time.ctime(time.time()) + str(clientAddr) + ": :" + str(
                data))  # this print function will print a timestamp on when that client is connecting.
            for client in clients:  # for loop to send the messages to all the clients currently in the chat.
                s.sendto(data, client)
        except:
            pass  # pass and try again if there's nothing on the stream left to receive or grab.
    s.close  # close the socket once we quit.

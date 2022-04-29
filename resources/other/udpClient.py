import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 50000  # port for the clients.

server = ('127.0.0.1', 40000)  # server IP and Port.

tLock = threading.Lock()  # we create a Lock for the thread to stop the application from trying to get output to the screen simultaneously.
shutdown = False  # this variable is going to be used to tell the thread to shut down.


def receiving(name, sock):  # receiving function will take a name for the thread and a socket.
    while not shutdown:  # while the application stills running, we are going to try and acquire the thread lock.
        try:
            tLock.acquire()
            while True:  # infinte loop to grab and print all the data that came in.
                data, addr = sock.recvfrom(1024)  # grab data and address from socket.
                print(str(data))
        except:
            pass  # pass and try again if there's nothing on the stream to receive.
        finally:  # release the thread lock once there's no more data to receive.
            tLock.release()


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST,
            PORT))  # attaching to socket to host IP and port. attaching port number to host for socket. associate the socket with network interface and port number used for reaching the host.
    s.setblocking(0)  # it will not block, it will grab data from the stream.

    rT = threading.Thread(target=receiving, args=(
    "RecvThread", s))  # creating our receiving thread . we'll call it receive thread and pass it the socket.
    rT.start()  # will start trying to receive messages from the Server.

    nickname = input("Name: ")  # Setting up an alias or nickname for the User for sending messages.
    message = input(nickname + "-> ")  # message user want to send.
    while message != 'q':  # infinite loop until client send 'q' message to quit from the server.
        if message != '':  # if message not equal empty, we're going to try to send it.
            s.sendto(nickname + ": " + message, server)  # send message with the nickname, the message and send it to the server.
        tLock.acquire()  # acquire the lock to try and get a new message.
        message = input(nickname + "-> ")
        tLock.release()  # we release the lock
        time.sleep(0.2)  # we set a sleep time before sending a new message.
        # now we can send messages to the server and receive messages as the thread will handle it.
    shutdown = True  # if the client choose to quit('q'), we're going to shut down from the server.
    rT.join()  # waiting for the thread. once it shut down, we can close the socket.
    s.close()

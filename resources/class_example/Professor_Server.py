#UDP Server from professor
from socket import *
serverPort = 55000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('localhost', serverPort))
print("\nThe UDP server has started and its ready to recieve\n")
while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    print(f"\tMessage {message.decode('utf-8')!r} has been received from UDP client...")
    modifiedMessage = message .upper()
    print(f"\tSending modified message {modifiedMessage.decode('utf-8')!r} to UDP client...")
    serverSocket.sendto(modifiedMessage, clientAddress)
    print("\tThe UDP server is ready to receive\n")
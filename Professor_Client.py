#UDP Client from the professor
from socket import *
serverName = "localhost"
serverPort = 55000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Input lowercase sentence: ')
print(f"\nSending message {message!r} to server...\n")
clientSocket.sendto(message.encode('utf-8'),(serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print("Printing reply from UDP server...\n\t")
print(f"\t{modifiedMessage.decode('utf-8')!s}")
print("\nClosing client UDP socket...\n")
clientSocket.close()
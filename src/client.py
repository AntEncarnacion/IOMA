import socket
import sys
import threading

class Client:
    def __init__(self):
        self.peer_port=50000
        self.server_port=40000


        self.message_list = []
        
        # Server ip and port (40000)
        self.server_ip='172.26.36.73'
        self.rendezvous = (self.server_ip, self.server_port)

        # Create a socket and bind it to '0.0.0.0.' and server port
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_sock.bind(('0.0.0.0', self.server_port))
        
        # Create a socket and bind it to '0.0.0.0.' and peer port
        self.peer_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.peer_sock.bind(('0.0.0.0', self.peer_port))

        # Function to get local ip address 
        hostname = socket.gethostname()
        self.local_ip = socket.gethostbyname(hostname)
        
        # Connect to the server and receive list of client in format of data string
        self.data_list_of_peer=self.connect_to_server()

        # Convert data_list_of_peer to a list of tuple peer_list
        self.peers_list=self.convertstr_into_tuple(self.data_list_of_peer)

        # Print the Peers
        # print_peer(peers_list)
        
        # Create thread so that the port can listen for server
        self.listener_server = threading.Thread(target=lambda: self.listen_server(), daemon=True);
        self.listener_server.start()
        
        # Create thread so that the port can listen for peer
        self.listener = threading.Thread(target=lambda: self.listen_peer(), daemon=True);
        self.listener.start()

    # Function to get local ip address
    def getlocal_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        local_ip=s.getsockname()[0]
        s.close()
        return local_ip

    # Connect to the server and receive list of client in format of data string  
    def connect_to_server(self):
        self.username = input('Enter username: ')
        print('connecting to rendezvous server')
        message = f'join|{self.username}'
        self.server_sock.sendto(message.encode(), self.rendezvous)
        while True:
            data = self.server_sock.recv(1024).decode()

            if data.strip() == 'ready':
                print('checked in with server, waiting')
                break

        data = self.server_sock.recv(1024).decode()
        return data
    
    # listen for peer socket
    def listen_peer(self):
        while True:
            data, address = self.peer_sock.recvfrom(1024)
            print(address[0])
            print(self.local_ip)
            if address[0] != self.local_ip:
                for client in self.peers_list:
                    if client[0] == address[0]:
                        user = client[1]
                        break
                self.message_list.append('{} {}'.format(user,data.decode()))

    # listen for server socket
    def listen_server(self):
        while True:
            data = self.server_sock.recv(1024).decode()
            self.peers_list.clear()
            self.peers_list.extend(self.convertstr_into_tuple(data))
            
    # send messages
    def send_message(self, msg):
        self.message_list.append(msg)

        for client in self.peers_list:
            if client[0] != self.local_ip:
                response = self.peer_sock.sendto(msg.encode(), (client[0], self.peer_port))
            while response != msg:
                response = self.peer_sock.sendto(msg.encode(), (client[0], self.peer_port))

    def client_leave(self):
        print('connecting to rendezvous server')
        message = f'leave|'
        self.server_sock.sendto(message.encode(), self.rendezvous)

    def convertstr_into_tuple(self, data):
        decoded_string = data
        li = list(decoded_string.split(" "))
        b=0
        c=0
        new_list= []
        for val in li:
            if b == 0:
                new_list.append(list())
                new_list[c].append(val) 
                b+=1
            else:
                new_list[c].append(val)
                b=0
                c+=1
        newnew_list=[]        

        for val in new_list:
            newnew_list.append(tuple(val))
        return newnew_list   

    # if __name__ == '__main__':
    #     main_client()   
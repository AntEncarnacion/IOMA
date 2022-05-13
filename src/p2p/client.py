import socket
import sys
import threading
peer_port=50000
server_port=40000

def main_client():
    # Function to get local ip address 
    local_ip=getlocal_ip()
    
    # Server ip and port (40000)
    server_ip='172.24.84.82'
    rendezvous = (server_ip, server_port)

    # Create a socket and bind it to '0.0.0.0.' and server port
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind(('0.0.0.0', server_port))
    
    # Create a socket and bind it to '0.0.0.0.' and peer port
    peer_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    peer_sock.bind(('0.0.0.0', peer_port))
    
    # Connect to the server and receive list of client in format of data string
    data_list_of_peer=connect_to_server(server_sock,rendezvous)

    # Convert data_list_of_peer to a list of tupple peer_list
    peers_list=convertstr_into_tupple(data_list_of_peer)

    # Print the Peers
    print_peer(peers_list)
    
    # Create thread so that the port can listen for server
    listener_server = threading.Thread(target=lambda :listen_server(peers_list,server_sock), daemon=True);
    listener_server.start()
    
    # Create thread so that the port can listen for peer
    listener = threading.Thread(target=lambda :listen_peer(peer_sock,peers_list), daemon=True);
    listener.start()

    # exit_flag = False
    while True:
        msg = input('> ')

        if(msg == 'exit'):
            client_leave(rendezvous,server_sock) # Leave the chat
            break
        else:
            send_message(peer_sock,msg,peers_list,local_ip) # Send message to other peers
    
def getlocal_ip():
    # Function to get local ip address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    local_ip=s.getsockname()[0]
    s.close()
    return local_ip

# Connect to the server and receive list of client in format of data string  
def connect_to_server(server_sock,rendezvous):
    username = input('Enter username: ')
    print('connecting to rendezvous server')
    message = f'join|{username}'
    server_sock.sendto(message.encode(), rendezvous)
    while True:
        data = server_sock.recv(1024).decode()

        if data.strip() == 'ready':
            print('checked in with server, waiting')
            break

    data = server_sock.recv(1024).decode()
    return data
   
def listen_peer(peer_sock,peers_list):
    # listen for peer socket
    while True:
        data, address = peer_sock.recv(1024)
        for client in peers_list:
                if client[0] == address[0]:
                    print('\r{} {}\n> '.format(client[1],data.decode()), end='') 

def listen_server(peers_list,server_sock):
    # listen for server socket
    while True:
        data = server_sock.recv(1024).decode()
        peers_list.clear()
        peers_list.extend(convertstr_into_tupple(data))
        

def send_message(peer_sock,msg,peers_list,local_ip):
    # send messages
    for client in peers_list:
        if client[0] != local_ip:
            peer_sock.sendto(msg.encode(), (client[0], peer_port))

def client_leave(rendezvous,server_sock):
    print('connecting to rendezvous server')
    message = f'leave|'
    server_sock.sendto(message.encode(), rendezvous)

# def print_ip_of_client(peers_list):
#     for client in peers_list:
#         return client[0]        
    
def print_peer(peers_list):
    # Print peer list    
        for client in peers_list:
            print('\ngot peer')
            print('  ip:          {}'.format(client[0]))
            print('  username:          {}'.format(client[1]))


def convertstr_into_tupple(data):
    # convert data string into a list of tupple
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

if __name__ == '__main__':
    main_client()   
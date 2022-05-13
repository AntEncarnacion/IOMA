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

    #Punch hole
    punch_hole(peer_sock,peers_list)
    
    # Create thread so that the port can listen for server
    listener_server = threading.Thread(target=lambda :listen_server(peers_list,server_sock), daemon=True);
    listener_server.start()
    
    # Create thread so that the port can listen for peer
    listener = threading.Thread(target=lambda :listen_peer(peer_sock), daemon=True);
    listener.start()

    exit_flag = False
    while True:
        msg = input('> ')
        if(exit_flag):
            client_leave(rendezvous,server_sock) # Leave the chat
            break
        send_message(peer_sock,msg,peers_list,local_ip) # Send message to other peers
    
def getlocal_ip():
    # Function to get local ip address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    local_ip=s.getsockname()[0]
    s.close()
    return local_ip

def connect_to_server(server_sock,rendezvous):
    # Connect to the server and receive list of client in format of data string  
    print('connecting to rendezvous server')
    server_sock.sendto(b'join', rendezvous)
    while True:
        data = server_sock.recv(1024).decode()

        if data.strip() == 'ready':
            print('checked in with server, waiting')
            break

    data = server_sock.recv(1024).decode()
    return data
   
def listen_peer(peer_sock):
    # listen for peer socket
    while True:
        data = peer_sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='') 

def listen_server(peers_list,server_sock):
    # listen for server socket

    while True:
        data = server_sock.recv(1024).decode()
        peers_list=convertstr_into_tupple(data)
        

def punch_hole(peer_sock,peers_list):
    # punch hole
    print('punching hole')
    for client in peers_list:
        peer_sock.sendto(b'0', (client[0], peer_port))
    print('ready to exchange messages\n')    

def send_message(peer_sock,msg,peers_list,local_ip):
    # send messages
    for client in peers_list:
        if client[0] != local_ip:
            peer_sock.sendto(msg.encode(), (client[0], peer_port))

def client_leave(rendezvous,server_sock):

    print('connecting to rendezvous server')
    server_sock.sendto(b'leave', rendezvous)

# def print_ip_of_client(peers_list):
#     for client in peers_list:
#         return client[0]        
    
def print_peer(peers_list):
    # Print peer list    
        for client in peers_list:
            print('\ngot peer')
            print('  ip:          {}'.format(client[0]))
            print('  source port: {}'.format(client[1]))
            print('  dest port:   {}\n'.format(40000))

def convertstr_into_tupple(data):
   
    # convert data string into a list of tupple
    decoded_string = data
    li = list(decoded_string.split(" "))
    b=0
    c=0
    new_list= []
    for i,val in enumerate(li):

        if b == 0:
            new_list.append(list())
            new_list[c].append(val) 
            b+=1
        #elif b == 1:
        #    newnew_list[c].append(int(val))
        #    b+=1
        else:
            new_list[c].append(int(val))
            b=0
            c+=1
    newnew_list=[]        

    for val in new_list:
        newnew_list.append(tuple(val))
    return newnew_list   

if __name__ == '__main__':
    main_client()   
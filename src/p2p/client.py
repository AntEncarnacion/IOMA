import socket
import sys
import threading
peer_port=50000
server_port=40000

def main_client():
    local_ip=getlocal_ip()
    
    server_ip='172.24.84.82'
    rendezvous = (server_ip, server_port)

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind(('0.0.0.0', server_port))
    
    peer_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    peer_sock.bind(('0.0.0.0', peer_port))
    
    
    data_list_of_peer=connect_to_server(server_sock,rendezvous)    
    peers_list=convertstr_into_tupple(data_list_of_peer)
    print_peer(peers_list)
    punch_hole(peer_sock,peers_list)
    listener_server = threading.Thread(target=lambda :listen_server(peers_list,server_sock), daemon=True);
    listener_server.start()
    listener = threading.Thread(target=lambda :listen_peer(peer_sock), daemon=True);
    listener.start()

    exit_flag = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', server_port))
    while True:
        msg = input('> ')
        if(exit_flag):
            client_leave(rendezvous,server_sock)
            break
        send_message(peer_sock,msg,peers_list,local_ip)
    
def getlocal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    local_ip=s.getsockname()[0]
    s.close()
    return local_ip

def connect_to_server(server_sock,rendezvous):
      
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
    # listen for
    while True:
        data = peer_sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='') 

def listen_server(peers_list,server_sock):
    # listen for

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
        
        for client in peers_list:
            print('\ngot peer')
            print('  ip:          {}'.format(client[0]))
            print('  source port: {}'.format(client[1]))
            print('  dest port:   {}\n'.format(40000))

def convertstr_into_tupple(data):

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
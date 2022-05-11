import socket
import sys
import threading
peer_port=50000
server_port=40000

def main_client():
    local_ip=getlocal_ip()
    
    server_ip='172.29.95.223'

    
    data_list_of_peer=connect_to_server(server_ip,peer_port,server_port)    
    tuple_data=convertstr_into_tupple(data_list_of_peer)
    print_peer(tuple_data)
    punch_hole(server_port,peer_port,tuple_data)
    listener_server = threading.Thread(target=lambda tuple_data:listen_server(tuple_data), daemon=True);
    listener_server.start()
    listener = threading.Thread(target=listen_peer, daemon=True);
    listener.start()

    exit_flag = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', server_port))
    while True:
        msg = input('> ')
        if(exit_flag):
            client_leave()
            break
        send_message(server_port,tuple_data,local_ip)
    
def getlocal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    local_ip=s.getsockname()[0]
    s.close()
    return local_ip

def connect_to_server(server_ip,peer_port,server_port):

        rendezvous = (server_ip, server_port)
    
        # 10.0.0.124 192.168.0.2
        # connect to rendezvous
        print('connecting to rendezvous server')

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', peer_port))
        sock.sendto(b'join', rendezvous)

        while True:
            data = sock.recv(1024).decode()

            if data.strip() == 'ready':
                print('checked in with server, waiting')
                break

        data = sock.recv(1024).decode()
        return data
   
def listen_peer():
    # listen for
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', peer_port))

    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='') 

def listen_server(tuple_data):
    # listen for
    #lambda
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', server_port))

    while True:
        data = sock.recv(1024).decode()
        tuple_data=convertstr_into_tupple(data)
        

def punch_hole(server_port,peer_port,tuple_data):
    # punch hole
    print('punching hole')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', peer_port))
    for client in tuple_data:
        sock.sendto(b'0', (client[0], server_port))

    print('ready to exchange messages\n')    

def send_message(server_port,tuple_data,local_ip):
    

    # send messages
    for client in tuple_data:
        if client[0] != local_ip:
            sock.sendto(msg.encode(), (client[0], peer_port))

def client_leave(server_ip, server_port):
    rendezvous = (server_ip, server_port)

    # 10.0.0.124 192.168.0.2
    # connect to rendezvous
    print('connecting to rendezvous server')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', peer_port))
    sock.sendto(b'leave', rendezvous)

# def print_ip_of_client(tuple_data):
#     for client in tuple_data:
#         return client[0]        
    
def print_peer(tuple_data):
        
        for client in tuple_data:
            print('\ngot peer')
            print('  ip:          {}'.format(client[0]))
            print('  source port: {}'.format(client[1]))
            print('  dest port:   {}\n'.format(40000))

def convertstr_into_tupple(data):

    decoded_string = data
    li = list(decoded_string.split(" "))
    b=0
    c=0
    newnew_list= []
    for i,val in enumerate(li):

        if b == 0:
            newnew_list.append(list())
            newnew_list[c].append(val) 
            b+=1
        #elif b == 1:
        #    newnew_list[c].append(int(val))
        #    b+=1
        else:
            newnew_list[c].append(int(val))
            b=0
            c+=1
    newnewnew_list=[]        

    for val in newnew_list:
        newnewnew_list.append(tuple(val))
    return newnewnew_list   

if __name__ == '__main__':
    main_client()   
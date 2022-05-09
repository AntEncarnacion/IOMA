import socket
import sys
import threading

def main_client():
    local_ip=getlocal_ip()
    sport=50000
    dport=40000
    server_ip='172.29.95.223'

    
    data_list_of_peer=connect_to_server(server_ip,sport,dport)    
    tuple_data=convertstr_into_tupple(data_list_of_peer)
    print_peer(tuple_data)
    punch_hole(dport,sport,tuple_data)
    listener = threading.Thread(target=listen, daemon=True);
    listener.start()
    send_message(dport,tuple_data)

    

    
def getlocal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    local_ip=s.getsockname()[0]
    s.close()
    return local_ip
def connect_to_server(server_ip,sport,dport):

        rendezvous = (server_ip, dport)
    
    # 10.0.0.124 192.168.0.2
    # connect to rendezvous
        print('connecting to rendezvous server')

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', sport))
        sock.sendto(b'0', rendezvous)

        while True:
            data = sock.recv(1024).decode()

            if data.strip() == 'ready':
                print('checked in with server, waiting')
                break

        data = sock.recv(1024).decode()
        return data

    
    
def listen():
    # listen for
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', sport))

    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')

def punch_hole(dport,sport,tuple_data):
        # punch hole
        print('punching hole')

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', sport))
        for client in tuple_data:
            sock.sendto(b'0', (client[0], dport))

        print('ready to exchange messages\n')    

def send_message(dport,tuple_data):
    # send messages
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', dport))

        while True:
            msg = input('> ')
            for client in tuple_data:
                if client[0] != local_ip:
                    sock.sendto(msg.encode(), (client[0], sport))

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

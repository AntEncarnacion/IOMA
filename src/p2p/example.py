import socket
import sys
import threading

def main_client():

    rendezvous = ('10.0.0.124', 40000)
    sport=50000
    dport=40000
    # 10.0.0.124 192.168.0.2
    # connect to rendezvous
    print('connecting to rendezvous server')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 50000))
    sock.sendto(b'0', rendezvous)

    while True:
        data = sock.recv(1024).decode()

        if data.strip() == 'ready':
            print('checked in with server, waiting')
            break

    data = sock.recv(1024).decode()
    tuple_data=convertstr_into_tupple(data)
    print_peer(tuple_data)
    

    # ip, sport, dport = data.split(' ')
    # sport = int(sport)
    # dport = int(dport)

    # print('\ngot peer')
    # print('  ip:          {}'.format(ip))
    # print('  source port: {}'.format(sport))
    # print('  dest port:   {}\n'.format(dport))

    # punch hole
    print('punching hole')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', sport))
    for client in tuple_data:
        sock.sendto(b'0', (client[0], dport))

    print('ready to exchange messages\n')

    # listen for
    def listen():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', sport))

        while True:
            data = sock.recv(1024)
            print('\rpeer: {}\n> '.format(data.decode()), end='')

    listener = threading.Thread(target=listen, daemon=True);
    listener.start()

    # send messages
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', dport))

    while True:
        msg = input('> ')
        for client in tuple_data:
            sock.sendto(msg.encode(), (client[0], sport))

# def print_ip_of_client(tuple_data):
#     for client in tuple_data:
#         return client[0]        
    
def print_peer(tuple_data):
        
        for client in tuple_data:
            print('\ngot peer')
            print('  ip:          {}'.format(client[0]))
            print('  source port: {}'.format(client[1]))
            print('  dest port:   {}\n'.format(client[0]))

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
        elif b == 1:
            newnew_list[c].append(int(val))
            b+=1
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

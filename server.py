import socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 40000))

    while True:
        clients = []

        while True:
            data, address = sock.recvfrom(128)

            client_join(clients, address, sock)
            if len(clients) == 2:
                print('got 2 clients, sending details to each')
                client_send_info(clients, sock)
                break

        client_exit(clients, 0)
        client_exit(clients, 1)

def client_join(clients, address, sock):
    print('connection from: {}'.format(address))
    clients.append(address)
    sock.sendto(b'ready', address)
    client_send_info(clients, sock)

def client_exit(clients, index, sock):
    clients.pop(index)
    client_send_info(clients, sock)

def client_send_info(clients, sock):
    # scalable future implementation
    # for client in clients:
    #     encoded_list = bytes(clients)
    #     sock.sendto(encoded_list, client)
    sock.sendto('{} {} {}'.format(clients[0], clients[0], 40000).encode(), clients[1])
    sock.sendto('{} {} {}'.format(clients[1], clients[1], 40000).encode(), clients[0])

if __name__ == '__main__':
    main()
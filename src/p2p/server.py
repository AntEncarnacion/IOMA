import socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 40000))

    while True:
        clients = []

        while True:
            data, address = sock.recvfrom(128)

            clients = client_join(clients, address, sock)
            if len(clients) == 2:
                print('got 2 clients, sending details to each')
                break

        client_send_info(clients, sock)
        clients = client_exit(clients, 0, sock)
        clients = client_exit(clients, 0, sock)

def client_join(clients, address, sock):
    print('connection from: {}'.format(address))
    clients.append(address)
    sock.sendto(b'ready', address)
    # client_send_info(clients, sock)

    return clients

def client_exit(clients, index, sock):
    clients.pop(index)
    # client_send_info(clients, sock)

    return clients

def client_send_info(clients, sock):
    # scalable future implementation
    # encoded_list = format_clients_to_string(clients).encode()
    # for client in clients:
    #     sock.sendto(encoded_list, client)
    sock.sendto('{} {} {}'.format(clients[0][0], clients[0][1], 40000).encode(), clients[1])
    sock.sendto('{} {} {}'.format(clients[1][0], clients[1][1], 40000).encode(), clients[0])

def format_clients_to_string(clients):
    formatted_list = ''
    for client in clients:
        for data in client:
            formatted_list += str(data) + ' '
    return formatted_list[:-1]

if __name__ == '__main__':
    main()
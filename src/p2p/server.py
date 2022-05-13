import socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 40000))

    clients = []

    while True:
        data, address = sock.recvfrom(128)

        if(data.decode() == 'join'):
            clients = client_join(clients, address, sock)
        elif(data.decode() == 'leave'):
            clients = client_exit(clients, address, sock)

def client_join(clients, address, sock):
    print(f'connection from: {address}')
    clients.append((address[0], 40000))

    sock.sendto(b'ready', address)
    client_send_info(clients, sock)

    return clients

def client_exit(clients, index, sock):
    clients.pop(index)
    client_send_info(clients, sock)

    return clients

def client_send_info(clients, sock):
    encoded_list = format_clients_to_string(clients).encode()
    for client in clients:
        sock.sendto(encoded_list, client)

def format_clients_to_string(clients):
    formatted_list = ''
    for client in clients:
        for data in client:
            formatted_list += str(data) + ' '
    return formatted_list[:-1]

if __name__ == '__main__':
    main()
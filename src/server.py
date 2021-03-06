import socket

# Main execution
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 40000))

    clients = []

    # Main execution loop that listens for peer messages
    while True:
        data, address = sock.recvfrom(128)
        data = data.decode().split('|')

        if 'join' == data[0]:
            clients = client_join(data, clients, address, sock)
        elif 'leave' == data[0]:
            for index, client in enumerate(clients):
                if client[0] == address[0]:
                    clients = client_exit(index, clients, sock)
                    break

# Client join method. Adds the new peer to the peer list and broadcasts the updated list.
def client_join(data, clients, address, sock):
    clients.append((address[0], data[1]))
    sock.sendto(b'ready', address)
    client_send_info(clients, sock)
    return clients

# Client exit method. Removes the peer from the peer list and broadcasts the updated list.
def client_exit(index, clients, sock):
    clients.pop(index)
    client_send_info(clients, sock)
    return clients

# Client broadcast method. Broadcasts the new list to all of the peers within it.
def client_send_info(clients, sock):
    encoded_list = format_clients_to_string(clients).encode()
    for client in clients:
        sock.sendto(encoded_list, (client[0], 40000))
    return

# Format method. This method turns the list from a list of tuples to a one dimensional list in the form of a string.
def format_clients_to_string(clients):
    formatted_list = ''
    for client in clients:
        for data in client:
            formatted_list += str(data) + ' '
    return formatted_list[:-1]

if __name__ == '__main__':
    main()
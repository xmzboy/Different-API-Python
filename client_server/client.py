import socket


def client():
    host = socket.gethostname()
    port = 5000
    sock = socket.socket()
    sock.connect((host, port))
    message = input(' -> ')
    while message.lower().strip() != 'bye':
        sock.send(message.encode())
        data = sock.recv(1024).decode()
        print(f'Received from server: {str(data)}')
        message = input(' -> ')
    sock.close()


if __name__ == '__main__':
    client()

import socket


def server():
    host = socket.gethostname()
    port = 5000
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(2)
    conn, addr = sock.accept()
    print(f'Connected from : {str(addr)}')
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f"from connected user: {str(data)}")
        data = input(' -> ')
        conn.send(data.encode())
    conn.close()


if __name__ == '__main__':
    server()

import ssl
import socket
import threading

# Generate SSL context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(r"C:\Users\srish\localhost.crt", r"C:\Users\srish\localhost.key")

# List of backend servers
backend_servers = [("127.0.0.1", 8000), ("127.0.0.1", 8001),("127.0.0.1", 8002)]
a=b=c=0
def handle_client(client_socket, address):
    global a,b,c
    print(f"Accepted connection from {address}")

    # Pick a backend server (for simplicity, round-robin strategy is used)
    backend_server = backend_servers.pop(0)
    backend_servers.append(backend_server)

    # Connect to the backend server
    backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    backend_socket.connect(backend_server)

    # Forwarding data between client and backend server
    while True:
        data_from_sever=backend_socket.recv(1024)
        if not data_from_sever:
            break
        client_socket.sendall(data_from_sever)

        data_from_client = client_socket.recv(4096)
        if not data_from_client:
            break
        backend_socket.sendall(data_from_client)

    client_socket.close()
    backend_socket.close()
    print(f"Closed connection from {address}")
    if(data_from_client==b'1'):
        a=a+1
    elif(data_from_client==b'2'):
        b=b+1
    elif(data_from_client==b'3'):
        c=c+1
    print("CURRENT STATS",a,b,c)


def main():
    # Create SSL socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12000))
    server_socket.listen(5)

    ssl_socket = ssl_context.wrap_socket(server_socket, server_side=True)

    print("Load balancing server started...")

    while True:
        client_socket, address = ssl_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":
    main()

from socket import *
import threading
import ssl
SERVER_ADDRESSES = [('localhost', 8000), ('localhost', 8001), ('localhost', 8002)]

active_connections = {server_address: 0 for server_address in SERVER_ADDRESSES}
active_connections_lock = threading.Lock()

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain("localhost.crt", "localhost.key")

def handle_client(connection, server_address, server_sockets):
    global active_connections
    with active_connections_lock:
        active_connections[server_address] += 1

    try:
        connection_ssl_socket = ssl_context.wrap_socket(connection, server_side=True)
        for socket_address, server_socket in zip(SERVER_ADDRESSES, server_sockets):
            if socket_address == server_address:
                break
        else:
            raise ValueError("No matching server socket found for the given server address")

        while True:
            # Wrap existing connection with SSL context
            

            # Forward data between client and server
            message_from_server = server_socket.recv(1024).decode()
            connection_ssl_socket.sendall(message_from_server.encode())
            data_from_client = connection_ssl_socket.recv(1024).decode()
            server_socket.sendall(data_from_client.encode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Decrement the active connection count for the server
        with active_connections_lock:
            active_connections[server_address] -= 1

        if 'server_socket' in locals() and server_socket is not None:
            server_socket.close()
        if 'connection_ssl_socket' in locals() and connection_ssl_socket is not None:
            connection_ssl_socket.close()


def main():
    # Create a TCP/IP socket
    proxy_socket = socket(AF_INET, SOCK_STREAM)
    # Bind the socket to the port
    proxy_socket.bind(('localhost', 12000))
    # Listen for incoming connections
    proxy_socket.listen(5)
    print("Proxy server listening on port 12000...")
    server_socket1 = socket(AF_INET, SOCK_STREAM)  # creating a new socket
    server_socket1.connect(('localhost', 8000))  # connects to server1
    server_socket2 = socket(AF_INET, SOCK_STREAM)  # creating a new socket
    server_socket2.connect(('localhost', 8001))  # connects to server2
    server_socket3 = socket(AF_INET, SOCK_STREAM)  # creating a new socket
    server_socket3.connect(('localhost', 8002))  # connects to server3
    while True:
            # Accept a new client connection
            connection, address = proxy_socket.accept()
            #print(f"Accepted connection from {address}")

            # Find the server with the fewest active connections
            with active_connections_lock:
                min_connections_server = min(active_connections, key=active_connections.get)

            server_sockets = [server_socket1, server_socket2, server_socket3]
            # Handle the client request using the server with the fewest active connections
            threading.Thread(target=handle_client, args=(connection, min_connections_server,server_sockets)).start()

if __name__ == "__main__":
    main()

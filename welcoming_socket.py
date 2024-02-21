# Import the necessary modules
import socket
import threading
import ssl

# List of server addresses to balance load across
SERVER_ADDRESSES = [('localhost', 8000), ('localhost', 8001), ('localhost', 8002)]

# Dictionary to store the number of active connections for each server
active_connections = {server_address: 0 for server_address in SERVER_ADDRESSES}

# Lock to ensure thread-safe access to active_connections dictionary
active_connections_lock = threading.Lock()

# SSL context for wrapping sockets
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(r"C:\Users\srish\localhost.crt", r"C:\Users\srish\localhost.key")

def handle_client(connection_socket, server_address):
    global active_connections

    # Increment the active connection count for the server
    with active_connections_lock:
        active_connections[server_address] += 1

    try:
        # Connect to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Wrap the server socket with SSL/TLS
            connection_ssl_socket = ssl_context.wrap_socket(connection_socket,server_side=True)
            connection_ssl_socket.connect(server_address)

            # Forward data between client and server
            while True:
                data = connection_ssl_socket.recv(1024)
                if not data:
                    break
                connection_ssl_socket.sendall(data)
                response = connection_ssl_socket.recv(1024)
                if not response:
                    break
                connection_ssl_socket.sendall(response)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Decrement the active connection count for the server
        with active_connections_lock:
            active_connections[server_address] -= 1
        connection_ssl_socket.close()

def main():
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
        # Bind the socket to the port
        proxy_socket.bind(('localhost', 12000))
        # Listen for incoming connections
        proxy_socket.listen(5)
        print("Proxy server listening on port 12000...")

        while True:
            # Accept a new client connection
            connection_socket, address = proxy_socket.accept()
            #print(f"Accepted connection from {address}")

            # Find the server with the fewest active connections
            with active_connections_lock:
                min_connections_server = min(active_connections, key=active_connections.get)

            # Handle the client request using the server with the fewest active connections
            threading.Thread(target=handle_client, args=(connection_socket, min_connections_server)).start()

if __name__ == "__main__":
    main()

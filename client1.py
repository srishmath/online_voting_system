from socket import *
import ssl
import threading
import random

def client_thread():
    serverName = '192.168.96.67'
    serverPort = 12000
    
    # Create a socket object for TCP/IP connection
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # Create SSL context and load certificate
   
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT) #Transport Layer Security
    context.check_hostname = False #not checking as hostname is statically assigned
    context.verify_mode = ssl.CERT_NONE #NONE due to self signed certificate
    
    ssock = context.wrap_socket(clientSocket, server_hostname=serverName)
    ssock.connect((serverName, serverPort))
    
   
    
    # Send and receive data
    print("Connected to server")
    Sentence_recv = ssock.recv(1024).decode()
    print("Received from server:", Sentence_recv)
    
    # Generate a random number between 1, 2, or 3
    num = str(random.randint(1, 3))
    ssock.send(num.encode())
    
    received_data = ssock.recv(1024).decode()
    print("Received from server:", received_data)

    # Close the connection
    ssock.close()
    print("Connection closed")

# Number of clients to create
num_clients = 100

# Create and start threads for each client
threads = []
for i in range(num_clients):
    thread = threading.Thread(target=client_thread)
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

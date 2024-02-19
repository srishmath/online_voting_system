from socket import *
import ssl
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

#SSL CONTEXT CREATION

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(r"C:\Users\srish\localhost.crt",r"C:\Users\srish\localhost.key")


while True:
    connectionSocket, addr = serverSocket.accept()
    ssock=context.wrap_socket(connectionSocket,server_side=True)
    message='select person 1:you,person 2:me'
    ssock.send(message.encode())

    sentence = ssock.recv(1024).decode()
    
    print("recieved: ",sentence)
    ssock.close()

    # # Choose a server to forward the connection to
    # server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_sock.connect(("localhost", 8000))

    # # Forward the connection
    # server_sock.sendall(client_sock.recv(1024))

    # # Close the connections
 

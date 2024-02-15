from socket import *
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()

    message='select person 1:you,person 2:me'
    connectionSocket.send(message.encode())

    sentence = connectionSocket.recv(1024).decode()
    # capitalizedSentence = sentence.upper()
    # connectionSocket.send(capitalizedSentence.encode())
    print("recived: ",sentence)
    connectionSocket.close()

    # # Choose a server to forward the connection to
    # server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_sock.connect(("localhost", 8000))

    # # Forward the connection
    # server_sock.sendall(client_sock.recv(1024))

    # # Close the connections
 
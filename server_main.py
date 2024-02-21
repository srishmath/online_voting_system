from socket import *
import ssl
import threading



serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(20)
print('The server is ready to receive')
a=b=c=0
count=0

#SSL CONTEXT CREATION

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(r"C:\Users\srish\localhost.crt",r"C:\Users\srish\localhost.key")


while True:
    connectionSocket, addr = serverSocket.accept()
    ssock=context.wrap_socket(connectionSocket,server_side=True)
    count=count+1
    


    message="select person 1:A,person 2:B,person 3:C"
    ssock.send(message.encode())

    sentence = ssock.recv(1024).decode()
    
    print("recieved: ",sentence)
    print("hello",type(sentence))
    if(sentence=='1'):
        
        a=a+1
    elif(sentence=='2'):
        b=b+1

    else:
        c=c+1
    ssock.close()

    print(a,b,c)
    # # Choose a server to forward the connection to
    # server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_sock.connect(("localhost", 8000))

    # # Forward the connection
    # server_sock.sendall(client_sock.recv(1024))

    # # Close the connections
 

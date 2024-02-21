from socket import *
import ssl

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations(r"C:\Users\srish\localhost.crt")

# Wrap the socket object with the SSL context
ssock = context.wrap_socket(clientSocket, server_hostname='localhost')

ssock.connect((serverName,serverPort))
# sentence = input('Input lowercase sentence:')
# clientSocket.send(sentence.encode())

Sentence_recv = ssock.recv(1024)
print(Sentence_recv)
num=input("enter no:")
modifiedMessage=num
ssock.send(modifiedMessage.encode())
ssock.close()

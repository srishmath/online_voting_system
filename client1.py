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
print("hi")
Sentence_recv = ssock.recv(1024).decode()
print("hi")
print(Sentence_recv)
num=input("enter no:")
modifiedMessage=num
ssock.send(modifiedMessage.encode())
received_data=ssock.recv(1024)



# Decode and print the statistics
stats = received_data.decode().split(',')
print("Received stats:")
print("Stat 1:", stats[0])
print("Stat 2:", stats[1])
print("Stat 3:", stats[2])
ssock.close()

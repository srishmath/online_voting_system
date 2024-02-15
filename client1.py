from socket import *
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
# sentence = input('Input lowercase sentence:')
# clientSocket.send(sentence.encode())

Sentence_recv = clientSocket.recv(1024)
print(Sentence_recv)
num=input("enter no:")
modifiedMessage="chose"+num
clientSocket.send(modifiedMessage.encode())
clientSocket.close()
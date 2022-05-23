import socket
import time
import sys
sys.path.append('./src')
import ConfigFile as cf

print("**********************************************************************************************************")
print("TEST FILE TO PERFORM INVERTED INDEX")
print("**********************************************************************************************************\n")

ClientSocket = socket.socket()
host = cf.server_name
port = cf.server_port_num

ClientSocket.connect((host, port))

ClientSocket.send(str.encode('5'))
time.sleep(0.01)
ClientSocket.send(str.encode('6'))
time.sleep(0.01)
ClientSocket.send(str.encode('data1.txt'))
time.sleep(0.01)
ClientSocket.send(str.encode('inverted index'))
time.sleep(0.01)
ClientSocket.send(str.encode('inverted index'))
time.sleep(0.01)
ClientSocket.send(str.encode('output1'))
time.sleep(0.01)
Response = ClientSocket.recv(1024)
time.sleep(0.01)
print("Status of Inverted Index operation:")
print(Response.decode('utf-8'))
print("************************************************************************************************************\n")
ClientSocket.close()
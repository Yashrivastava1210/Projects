import socket
import time
import sys
sys.path.append('./src')
import ConfigFile as cf

print("**********************************************************************************************************")
print("TEST FILE TO CONNECT MULTIPLE CLIENTS TO THE MASTER SERVER")
print("**********************************************************************************************************\n")


ClientSocket1 = socket.socket()
ClientSocket2 = socket.socket()
host = cf.server_name
port = cf.server_port_num

print("Connecting client 1")
ClientSocket1.connect((host, port))
print("Connecting client 2")
ClientSocket2.connect((host, port))

ClientSocket1.send(str.encode('5'))
ClientSocket2.send(str.encode('5'))
time.sleep(0.01)
ClientSocket1.send(str.encode('6'))
ClientSocket2.send(str.encode('6'))
time.sleep(0.01)
ClientSocket1.send(str.encode('data.txt'))
ClientSocket2.send(str.encode('data1.txt'))
time.sleep(0.01)
ClientSocket1.send(str.encode('word count'))
ClientSocket2.send(str.encode('inverted index'))
time.sleep(0.01)
ClientSocket1.send(str.encode('word count'))
ClientSocket2.send(str.encode('inverted index'))
time.sleep(0.01)
ClientSocket1.send(str.encode('output'))
ClientSocket2.send(str.encode('output1'))
time.sleep(0.01)
Response1 = ClientSocket1.recv(1024)
Response2 = ClientSocket2.recv(1024)
time.sleep(0.01)
print("Response from client 1:")
print(Response1.decode('utf-8'))
print("Response from client 2:")
print(Response2.decode('utf-8'))

print("Closeing client 1")
ClientSocket1.close()
print("Closeing client 2")
print("************************************************************************************************************\n")
ClientSocket2.close()
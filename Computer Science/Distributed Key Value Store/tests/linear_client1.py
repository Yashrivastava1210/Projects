import socket
import time
import sys
from datetime import datetime
sys.path.append('./servers')
import ConfigFile as cf


server1Name = cf.server1_name
server1Port = cf.server1_port_num
clientSocket = socket.socket()
clientSocket.connect((server1Name,server1Port))
print("**************************************************************************")
print("TEST FILE TO CHECK FOR Linearizability")
print("**************************************************************************\n")
print("Starting client for W1(k,v) from client 1\n")
now = datetime.now().strftime("%H:%M:%S")
print("Operation starting at: "+ str(now))
command1 = "set test1 50 linear\r\n"
clientSocket.send(command1.encode())
time.sleep(0.01)
command1_value = "1" 
clientSocket.send(command1_value.encode())
status = clientSocket.recv(9542).decode()
print(status)
print("Ending connection for W1(k,v) Operation from client 1\n")
print("**************************************************************************\n")
clientSocket.close()

time.sleep(8)

clientSocket = socket.socket()
clientSocket.connect((server1Name,server1Port))
print("Starting client for W2(k,v) from client 1\n")
now = datetime.now().strftime("%H:%M:%S")
print("Operation starting at: "+ str(now))
command1 = "set test1 50 linear\r\n"
clientSocket.send(command1.encode())
time.sleep(0.01)
command1_value = "5" 
clientSocket.send(command1_value.encode())
status = clientSocket.recv(9542).decode()
print(status)
print("Ending connection for W2(k,v) Operation from client 1\n")
print("**************************************************************************\n")
clientSocket.close()
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
print("TEST FILE TO CHECK FOR LINEAR CONSISTENCY")
print("**************************************************************************\n")
print("Starting client for W1(k,v)\n")
now = datetime.now().strftime("%H:%M:%S")
print("Operation starting for W1(k,v) at: "+ str(now))
command1 = "set test1 50 linear\r\n"
clientSocket.send(command1.encode())
time.sleep(0.01)
command1_value = "1" 
clientSocket.send(command1_value.encode())
status = clientSocket.recv(9542).decode()
print("Response for  W1(k,v) operation: "+ status)
print("Ending connection for W1(k,v) Operation\n")
print("**************************************************************************\n")
clientSocket.close()
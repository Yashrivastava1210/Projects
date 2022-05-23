import socket
import time
import sys
from datetime import datetime
sys.path.append('./servers')
import ConfigFile as cf

time.sleep(7)
print()
server2Name = cf.server2_name
server2Port = cf.server2_port_num
clientSocket = socket.socket()
clientSocket.connect((server2Name,server2Port))
start = time.time()
print("Starting client for R1(k) from client 2\n")
now = datetime.now().strftime("%H:%M:%S")
print("Operation starting at: "+ str(now))
command2 = "get test1 linear"
clientSocket.send(command2.encode())
get_result = clientSocket.recv(9541).decode()
print(get_result)
get_end = clientSocket.recv(9541).decode()
end = time.time()
print(get_end)
print("Ending connection for R1(k) Operation from client 2\n")
print("Total time for read operation in linear consistency: "+ str(end - start))
clientSocket.close()

time.sleep(4)
server1Name = cf.server1_name
server1Port = cf.server1_port_num
clientSocket = socket.socket()
clientSocket.connect((server1Name,server1Port))
print("Starting client for W1(k,v) from client 2\n")
now = datetime.now().strftime("%H:%M:%S")
print("Operation starting at: "+ str(now))
start = time.time()
command1 = "set test1 50 linear\r\n"
clientSocket.send(command1.encode())
time.sleep(0.01)
command1_value = "3" 
clientSocket.send(command1_value.encode())
status = clientSocket.recv(9542).decode()
print(status)
end = time.time()
print("Ending connection for W1(k,v) Operation from client 2\n")
print("**************************************************************************\n")
clientSocket.close()
print("Total time for write operation in linear consistency: "+ str(end - start))

time.sleep(2)
print()
server2Name = cf.server2_name
server2Port = cf.server2_port_num
clientSocket = socket.socket()
clientSocket.connect((server2Name,server2Port))
print("Starting client for R2(k) from client 2\n")
now = datetime.now().strftime("%H:%M:%S")
print("Operation starting at: "+ str(now))
command2 = "get test1 linear"
clientSocket.send(command2.encode())
get_result = clientSocket.recv(9541).decode()
print(get_result)
get_end = clientSocket.recv(9541).decode()
print(get_end)
print("Ending connection for R2(k) Operation from client 2\n")
clientSocket.close()

print("**************************************************************************\n")
time.sleep(5)
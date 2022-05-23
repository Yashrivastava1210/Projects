import socket
import time
import sys
from datetime import datetime
sys.path.append('./servers')
import ConfigFile as cf

time.sleep(1)
server1Name = cf.server1_name
server1Port = cf.server1_port_num
clientSocket = socket.socket()
clientSocket.connect((server1Name,server1Port))
start = time.time()
print("Starting client for W2(k,v) from client 1\n")
now = datetime.now().strftime("%H:%M:%S")
print("Operation for W2(k,v) starting at: "+ str(now))
command1 = "set test1 50 linear\r\n"
clientSocket.send(command1.encode())
time.sleep(0.01)
command1_value = "1" 
clientSocket.send(command1_value.encode())
status = clientSocket.recv(9542).decode()
print("Response for  W2(k,v) operation: "+ status)
print("Ending connection for W2(k,v) Operation from client 1\n")
print("**************************************************************************\n")
clientSocket.close()
end = time.time()
print("Total time for write operation in linear consistency: "+ str(end - start))
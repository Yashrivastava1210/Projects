import socket
import time
import sys
from datetime import datetime
sys.path.append('./servers')
import ConfigFile as cf

time.sleep(0.2)
server1Name = cf.server1_name
server1Port = cf.server1_port_num
clientSocket = socket.socket()
clientSocket.connect((server1Name,server1Port))
start = time.time()
print("Starting client for R1(k) from client 1\n")
now = datetime.now().strftime("%H:%M:%S")
print("Operation starting at: "+ str(now))
command2 = "get test1"
clientSocket.send(command2.encode())
get_result = clientSocket.recv(9541).decode()
print(get_result)
get_end = clientSocket.recv(9541).decode()
print("Response for  R1(k,v) operation: "+get_end)
print("Ending connection for R1(k) Operation from client 1\n")
clientSocket.close()
end = time.time()
print("Total time for read operation in linear consistency: "+ str(end - start))
time.sleep(10)
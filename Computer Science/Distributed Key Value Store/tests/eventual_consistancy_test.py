import socket
import time
import sys
sys.path.append('./servers')
import ConfigFile as cf

server1Name = cf.server1_name
server1Port = cf.server1_port_num
clientSocket = socket.socket()
clientSocket.connect((server1Name,server1Port))
print("**************************************************************************")
print("TEST FILE TO CHECK FOR EVENTUAL CONSISTANCY")
print("**************************************************************************\n")
print("Starting client to Set value for key \"test1\" in server 1\n")
command1 = "set test1 51 eventual\r\n"
start = time.time()
clientSocket.send(command1.encode())
time.sleep(0.01)
command1_value = "15" 
clientSocket.send(command1_value.encode())
status = clientSocket.recv(9542).decode()
print(status)
print("Ending connection for Set Operation\n")
print("**************************************************************************\n")
end = time.time()
print("Total time for write operation in eventual consistency: "+ str(end - start))
clientSocket.close()

server2Name = cf.server2_name
server2Port = cf.server2_port_num
clientSocket = socket.socket()
clientSocket.connect((server2Name,server2Port))
start = time.time()
print("Starting client to Get value for key \"test1\" from server 2\n")
command2 = "get test1"
clientSocket.send(command2.encode())
get_result = clientSocket.recv(9541).decode()
print(get_result)
get_end = clientSocket.recv(9541).decode()
print(get_end)
print("Ending connection for Get Operation\n")
end = time.time()
print("Total time for read operation in eventual consistency: "+ str(end - start))
clientSocket.close()

print("**************************************************************************\n")
clientSocket = socket.socket()
clientSocket.connect((server1Name,server1Port))
print("Starting client to Get value for key \"test1\" from server 1\n")
command2 = "get test1"
clientSocket.send(command2.encode())
get_result = clientSocket.recv(9542).decode()
print(get_result)
get_end = clientSocket.recv(9542).decode()
print(get_end)
print("Ending connection for Get Operation\n")
clientSocket.close()

time.sleep(25)
clientSocket = socket.socket()
clientSocket.connect((server2Name,server2Port))
print("***************************************************************************\n")
print("Starting client to Get value for key \"test1\" from server 2 after eventual consistancy is achieved\n")
command2 = "get test1"
clientSocket.send(command2.encode())
get_result = clientSocket.recv(9541).decode()
print(get_result)
get_end = clientSocket.recv(9541).decode()
print(get_end)
print("Ending connection for Get Operation\n")
print("**************************************************************************\n")
clientSocket.close()
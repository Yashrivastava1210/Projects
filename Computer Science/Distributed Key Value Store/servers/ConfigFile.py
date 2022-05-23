import threading
# Change the port number where you want to run the master server
server1_port_num = 8211
server2_port_num = 8212
# Change the server name where you want to run the master server
server1_name = 'localhost'
server2_name = 'localhost'

lock = threading.Lock()
sequential = 0
current = 1
lock2 = threading.Lock()

def increment():
    global sequential
    sequential += 1
import socket
import sys
from configparser import ConfigParser
import init_config

config = ConfigParser()
config.read('config.ini')

ip = "192.168.3.1"
port = 3567

# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
print("Do Ctrl+c to exit the program !!")

# Let's send data through UDP protocol
while True:
    send_data = input("Type some text to send =>")
    s.sendto(send_data.encode('utf-8'), (ip, port))
    if config.getboolean('DEBUG','PRINT_LOGS') is True:
        print("\n\n 1. Client Sent : ", send_data, "\n\n")
# close the socket
s.close()
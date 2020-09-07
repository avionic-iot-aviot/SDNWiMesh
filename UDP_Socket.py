import socket
import sys

def RunReceiverProcess(ip,port):
    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    server_address = (ip, port)
    s.bind(server_address)
    print("Do Ctrl+c to exit the program !!")

def SendPacket(data,address):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(data.encode('utf-8'), address)
    print("\n\n 1. Server sent : ", data,"\n\n")

def ReceiverPacket(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        data, address = s.recvfrom(4096)
        print("\n\n 2. Server received: ", data.decode('utf-8'), "\n\n")
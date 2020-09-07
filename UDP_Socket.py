import threading
import socket
import sys
import time
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

# def RunReceiverProcess(ip,port):
#     # Create a UDP socket
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     # Bind the socket to the port
#     server_address = (ip, port)
#     s.bind(server_address)
#     print("Do Ctrl+c to exit the program !!")

# def SendPacket(data,address):
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.sendto(data.encode('utf-8'), address)
#     print("\n\n 1. Server sent : ", data,"\n\n")

# def ReceiverPacket(address):
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     while True:
#         data, address = s.recvfrom(4096)
#         print("\n\n 2. Server received: ", data.decode('utf-8'), "\n\n")


class ThreadServer (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter

   def run(self):
       print("Starting " + self.name)
       if (socket.gethostname() == "Omega-1D63"):
           Start_Udp("192.168.0.1", int(config['GENERAL']['Port']))
       if (socket.gethostname() == "Omega-1D06"):
           Start_Udp("192.168.1.1", int(config['GENERAL']['Port']))


def Start_Udp(ip, port):
    localIP     = ip
    localPort   = port
    bufferSize  = 1024

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, localPort))

    print("UDP server up and listening")

    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)
        print(clientMsg)
        print(clientIP)

# def Start_Udp(ip, port):
#     # Create a UDP socket
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     # Bind the socket to the port
#     server_address = (ip, port)
#     s.bind(server_address)
#     while True:
#         data, address = s.recvfrom(4096)
#         print("\n\n\t\t Server received from [", address, "] :" , data.decode('utf-8'), "\n\n")


class ThreadClient (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter

   def run(self):
      print ("Starting " + self.name)
      if (socket.gethostname() == "Omega-1D63"):
          SendPacket("8.8.8.8", "Ciaoooo")
      if (socket.gethostname() == "Omega-1D06"):
          SendPacket("192.168.0.1", "CIaooooooooo")

def SendPacket(address,data):
    msgFromClient       = data
    bytesToSend         = str.encode(msgFromClient)
    serverAddressPort   = (address, int(config['GENERAL']['Port']))
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    while True:
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        print("Send to -> ", address)
        time.sleep(4)



# def SendPacket(data,address):
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.sendto(data.encode('utf-8'), address)
#     print("\n\n\t\tServer Sent to [",address,"] : ", data,"\n\n")



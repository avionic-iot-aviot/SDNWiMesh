import threading
import socket
import sys
import time
import PacketsHandler
from Packets import BeaconPacket
from Packets import Packets
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


class ThreadReceiverUdpPackets (threading.Thread):
   def __init__(self, threadID, name, port):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.port = port

   def run(self):
       print("Starting " + self.name)
       #UdpSocketReceiver( config.get(socket.gethostname(),'IpStation') , int(config['GENERAL']['Port']) )
       UdpSocketReceiver( self.port )

def UdpSocketReceiver(port):
    bufferSize  = 1024
    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
    UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    UDPServerSocket.bind(("", port ))
   #  UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
   #  UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        PacketsHandler.PacketHandler(message)

        # clientMsg = "Message from Client:{}".format(message)
        # clientIP  = "Client IP Address:{}".format(address)
        # print(clientMsg)
        # print(clientIP)

# def Start_Udp(ip, port):
#     # Create a UDP socket
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     # Bind the socket to the port
#     server_address = (ip, port)
#     s.bind(server_address)
#     while True:
#         data, address = s.recvfrom(4096)
#         print("\n\n\t\t Server received from [", address, "] :" , data.decode('utf-8'), "\n\n")


# class ThreadClient (threading.Thread):
#    def __init__(self, threadID, name, counter,myip):
#       threading.Thread.__init__(self)
#       self.threadID = threadID
#       self.name = name
#       self.counter = counter
#       self.MyIp = myip

#    def run(self):
#       print ("Starting " + self.name)

#       #if (socket.gethostname() == "Omega-1D63"):
#       #    SendPacket("8.8.8.8", "Ciaoooo")
#       if (socket.gethostname() == "Omega-1D06"):
#           SendPacket("192.168.0.1",self.MyIp)

# def SendPacket(address,MyIp):
#     #beacon = BeaconPacket(int(config['GENERAL']['Port']),)
#     pckdata = Packets (config.get(socket.gethostname(),'NetId'), "0" , address, MyIp, "1","100", "address","Pck Data!!!!" )
#     bytesToSend         = pckdata.getBytesFromPackets()
#     serverAddressPort   = (address, int(config['GENERAL']['Port']))
#     UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
#    #  UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    

#     while True:
#         UDPClientSocket.sendto(bytesToSend, serverAddressPort)
#         print("Send to -> ", address)
#         time.sleep(6)

# def SendPacket(data,address):
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.sendto(data.encode('utf-8'), address)
#     print("\n\n\t\tServer Sent to [",address,"] : ", data,"\n\n")


class ThreadBeacon (threading.Thread):
   def __init__(self, threadID, name, beacon, port):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.beacon = beacon
      self.port = port

   def run(self):
      print ("Starting " + self.name)
      SendUdpPacketBroadcastLoop(self.beacon, self.port)

def SendUdpPacketBroadcastLoop(beacon,port):
   bytesToSend         = beacon
   serverAddressPort   = ('<broadcast>', port)
   UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
   UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
   UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
   UDPClientSocket.settimeout(0.2)
   while True:
      UDPClientSocket.sendto(bytesToSend, serverAddressPort)
      print("Broadcast Beacon Send!")
      time.sleep(4)


def SendUdpPacketBroadcast(data,port):
    bytesToSend         = data
    serverAddressPort   = ('<broadcast>', port)
    UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    print("Broadcast Packet Send!")

def SendUdpPacketUnicast(data,address,port):
    bytesToSend         = data
    serverAddressPort   = (address, port)
    UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    print("Unicast Packet Send!")




# def SendPacket(address,MyIp):
#     #beacon = BeaconPacket(int(config['GENERAL']['Port']),)
#     pckdata = Packets (config.get(socket.gethostname(),'NetId'), "0" , address, MyIp, "1","100", "address","Pck Data!!!!" )
#     bytesToSend         = pckdata.getBytesFromPackets()
#     serverAddressPort   = (address, int(config['GENERAL']['Port']))
#     UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
#    #  UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    

#     while True:
#         UDPClientSocket.sendto(bytesToSend, serverAddressPort)
#         print("Send to -> ", address)
#         time.sleep(6)
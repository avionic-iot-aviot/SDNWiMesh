import threading
import socket
import sys
import time
import PacketsHandler
from Packets import ReportPacket
from Packets import BeaconPacket
from Packets import Packets
import node_variables
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

# --- Thread Receiver Udp Packets --- #
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
        PacketsHandler.PacketHandler(message, address)

        # clientMsg = "Message from Client:{}".format(message)
        # clientIP  = "Client IP Address:{}".format(address)
        # print(clientMsg)
        # print(clientIP)


# --- Thread Beacon Udp Packets --- #
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
      time.sleep(int(config['GENERAL']['BeaconSleep']))


# --- Thread Report Udp Packets --- #
class ThreadReport (threading.Thread):
   def __init__(self, threadID, name, port, s_address, d_address):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.port = port
      self.s_address = s_address
      self.d_address = d_address

   def run(self):
      print ("Starting " + self.name)
      SendUdpPacketUnicastLoop(self.port, self.s_address, self.d_address)

def SendUdpPacketUnicastLoop(port,src,dst):
   serverAddressPort   = (dst, port)
   UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
   UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
   UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
   UDPClientSocket.settimeout(0.2)
   while True:
      pckReort = ReportPacket ( config.get(socket.gethostname(),'NetId'), config['GENERAL']['IpSink'], src, "100", dst, "Ciaoo")
      bytesToSend = pckReort.getBytesFromPackets()
      UDPClientSocket.sendto(bytesToSend, serverAddressPort)
      print("Unicast Report Send!")
      time.sleep(int(config['GENERAL']['BeaconSleep']))


# --- Generic Function For Send Udp Packets --- #
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



class ThreadPrintInfoNode (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name

   def run(self):
       print("Starting " + self.name)
       #UdpSocketReceiver( config.get(socket.gethostname(),'IpStation') , int(config['GENERAL']['Port']) )
       PrintBasicInfo(1,0)

def PrintBasicInfo(NeighborInfo,OtherInfo):
    while True:
      print("\n[B-INFO] Network ID: ", config.get(socket.gethostname(),'NetId') )
      print("[B-INFO] Node ID: ", config.get(socket.gethostname(),'Id') )
      print("[B-INFO] SINK: ", config.get(socket.gethostname(),'Sink') )
      print("[B-INFO] Ip Station: ", node_variables.IpStation )
      print("[B-INFO] Ip Client: ", node_variables.IpClient )
      print("[B-INFO] Default Gateway: ", node_variables.IpDefaultGateway )
      if (NeighborInfo == 1):
         print("[Nei-INFO] Network ID: ", node_variables.list_neighbor )
      if (OtherInfo == 1):
         print(" --- ")
      print("\n")
      time.sleep(int(config['GENERAL']['InfoSleep']))
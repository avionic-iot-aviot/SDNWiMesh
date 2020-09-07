import threading
import socket
import sys

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
           Start_Udp("192.168.0.1", 4000)
       if (socket.gethostname() == "Omega-1D06"):
           Start_Udp("192.168.1.1", 4000)


def Start_Udp(ip, port):
    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    server_address = (ip, port)
    s.bind(server_address)
    while True:
        data, address = s.recvfrom(4096)
        print("\n\n\t\t Server received from [", address, "] :" , data.decode('utf-8'), "\n\n")


class ThreadClient (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter

   def run(self):
      print ("Starting " + self.name)
      if (socket.gethostname() == "Omega-1D63"):
          SendPacket("192.168.0.130", "Ciaoooo")
      if (socket.gethostname() == "Omega-1D06"):
          SendPacket("192.168.1.130", "CIaooooooooo")

def SendPacket(data,address):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(data.encode('utf-8'), address)
    print("\n\n\t\tServer Sent to [",address,"] : ", data,"\n\n")

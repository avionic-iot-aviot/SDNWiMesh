from Packets import BeaconPacket
from Packets import Packets
import init_config
import socket
import ifaddr
import time
import UDP_Socket
import threading
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')


############ 0. Asseganre gli Indirizzi Ip Nuovi ############
print("\n\n\t\tSTART SDNWISE\n\n")

init_config.Inizio()

print("\n\tIndirizzi Ip Asseganti\n")

############ 1. Calcolo Indirizzi Ip Nuovi ############
adapters = ifaddr.get_adapters()

for adapter in adapters:
    if (adapter.nice_name == "br-wlan"):
        IpStation = adapter.ips[0].ip
    if (adapter.nice_name == "apcli0"):
        IpClient = adapter.ips[0].ip

print(f"Client: {IpClient} \tStation: {IpStation}")

############ 2. Avvio Server UDP ############

# Create new threads
ThreadUdpReceiver = UDP_Socket.ThreadReceiverUdpPackets(1, "Thread-UdpReceiver", int(config['GENERAL']['Port']) )

pckBeacon = BeaconPacket ( config.get(socket.gethostname(),'NetId'), config.get(socket.gethostname(),'IpBroadcast') , IpStation, "100", config.get(socket.gethostname(),'IpBroadcast') )
ThreadUdpBeacon = UDP_Socket.ThreadBeacon( 2, "Thread-Beacon", pckBeacon.getBytesFromPackets() , int(config['GENERAL']['Port']) )
# if (socket.gethostname() == "Omega-1D06"):
#     thread3 = UDP_Socket.ThreadClient(3, "Thread-DATA", 3, IpStation)

# Start new Threads
ThreadUdpReceiver.start()
ThreadUdpBeacon.start()
# if (socket.gethostname() == "Omega-1D06"):
#     thread3.start()

############ 2. Avvio Server UDP ############


# UDP_Socket.RunReceiverProcess(IpStation,4000)
# UDP_Socket.ReceiverPacket(IpStation)

# while True:
#     UDP_Socket.SendPacket("Ciao","192.168.0.130")



# MULTICAST


# if ( socket.gethostname() == "Omega-1D63"):
#     server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#     server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
#     server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#     server.settimeout(0.2)
#     message = b"your very important message"
#     while True:
#         server.sendto(message, ('<broadcast>', 37020))
#         print("message sent!")
#         time.sleep(1)

# if ( socket.gethostname() == "Omega-1D06"):
#     client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
#     client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
#     client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#     client.bind(("", 37020))
#     while True:
#         data, addr = client.recvfrom(1024)
#         print("received message: %s"%data)



# PACKETS


# p1 = BeaconPacket("1","10.10.0.1","10.10.0.0","100","10.10.0.1")
# print(p1.printFullPacket())
# print(p1.printLitePacket())

# p1.getBytesFromPackets() 

# test = bytearray(b'-1--46------10.10.0.1------10.10.0.0-0100------10.10.0.1Payload BEACON')
# p2 = Packets.getPacketFromBytes(test)

# print(p2.printFullPacket())
# print(p2.printLitePacket())


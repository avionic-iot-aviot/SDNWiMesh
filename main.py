from Packets import BeaconPacket
from Packets import Packets
import init_config
import socket
import ifaddr
import time
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')


print("\n\n\t\tSTART SDNWISE\n\n")

init_config.Inizio()

print("\n\tIndirizzi Ip Asseganti\n")
hostname = socket.gethostname()



# p1 = BeaconPacket("1","10.10.0.1","10.10.0.0","100","10.10.0.1")
# print(p1.printFullPacket())
# print(p1.printLitePacket())

# p1.getBytesFromPackets() 

# test = bytearray(b'-1--46------10.10.0.1------10.10.0.0-0100------10.10.0.1Payload BEACON')
# p2 = Packets.getPacketFromBytes(test)

# print(p2.printFullPacket())
# print(p2.printLitePacket())



adapters = ifaddr.get_adapters()

for adapter in adapters:
    if (adapter.nice_name == "br-wlan"):
        IpStation = adapter.ips[0].ip
    if (adapter.nice_name == "apcli0"):
        IpClient = adapter.ips[0].ip

print(f"Client: {IpClient} \tStation: {IpStation}")

if ( socket.gethostname() == "Omega-1D63"):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    server.settimeout(0.2)
    message = b"your very important message"
    while True:
        server.sendto(message, ('<broadcast>', 37020))
        print("message sent!")
        time.sleep(1)

if ( socket.gethostname() == "Omega-1D06"):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    client.bind(("", 37020))
    while True:
        data, addr = client.recvfrom(1024)
        print("received message: %s"%data)

from Packets import BeaconPacket
from Packets import Packets
import socket
import ifaddr
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')


print("\n\n\t\tSTART SDNWISE\n\n")

hostname = socket.gethostname()

if (hostname == config["Omega-1D63"]):
    print("YESS")

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
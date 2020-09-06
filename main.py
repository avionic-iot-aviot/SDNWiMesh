from Packets import BeaconPacket
from Packets import Packets
import socket
import ifaddr
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')



p1 = BeaconPacket("1","10.10.0.1","10.10.0.0","100","10.10.0.1")
print(p1.printFullPacket())
print(p1.printLitePacket())

p1.getBytesFromPackets() 

test = bytearray(b'-1--46------10.10.0.1------10.10.0.0-0100------10.10.0.1Payload BEACON')
p2 = Packets.getPacketFromBytes(test)

print(p2.printFullPacket())
print(p2.printLitePacket())


hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")

adapters = ifaddr.get_adapters()

for adapter in adapters:
    if (adapter.nice_name == "br-wlan"):
        print(adapter.ips[0])
        # for ip in adapter.ips:
        #     print("%s/%s" % (ip.ip, ip.network_prefix))
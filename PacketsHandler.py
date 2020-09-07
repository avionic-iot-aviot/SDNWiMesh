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


def PacketHandler(data):
    packet = Packets.getPacketFromBytes(data)
    if(int(packet.Type) == 0):
        TypeBeacon(packet)
    if(int(packet.Type) == 1):
        TypeData(packet)
    if(int(packet.Type) != 1 or int(packet.Type) != 0):
        print("Pacchetto di tipo sconosciuto")


def TypeBeacon(packet):
    if ( packet.Source != config.get(socket.gethostname(),'IpStation') ):
        print("Beacon Ricevuto")

def TypeData(packet):
    if ( packet.Source != config.get(socket.gethostname(),'IpStation') ):
        print("Data Ricevuto")
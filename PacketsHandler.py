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


def PacketHandler(self, data):
    packet = Packets.getPacketFromBytes(data)
    PacketHandlerSwitchCase(int(packet.Type))

def PacketHandlerSwitchCase(i):
    switcher = {
        0: TypeBeacon(),
        1: print('Pacchetto di Path'),
        2: TypeData()
    }
    return switcher.get(i, "Tipo di pacchetto invalido")

def TypeBeacon():
    print("Beacon Ricevuto")

def TypeData():
    print("Data Ricevuto")
from Packets import BeaconPacket
from Packets import Packets
import init_config
import socket
import ifaddr
import time
import UDP_Socket
import threading
import node_variables
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')


def PacketHandler(data, address):
    packet = Packets.getPacketFromBytes(data)
    print (packet.Destination,config.get(socket.gethostname(),'IpStation'))
    if (packet.Destination == config.get(socket.gethostname(),'IpStation') ):
        if(int(packet.Type) == 0):
            TypeBeacon(packet)
        if(int(packet.Type) == 1):
            TypeReport(packet)
        if(int(packet.Type) == 2):
            TypeData(packet)
    else:
        packet.DecreaseTTL()
        UDP_Socket.SendUdpPacketUnicast(data,node_variables.IpDefaultGateway,int(config['GENERAL']['Port']))



def TypeBeacon(packet):
    if ( packet.Source != config.get(socket.gethostname(),'IpStation') ):
        print("Beacon Ricevuto from: ",packet.Source)
        if (config.get(socket.gethostname(),'Sink') == "NO"):
            UpdateNeighborList(packet.Source)
            packet.ChangeDst(config['GENERAL']['IpSink'])
            data=packet.getBytesFromPackets()
            UDP_Socket.SendUdpPacketUnicast(data,node_variables.IpDefaultGateway,int(config['GENERAL']['Port']))
        else:
            if (packet.TTL == "100" ):
                UpdateNeighborList(packet.Source)
                data=packet.getBytesFromPackets()
                UDP_Socket.SendUdpPacketUnicast(data,node_variables.IpDefaultGateway,int(config['GENERAL']['Port']))
            else: 
                data=packet.getBytesFromPackets()
                UDP_Socket.SendUdpPacketUnicast(data,node_variables.IpDefaultGateway,int(config['GENERAL']['Port']))


def TypeReport(packet):
    if ( packet.Source != config.get(socket.gethostname(),'IpStation') ):
        print("Report Ricevuto from: ", packet.Source)
        data=packet.getBytesFromPackets()
        UDP_Socket.SendUdpPacketUnicast(data,node_variables.IpDefaultGateway,int(config['GENERAL']['Port']))


def TypeData(packet):
    if ( packet.Source != config.get(socket.gethostname(),'IpStation') ):
        print("Data Ricevuto from: ", packet.Source)


def UpdateNeighborList(ip):
    if ( FindIpInTheNeighborList(ip) == 0 ):
        node_variables.list_neighbor.append(ip)

def FindIpInTheNeighborList(ip):
    return ip in node_variables.list_neighbor

def SendReportToSink(packet):
    print ( packet.TTL )

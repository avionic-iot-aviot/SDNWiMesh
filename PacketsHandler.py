from Packets import BeaconPacket
from Packets import FunctionPacket
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
from AudioFile import GetAudio

# verifco se il pacchetto è per me o no


def PacketHandler(data, address):
    packet = Packets.getPacketFromBytes(data)
    print (packet.printLitePacket())

    if (packet.Destination == str(config['GENERAL']['IpSink'])):
        #print ("Yess - è per me")
        # print("######## ", packet.TTL)
        if(int(packet.Type) == 0):
            TypeBeacon(packet)
        if(int(packet.Type) == 1):
            TypeReport(packet)
        if(int(packet.Type) == 2):
            TypeData(packet)
        if(int(packet.Type) == 3):
            TypeFunction(packet)
    else:
        #print("NO - non è per me")
        packet.DecreaseTTL()
        #print("@@@@@@@ ", packet.TTL)
        data = packet.getBytesFromPackets()
        UDP_Socket.SendUdpPacketUnicast(
            data, node_variables.IpDefaultGateway, int(config['GENERAL']['Port']))


def TypeBeacon(packet):

    
    if (packet.Destination==str(config['GENERAL']['IpSink']) and init_config.GetIp(config['GENERAL']['StationInterface'])==str(config['GENERAL']['IpSink']) ):
        data = packet.getBytesFromPackets()
        #Packets.getPacketFromBytes(data).printLitePacket()
        print("Beacon Received from: ", packet.Source)
        UDP_Socket.SendUdpPacketUnicast(data, config['GENERAL']['IpController'], int(config['GENERAL']['PortController']))
    


def TypeReport(packet):
    if (packet.Destination==str(config['GENERAL']['IpSink'])and init_config.GetIp(config['GENERAL']['StationInterface'])==str(config['GENERAL']['IpSink'])):
        print("Report Received from: ", packet.Source)
        data = packet.getBytesFromPackets()
        UDP_Socket.SendUdpPacketUnicast(data, config['GENERAL']['IpController'], int(config['GENERAL']['PortController']))


def TypeData(packet):
    if (packet.Destination==str(config['GENERAL']['IpSink'])and init_config.GetIp(config['GENERAL']['StationInterface'])==str(config['GENERAL']['IpSink'])):
        print("Data Received from: ", packet.Source)
        data = packet.getBytesFromPackets()
        UDP_Socket.SendUdpPacketUnicast(data, config['GENERAL']['IpController'], int(config['GENERAL']['PortController']))


def TypeFunction(packet):
    if (packet.NextHop==str(config['GENERAL']['IpSinkOnWan']) and init_config.GetIp(config['GENERAL']['StationWanInterface'])==str(config['GENERAL']['IpSinkOnWan'])):
        print("Function PKT Received from: ", packet.Source)
        data = packet.getBytesFromPackets()
        UDP_Socket.SendUdpPacketUnicast(data, packet.Destination, int(config['GENERAL']['Port']))
    if (packet.Destination == init_config.GetIp(config['GENERAL']['StationInterface'])):
        GetAudio()




def UpdateNeighborList(ip):
    if (FindIpInTheNeighborList(ip) == 0):
        node_variables.list_neighbor.append(ip)


def FindIpInTheNeighborList(ip):
    return ip in node_variables.list_neighbor


def SendReportToSink(packet):
    print(packet.TTL)

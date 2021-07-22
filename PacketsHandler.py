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
from Packets import DataPacket

# verifco se il pacchetto è per me o no


def PacketHandler(data, address):
    packet = Packets.getPacketFromBytes(data)
    if config['DEBUG']['PRINT_LOGS'] is True:
        print(packet.printLitePacket())
    if config['DEBUG']['PRINT_LOGS'] is True:
        print("--->", init_config.GetIp(config['GENERAL']['StationInterface']))

    if (packet.Destination == init_config.GetIp(
            config['GENERAL']['StationInterface'])):
        #print ("Yess - è per me")
        # print("######## ", packet.TTL)
        if (int(packet.Type) == 0):
            TypeBeacon(packet)
        if (int(packet.Type) == 1):
            TypeReport(packet)
        if (int(packet.Type) == 2):
            TypeData(packet, packet.Source)
        if (int(packet.Type) == 3):
            TypeFunction(packet)
    #else:
    #print("NO - non è per me")
    # packet.DecreaseTTL()
    #print("@@@@@@@ ", packet.TTL)
    # data = packet.getBytesFromPackets()
    # UDP_Socket.SendUdpPacketUnicast(
    #data, node_variables.IpDefaultGateway, int(config['GENERAL']['Port']))
    if (packet.NextHop == str(config['GENERAL']['IpSinkOnWan'])
            and init_config.GetIp(config['GENERAL']['StationInterface'])
            == str(config['GENERAL']['IpSink'])):
        if (int(packet.Type) == 3):
            TypeFunction(packet)


def TypeBeacon(packet):

    if (packet.Destination == str(config['GENERAL']['IpSink'])
            and init_config.GetIp(config['GENERAL']['StationInterface'])
            == str(config['GENERAL']['IpSink'])):

        #Packets.getPacketFromBytes(data).printLitePacket()
        if config['DEBUG']['PRINT_LOGS'] is True:
            print("Beacon Received from: ", packet.Source)
        data = packet.getBytesFromPackets()
        UDP_Socket.SendUdpPacketUnicast(
            data, config['GENERAL']['IpController'],
            int(config['GENERAL']['PortController']))


def TypeReport(packet):
    if (packet.Destination == str(config['GENERAL']['IpSink'])
            and init_config.GetIp(config['GENERAL']['StationInterface'])
            == str(config['GENERAL']['IpSink'])):
        if config['DEBUG']['PRINT_LOGS'] is True:
            print("Report Received from: ", packet.Source)
        data = packet.getBytesFromPackets()
        UDP_Socket.SendUdpPacketUnicast(
            data, config['GENERAL']['IpController'],
            int(config['GENERAL']['PortController']))


def TypeData(packet, s):
    #if (packet.Destination==str(config['GENERAL']['IpSink'])and init_config.GetIp(config['GENERAL']['StationInterface'])==str(config['GENERAL']['IpSink'])): no
    if config['DEBUG']['PRINT_LOGS'] is True:
        print("Data Received from: ", s)
    pckData = DataPacket(config['GENERAL']['NetId'],
                         config['GENERAL']['IpRasp'],
                         packet.Source, "100",
                         config['GENERAL']['IpRasp'], packet.Payload)
    data = pckData.getBytesFromPackets()
    UDP_Socket.SendUdpPacketUnicast(data, config['GENERAL']['IPRasp'],
                                    int(config['GENERAL']['PortRasp']))
    if config['DEBUG']['WRITE_FILE'] is True:
        print("Saving inside the file ------->", str(packet.Source) )
        f = open("/etc/AUDIO/{}.txt".format(packet.Source), "wb") #commen
        f. write(packet.Payload) #comme
        f. close() #comm


def TypeFunction(packet):
    if config['DEBUG']['PRINT_LOGS'] is True:
        print("Sono nella TypeFunction")
    if config['DEBUG']['PRINT_LOGS'] is True:
        print("Next hop->", packet.NextHop, " vs->",
              str(config['GENERAL']['IpSinkOnWan']))
    #config['GENERAL']['StationWanInterface']
    if config['DEBUG']['PRINT_LOGS'] is True:
        print("Wan IP->", init_config.GetIp("br-lan1"), " vs->",
              str(config['GENERAL']['IpSinkOnWan']))
    if config['DEBUG']['PRINT_LOGS'] is True:
        print("packet destnation->", packet.Destination, " vs->",
              init_config.GetIp(config['GENERAL']['StationInterface']))
    if (packet.NextHop == str(config['GENERAL']['IpSinkOnWan'])
            and init_config.GetIp("br-lan1") == str(
                config['GENERAL']['IpSinkOnWan'])):
        if config['DEBUG']['PRINT_LOGS'] is True:
            print("Function PKT Received from: ", packet.Source)
        dest = packet.Destination
        data = packet.getBytesFromPackets()
        if config['DEBUG']['PRINT_LOGS'] is True:
            print("Invio a, ", dest)
        UDP_Socket.SendUdpPacketUnicast(data, dest,
                                        int(config['GENERAL']['Port']))
    if (packet.Destination == init_config.GetIp(
            config['GENERAL']['StationInterface'])):
        GetAudio(packet.Payload)
        #ciao


def UpdateNeighborList(ip):
    if (FindIpInTheNeighborList(ip) == 0):
        node_variables.list_neighbor.append(ip)


def FindIpInTheNeighborList(ip):
    return ip in node_variables.list_neighbor


def SendReportToSink(packet):
    print(packet.TTL)

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

try:
    if str(init_config.GetIp(config['GENERAL']['StationInterface'])) == str(config['GENERAL']['IpSink']):
        config['GENERAL']['IPRasp']=socket.gethostbyname(config['GENERAL']['IPRasp'])
        config['GENERAL']['IpSinkOnWan']=socket.gethostbyname(config['GENERAL']['IpSinkOnWan'])
        config['GENERAL']['IpController']=socket.gethostbyname(config['GENERAL']['IpController'])
except Exception as error:
    print("PacketHandler.py Error when trying to resolve names: ", error)

def PacketHandler(data, address):
    try:
        # It tries to resolve the IP of the given name. NB if the the value is an IP it will return the IP itself
        ip_rasp=socket.gethostbyname(config['GENERAL']['IPRasp'])
        ip_sink_wan=socket.gethostbyname(config['GENERAL']['IpSinkOnWan'])
        ip_controller=socket.gethostbyname(config['GENERAL']['IpController'])
        packet = Packets.getPacketFromBytes(data)
        if config.getboolean('DEBUG','PRINT_LOGS') is True:
            print(packet.printLitePacket())
        if config.getboolean('DEBUG','PRINT_LOGS') is True:
            print("--->", init_config.GetIp(config['GENERAL']['StationInterface']))

        if (packet.Destination == init_config.GetIp(
                config['GENERAL']['StationInterface'])):
            #print ("Yess - è per me")
            # print("######## ", packet.TTL)
            if (int(packet.Type) == 0):
                TypeBeacon(packet, ip_controller)
            if (int(packet.Type) == 1):
                TypeReport(packet, ip_controller)
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
        if (packet.NextHop == str(ip_sink_wan)
                and init_config.GetIp(config['GENERAL']['StationInterface'])
                == str(config['GENERAL']['IpSink'])):
            if (int(packet.Type) == 3):
                TypeFunction(packet,ip_sink_wan)
    except Exception as e:
        print("Error in PacketHandler: ", e)


def TypeBeacon(packet, ip_controller):

    if (packet.Destination == str(config['GENERAL']['IpSink'])
            and init_config.GetIp(config['GENERAL']['StationInterface'])
            == str(config['GENERAL']['IpSink'])):

        #Packets.getPacketFromBytes(data).printLitePacket()
        if config.getboolean('DEBUG','PRINT_LOGS') is True:
            print("Beacon Received from: ", packet.Source)
        data = packet.getBytesFromPackets()
        UDP_Socket.SendUdpPacketUnicast(
            data, ip_controller,
            int(config['GENERAL']['PortController']))


def TypeReport(packet, ip_controller):
    if (packet.Destination == str(config['GENERAL']['IpSink'])
            and init_config.GetIp(config['GENERAL']['StationInterface'])
            == str(config['GENERAL']['IpSink'])):
        if config.getboolean('DEBUG','PRINT_LOGS') is True:
            print("Report Received from: ", packet.Source)
        data = packet.getBytesFromPackets()
        UDP_Socket.SendUdpPacketUnicast(
            data, ip_controller,
            int(config['GENERAL']['PortController']))


def TypeData(packet, s):
    #if (packet.Destination==str(config['GENERAL']['IpSink'])and init_config.GetIp(config['GENERAL']['StationInterface'])==str(config['GENERAL']['IpSink'])): no
    if config.getboolean('DEBUG','PRINT_LOGS') is True:
        print("Data Received from: ", s)
    pckData = DataPacket(config['GENERAL']['NetId'],
                         config['GENERAL']['IpRasp'],
                         packet.Source, "100",
                         config['GENERAL']['IpRasp'], packet.Payload)
    data = pckData.getBytesFromPackets()
    UDP_Socket.SendUdpPacketUnicast(data, config['GENERAL']['IPRasp'],
                                    int(config['GENERAL']['PortRasp']))
    if config.getboolean('DEBUG','WRITE_FILE') is True:
        print("Saving inside the file ------->", str(packet.Source) )
        f = open("/etc/AUDIO/{}.txt".format(packet.Source), "ab") #commen
        f. write(packet.Payload) #comme
        f. close() #comm


def TypeFunction(packet, ip_sink_wan):
    if config.getboolean('DEBUG','PRINT_LOGS') is True:
        print("Sono nella TypeFunction")
    if config.getboolean('DEBUG','PRINT_LOGS') is True:
        print("Next hop->", packet.NextHop, " vs->",
              str(ip_sink_wan))
    #config['GENERAL']['StationWanInterface']
    if config.getboolean('DEBUG','PRINT_LOGS') is True:
        print("Wan IP->", init_config.GetIp("br-lan1"), " vs->",
              str(ip_sink_wan))
    if config.getboolean('DEBUG','PRINT_LOGS') is True:
        print("packet destnation->", packet.Destination, " vs->",
              init_config.GetIp(config['GENERAL']['StationInterface']))
    if (packet.NextHop == str(ip_sink_wan)
            and init_config.GetIp("br-lan1") == str(
                ip_sink_wan)):
        if config.getboolean('DEBUG','PRINT_LOGS') is True:
            print("Function PKT Received from: ", packet.Source)
        dest = packet.Destination
        data = packet.getBytesFromPackets()
        if config.getboolean('DEBUG','PRINT_LOGS') is True:
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



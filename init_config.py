import subprocess
import socket
import sys
import ifaddr
import os
import time

from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')


def SetDeviceOnStart():
    temp = config.get(socket.gethostname(),'IpStation')
    os.system(f'uci set network.wlan.ipaddr={temp}')
    os.system('uci commit network')
    os.system('/etc/init.d/network restart')
    sys.stdout.flush()
    time.sleep(50)
    print("Tutto ok")

def GetIp(interface):
    adapters = ifaddr.get_adapters()

    temp = ""
    for adapter in adapters:
        if (adapter.nice_name == interface):
            temp = adapter.ips[0].ip
    
    return temp

    # addrs = netifaces.ifaddresses('br-wlan')
    # #print ( ((addrs[2])[0])['addr'] )
    # return ((addrs[2])[0])['addr']

def GetDefaultGateway(interface):
    temp = GetIp(interface)
    temp1 = temp.split(".")
    temp2 = "" + temp1[0] + "." + temp1[1] + "." + temp1[2] + "." + "1"
    #print ( temp1 , type(temp1) )
    return temp2

    # gateway = ''
    # addrs = netifaces.ifaddresses(interface)
    # print ( addrs )

    # for obj in netifaces.gateways()[2]:
    #     if ( ((obj)[0])[1] == interface ):
    #         gateway = ((obj)[0])[0]
    # return gateway
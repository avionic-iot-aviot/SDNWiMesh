import subprocess
import socket
import sys
import os
import time

from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')


def SetDeviceOnStart():
    if ( socket.gethostname() == "Omega-1D63"):
        temp = config['Omega-1D63']['IpStation']
        os.system(f'uci set network.wlan.ipaddr={temp}')
        os.system('uci commit network')
        os.system('/etc/init.d/network restart')
        sys.stdout.flush()
        time.sleep(40)
        print("Tutto ok")
    if ( socket.gethostname() == "Omega-1D06"):
        temp = config['Omega-1D06']['IpStation']
        os.system(f'uci set network.wlan.ipaddr={temp}')
        os.system('uci commit network')
        os.system('/etc/init.d/network restart')
        sys.stdout.flush()
        time.sleep(40)
        print("Tutto ok")

# def GetIps(interface):
#     addrs = netifaces.ifaddresses('br-wlan')
#     #print ( ((addrs[2])[0])['addr'] )
#     return ((addrs[2])[0])['addr']


# def GetDefaultGateway(interface):
#     gateway = ''
#     addrs = netifaces.ifaddresses(interface)
#     print ( addrs )

#     for obj in netifaces.gateways()[2]:
#         if ( ((obj)[0])[1] == interface ):
#             gateway = ((obj)[0])[0]
#     return gateway
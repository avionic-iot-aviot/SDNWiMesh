import subprocess
import socket
import sys
import os
import time
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')


def Inizio():
    if ( socket.gethostname() == "Omega-1D63"):
        temp = config['Omega-1D63']['IpStation']
        os.system(f'uci set network.wlan.ipaddr={temp}')
        os.system('uci commit network')
        os.system('/etc/init.d/network restart')
        sys.stdout.flush()
        time.sleep(5)
        print("Tutto ok")
    if ( socket.gethostname() == "Omega-1D06"):
        subprocess.call(["uci set network.wlan.ipaddr=192.168.1.1" , "uci commit network", "/etc/init.d/network restart"])
        sys.stdout.flush()
        print("Tutto ok")


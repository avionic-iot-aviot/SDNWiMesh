import subprocess
import socket
import sys
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')


def Inizio():
    if ( socket.gethostname() == "Omega-1D63"):
        # subprocess.call(["uci set network.wlan.ipaddr=192.168.0.1" , "uci commit network", "/etc/init.d/network restart"])
        subprocess.call(["pwd"])
        sys.stdout.flush()
        print("Tutto ok")
    if ( socket.gethostname() == "Omega-1D06"):
        subprocess.call(["uci set network.wlan.ipaddr=192.168.1.1" , "uci commit network", "/etc/init.d/network restart"])
        sys.stdout.flush()
        print("Tutto ok")


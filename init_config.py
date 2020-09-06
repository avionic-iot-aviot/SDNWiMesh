import subprocess
import socket
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')


def Inizio():
    if ( socket.gethostname() == "Omega-1D63"):
        subprocess.call(["uci set network.wlan.ipaddr=192.168.0.1" , "uci commit network", "/etc/init.d/network restart"])
        print("Tutto ok")
    if ( socket.gethostname() == "Omega-1D06"):
        subprocess.call(["uci set network.wlan.ipaddr=192.168.1.1" , "uci commit network", "/etc/init.d/network restart"])
        print("Tutto ok")


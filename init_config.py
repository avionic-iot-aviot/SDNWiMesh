import subprocess
import socket
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')


def Inizio():
    if ( socket.gethostname() == "Omega-1D63"):
        subprocess.call([f"uci set network.wlan.ipaddr={config['Omega-1D63']['IpStation']}" , "uci commit network", "/etc/init.d/network restart"])
        print("Tutto ok")


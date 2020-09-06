import subprocess
import socket
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')


def Inizio():
    test = "Ciao"
    if ( socket.gethostname() == "Omega-1D63"):
        subprocess.call(["echo {test}"])


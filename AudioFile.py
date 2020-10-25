import wave
import threading
import socket
import sys
import time
import PacketsHandler
from Packets import ReportPacket
from Packets import BeaconPacket
from Packets import Packets
import node_variables
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

class ThreadSendDataAudio (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting " + self.name)
        #UdpSocketReceiver( config.get(socket.gethostname(),'IpStation') , int(config['GENERAL']['Port']) )
        AudioFile()


def AudioFile():
    
    while True:
        obj = wave.open('/tmp/SDNPy-master/sound.wav', 'r')
        print("Number of channels", obj.getnchannels())
        print("Sample width", obj.getsampwidth())
        print("Frame rate.", obj.getframerate())
        print("Number of frames", obj.getnframes())
        print("parameters:", obj.getparams())
        obj.close()

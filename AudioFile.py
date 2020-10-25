import wave
import threading
import socket
import sys
import time
import PacketsHandler
import UDP_Socket
from Packets import ReportPacket
from Packets import BeaconPacket
from Packets import Packets
from Packets import DataPacket
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
        frame = 0
        for x in range(0, 2601600, 80):
            tmp = obj.readframes(int(config['FileWave']['Frame']))
            pckData = DataPacket(config.get(socket.gethostname(),'NetId'),(config['GENERAL']['IpSink']), node_variables.IpStation, "100",node_variables.IpDefaultGateway,tmp)
            UDP_Socket.SendUdpPacketUnicast(pckData.getBytesFromPackets(),node_variables.IpDefaultGateway,int(config['GENERAL']['Port']))
            frame = frame + len(tmp)
            print("Frame ["+ str(x) + "]   lette: " + str(frame))
            time.sleep(float(config['FileWave']['TimeSleepBetweenTwoFrame']))
        obj.close()
        time.sleep(int(config['FileWave']['TimeSleepBetweenTwoPlay']))

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
import init_config
from configparser import ConfigParser
import serial
config = ConfigParser()
import subprocess
config.read('config.ini')


#class ThreadSendDataAudio (threading.Thread):
 #   def __init__(self, threadID, name):
  #      threading.Thread.__init__(self)
   #     self.threadID = threadID
    #    self.name = name

    #def run(self):
     #   print("Starting " + self.name)
      #  #UdpSocketReceiver( config.get(socket.gethostname(),'IpStation') , int(config['GENERAL']['Port']) )
       # AudioFile()


def GetAudio(action):
    #time.sleep(5)
    #nodeIP = init_config.GetIp(config['GENERAL']['StationInterface'] )
    #while True:
    ser = serial.Serial('/dev/ttyS1')  # open serial port    
    print("Microphone "+action)
    if action =="ON":
        while action =="ON":
            
            payload= str(ser.readline())
            print(payload)
            print ("send mic data")
            pckData = DataPacket(config['GENERAL']['NetId'],config['GENERAL']['IpSink'], init_config.GetIp(config['GENERAL']['StationInterface']), "100",config['GENERAL']['IpSink'],payload)
            UDP_Socket.SendUdpPacketUnicast(pckData.getBytesFromPackets(),config['GENERAL']['IpSink'],int(config['GENERAL']['Port'])) 
    if action == "OFF":
        ser.close()
        subprocess.Popen("fuser -k /dev/ttyS1", shell=True, stdout=subprocess.PIPE)        
        

        #obj = wave.open('/tmp/SDNPy-master/sound.wav', 'r')
       # print("Number of channels", obj.getnchannels())
        #print("Sample width", obj.getsampwidth())
        #print("Frame rate.", obj.getframerate())
        #print("Number of frames", obj.getnframes())
        #print("parameters:", obj.getparams())
        #frame = 0
        #for x in range(0, 2601600, 80):
        #tmp = obj.readframes(int(config['FileWave']['Frame']))
        #pckData = DataPacket(config['GENERAL']['NetId'],config['GENERAL']['IpSink'], nodeIP, "100",config['GENERAL']['IpSink'],'CIAOOONE')
        #UDP_Socket.SendUdpPacketUnicast(pckData.getBytesFromPackets(),config['GENERAL']['IpSink'],int(config['GENERAL']['Port']))
        #frame = frame + len(tmp)
        #print("Frame ["+ str(x) + "]   lette: " + str(frame))
        #time.sleep(float(config['FileWave']['TimeSleepBetweenTwoFrame']))
        #obj.close()
        #time.sleep(int(config['FileWave']['TimeSleepBetweenTwoPlay']))

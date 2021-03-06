from multiprocessing import Process
import os
import subprocess
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
config.read('config.ini')
nodeIP = init_config.GetIp(config['GENERAL']['StationInterface'] )
seconds_to_wait_before_notify = 2

# class ThreadSendDataAudio (threading.Thread):
#   def __init__(self, threadID, name):
#      threading.Thread.__init__(self)
#     self.threadID = threadID
#    self.name = name

# def run(self):
#   print("Starting " + self.name)
#  #UdpSocketReceiver( config.get(socket.gethostname(),'IpStation') , int(config['GENERAL']['Port']) )
# AudioFile()


def GetAudio(action):
    # time.sleep(5)
    #nodeIP = init_config.GetIp(config['GENERAL']['StationInterface'] )
    # while True:

    if action.decode('utf-8') == "ON":
        t = ThreadAud("AudioThread", action)
        t.start()
        # audioT.join()
        print("Thread Audio Started")
        # return

    if action.decode('utf-8') == "OFF":
        #print("Microphone "+action.decode('utf-8'))
        node_variables.MicStatus = action
        #os.system("kill -SIGKILL " + str(node_variables.ThreadId))

        #obj = wave.open('/tmp/SDNPy-master/sound.wav', 'r')
    # print("Number of channels", obj.getnchannels())
    #print("Sample width", obj.getsampwidth())
    #print("Frame rate.", obj.getframerate())
    #print("Number of frames", obj.getnframes())
    #print("parameters:", obj.getparams())
    #frame = 0
    # for x in range(0, 2601600, 80):
    #tmp = obj.readframes(int(config['FileWave']['Frame']))
    #pckData = DataPacket(config['GENERAL']['NetId'],config['GENERAL']['IpSink'], nodeIP, "100",config['GENERAL']['IpSink'],'CIAOOONE')
    # UDP_Socket.SendUdpPacketUnicast(pckData.getBytesFromPackets(),config['GENERAL']['IpSink'],int(config['GENERAL']['Port']))
    #frame = frame + len(tmp)
    #print("Frame ["+ str(x) + "]   lette: " + str(frame))
    # time.sleep(float(config['FileWave']['TimeSleepBetweenTwoFrame']))
    # obj.close()
    # time.sleep(int(config['FileWave']['TimeSleepBetweenTwoPlay']))


class ThreadAud(threading.Thread):
    def __init__(self, name, action):
        threading.Thread.__init__(self)
        self.name = name
        self.action = action.decode('utf-8')

    def run(self):
        if config.getboolean('DEBUG','PRINT_LOGS') is True:
            print("CIAOOOOOOO SONO QUIIIIIIIIIII")
        node_variables.MicStatus = self.action
        if config.getboolean('DEBUG','PRINT_LOGS') is True:
            print("Avvio il Thread all'interno")
        #        ser = serial.Serial('/dev/ttyUSB1', baudrate=12000000,rtscts=True,dsrdtr=True, timeout=0)
        #        print(ser.isOpen())
        #        pos=0
        #        buffSize = 3
        #        inBuff = [bytes(0)] * buffSize
        #        messRCV = False
        #        sampleSizeRCV = False
        #        audioSample = []
        #        print("Eccomi")
        counter = 0
        #        while node_variables.MicStatus == "ON":
        #        print("Microphone " + self.action)
        audioSample = bytearray()
        total_bytes_sent = 0
        latest_notification_time = time.time()
        while node_variables.MicStatus == "ON":
            counter = counter + 1
            if counter <= 255:
                audioSample.append(counter)
            if counter > 255:
                counter = 1
                audioSample.append(counter)
            while len(audioSample) <= 1750:
                audioSample.append(0)


#                messRCV = False
#                strVal = ser.read(1)
#print(strVal)
#                if strVal == ('<').encode():
#                    while not messRCV:
#                        if pos == buffSize:  # and val == ('\r').encode():

#print("---------->", int.from_bytes(inBuff[0] + inBuff[1] + inBuff[2], "big", signed="True") )
#                            print("---------->",inBuff[0] + inBuff[1] + inBuff[2])
#                            audioSample.extend(inBuff[0] + inBuff[1] + inBuff[2])
#audioSample.append(int.from_bytes(inBuff[0] + inBuff[1] + inBuff[2], "big", signed="True"))
#                            messRCV = True
#                            pos = 0
#                            inBuff = [bytes(0)] * buffSize
#                        else:
#                            val = ser.read(1)
#                            inBuff[pos] = bytes(val)
#                            pos = pos + 1

            if config.getboolean('DEBUG','PRINT_LOGS') is True:
                print("send mic data:", str(counter))
            total_bytes_sent += len(audioSample)
            pckData = DataPacket(
                config['GENERAL']['NetId'], config['GENERAL']['IpSink'],
                init_config.GetIp(config['GENERAL']['StationInterface']),
                "100", config['GENERAL']['IpSink'], audioSample)
            # pckData="-1--38----192.168.3.1----192.168.3.1-2100----192.168.3.1"+payload
            # pckData=pckData.replace("192.168.3.1-2100",init_config.GetIp(config['GENERAL']['StationInterface'])+"-2100")
            #pckData=pckData.replace("38", str(38+len(payload)))

            UDP_Socket.SendUdpPacketUnicast(pckData.getBytesFromPackets(),
                                            config['GENERAL']['IpSink'],
                                            int(config['GENERAL']['Port']))
            now = time.time()
            if now - latest_notification_time > seconds_to_wait_before_notify:
                latest_notification_time = now
                UDP_Socket.SendUdpPacketMicStatus(int(config['GENERAL']['Port']),
                                                nodeIP,
                                                config['GENERAL']['IpSink'],
                                                "ON")
            time.sleep(0.250)
        counter = 0
        print("Total bytes sent: {}".format(total_bytes_sent))
        for i in range(5):
            time.sleep(0.1)
            UDP_Socket.SendUdpPacketMicStatus(int(config['GENERAL']['Port']),
                                                nodeIP,
                                                config['GENERAL']['IpSink'],
                                                "OFF")

        # UDP_Socket.SendUdpPacketUnicast(pckData.getBytesFromPackets(),config['GENERAL']['IpSink'],int(config['GENERAL']['Port']))

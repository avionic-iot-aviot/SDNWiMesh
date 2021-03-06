import threading
import UDP_Socket
from Packets import DataPacket
import node_variables
import init_config
from configparser import ConfigParser
import serial
from queue import Queue
import time

config = ConfigParser()
config.read('config.ini')
nodeIP = init_config.GetIp(config['GENERAL']['StationInterface'] )
q = Queue()
seconds_to_wait_before_notify = 2

def GetAudio(action):

    if action.decode('utf-8') == "ON":

        t = ThreadAud("AudioThread", action, q)
        t.start()
        print("Thread Audio Started")

    if action.decode('utf-8') == "OFF":
        print("Microphone " + action.decode('utf-8'))
        node_variables.MicStatus = action


class ThreadAud(threading.Thread):
    def __init__(self, name, action, queue):
        threading.Thread.__init__(self)
        self.name = name
        self.action = action.decode('utf-8')
        self.queue = queue

    def run(self):
        node_variables.MicStatus = self.action
        if config['DEBUG']['PRINT_LOGS'] is True:
            print("Avvio il Thread all'interno")
        buffSize = 360
        port = '/dev/ttyACM0'
        baudrate = 4000000
        audioSample = bytearray()

        ser = serial.Serial(None, baudrate, timeout = 0.1)
        ser.port = port
        ser.open()
        ser.write('start'.encode('utf-8'))
        counter_packets = 0
        print("Microphone " + self.action)

        while node_variables.MicStatus == "ON":
            bufferedData = bytearray()
            counter = 0
            while counter < 5:
                inBuff = ser.read(buffSize)
                bufferedData.extend(inBuff)
                counter += 1
            self.queue.put(bufferedData)
            #audioSample.extend(bufferedData)
            counter_packets += 1
            #print("AUDIO: ", len(inBuff))

        ser.write('stop'.encode('utf-8'))
        print("Packets sent: {}".format(counter_packets))
        for i in range(5):
            time.sleep(0.1)
            UDP_Socket.SendUdpPacketMicStatus(int(config['GENERAL']['Port']),
                                                nodeIP,
                                                config['GENERAL']['IpSink'],
                                                "OFF")
# SCRITTURA SU FILE NELLA onion
#        fHandler = open('/etc/SDNPy-SDNWiMesh/audio.bin', 'wb')
#        fHandler.write(audioSample)
#        fHandler.close()

        ser.close()


class ThreadWriter(threading.Thread):
    def __init__(self, name, queue):
        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue

    def run(self):
        latest_notification_time = time.time()
        while True:
            print("Elements in queue: {}".format(self.queue.qsize()))
            bufferedData = self.queue.get()
            
            pckData = DataPacket(
                config['GENERAL']['NetId'], config['GENERAL']['IpSink'],
                init_config.GetIp(config['GENERAL']['StationInterface']),
                "100", config['GENERAL']['IpSink'], bufferedData)

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

tw = ThreadWriter("WriterThread", q)
tw.start()





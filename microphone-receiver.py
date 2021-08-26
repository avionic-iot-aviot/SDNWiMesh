import serial
import signal
import sys

capture = True

def signal_handler(sig, frame):
    global capture
    print('You pressed Ctrl+C!')
    capture = False


signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')

buffSize = 360
port = '/dev/ttyACM0'
baudrate = 4000000

ser = serial.Serial(None, baudrate, timeout = 0.1)
ser.port = port
ser.open()
fHandler = open('/etc/SDNPy-SDNWiMesh/audio.bin', 'wb')  

while capture is True:
    ser.write('start'.encode('utf-8'))
    counter = 0
    inBuff = bytearray(buffSize)
    inBuff = ser.read(buffSize)
    fHandler.write(inBuff)
#    while counter < buffSize - 2:
#        if inBuff[counter:counter+1] ==  ('0').encode():
#            fHandler.write(inBuff[counter:counter+3])
#            #print(inBuff[counter:counter+3])
#            counter = counter + 3
#        else:
#            counter = counter + 1

ser.write('stop'.encode('utf-8'))
fHandler.close()

ser.close()








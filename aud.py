import serial

onionCode = 1

#Init buffer containing the received data
buffSize = 360


done = False
sampleSizeRCV = False
audioSample = []
counter = 0

if onionCode == 1:
    port = '/dev/ttyACM0'
else:
    port = 'COM6'
    
baudrate = 4000000
try:
    #Create serial object
    ser = serial.Serial(None,baudrate, timeout = 0.1)
    #Open serial
    ser.port = port
    ser.open()
    #Start data transmission 
    ser.write('start'.encode('utf-8'))
    #Start looking for the message
    while len(audioSample) < 60000 :
        counter = 0
        inBuff = ser.read(buffSize)
        #print("Waiting packets: ",ser.in_waiting)
        while counter < buffSize:
            if inBuff[counter:counter+1] ==  ('0').encode():
                audioSample.append(int.from_bytes(inBuff[counter+1:counter+2]+inBuff[counter+2:counter+3],"big", signed="True"))
                counter = counter + 3
            else:
                counter = counter + 1
                if counter + 2 > buffSize:
                    inBuff = bytearray(buffSize)
                    break
                        
except :
    print('Program exit !')
    
finally :
    ser.write('stop'.encode('utf-8'))
    maxTest = 0
    
    ser.reset_input_buffer()
    while sampleSizeRCV != True and maxTest < 10:
        mss = str(ser.read_until(expected= '\n'))
        index = mss.rfind("Sample sent:")
        if index == -1:
            maxTest = maxTest + 1
        else:
            sampleRCV = mss[index:len(mss)-5]
            sampleSizeRCV = True

        
    ser.close()
    #Save normalized file to text
    if onionCode == 1:
        fHandler = open('/etc/audio.txt', 'w')
    else:
        fHandler = open('C:/Users/ruben/Desktop/Test_9.txt', 'w')
        
    for line in audioSample:
        fHandler.write(str(line))
        fHandler.write("\n")
    fHandler.close()
pass

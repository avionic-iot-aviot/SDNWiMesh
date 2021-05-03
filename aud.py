import serial
# Init buffer containing the received data
buffSize = 3
inBuff = [bytes(0)] * buffSize
pos = 0

done = False
messRCV = False
sampleSizeRCV = False
audioSample = []

port = '/dev/usb1'
baudrate = 12000000
try:
    # Create serial object
    ser = serial.Serial(None, baudrate, timeout=0.1)
    # Open serial
    ser.port = port
    ser.open()
    # Start data transmission
    ser.write('start'.encode('utf-8'))
    # Start looking for the message
    while done == False:
        messRCV = False
        strVal = ser.read(1)

        if strVal == ('<').encode():
            while not messRCV:
                # If message found or buff is full stop reading and save sample

                if pos == buffSize:  # and val == ('\r').encode():

                    audioSample.append(int.from_bytes(inBuff[0] + inBuff[1] + inBuff[2], "big", signed="True"))
                    print(len(audioSample))
                    messRCV = True
                    pos = 0
                    inBuff = [bytes(0)] * buffSize

                    # ser.reset_output_buffer()
                else:
                    val = ser.read(1)
                    inBuff[pos] = bytes(val)
                    pos = pos + 1
except:
    print('Program exit !')

finally:
    ser.write('stop'.encode('utf-8'))
    maxTest = 0

    ser.reset_input_buffer()
    while sampleSizeRCV != True and maxTest < 10:
        mss = str(ser.read_until(expected='\n'))
        index = mss.rfind("Sample sent:")
        if index == -1:
            maxTest = maxTest + 1
        else:
            sampleRCV = mss[index:len(mss) - 5]
            sampleSizeRCV = True

    ser.close()
    # Save normalized file to text
    fHandler = open('C:/Users/Salvo/Desktop/Test_9.txt', 'w')
    for line in audioSample:
        fHandler.write(str(line))
        fHandler.write("\n")
    fHandler.close()
pass

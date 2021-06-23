import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write


sound = np.loadtxt(r"message.txt")


# Compute sampling time
fs = 8000                                                                     # sampling frequency
#Init time array
t = np.arange(0, len(sound)/fs, 1/fs)

    
sound_norm = [0] * len(sound)
max_val = max(abs(sound))/1

counter = 0

for val in sound:
    sound_norm[counter] = val/max_val
    counter = counter + 1
    
#Save normalized file to text
fHandler = open('message.txt', 'w')
for line in sound_norm:
    fHandler.write(str(line))
    fHandler.write("\n")
fHandler.close()

plt.plot(t, sound)
plt.show()

plt.plot(t, sound_norm)
plt.show()

write(r'output1.wav', fs, np.array(sound_norm))

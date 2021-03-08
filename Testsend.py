import subprocess
from time import sleep
while True:
    print("Invio")
    result = subprocess.Popen("echo \"my message\" > /dev/ttyS1", shell=True, stdout=subprocess.PIPE)
    s = result.stdout.read()
    s1 = s.decode('utf-8', 'ignore')
    sleep(1)

    
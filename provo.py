

import sys
import os


import subprocess

result = subprocess.run(['arp -a | awk \'{print $1,$4}\''], stdout=subprocess.PIPE)
print(result.stdout)


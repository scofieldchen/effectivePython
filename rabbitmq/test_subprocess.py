import os
import signal
import time
import subprocess


proc = subprocess.Popen("python test_script.py", shell=True)

cnt = 0
while cnt < 10:
    status = proc.poll()
    print(status)
    cnt += 1
    time.sleep(2)

proc.terminate()
print(proc.poll())
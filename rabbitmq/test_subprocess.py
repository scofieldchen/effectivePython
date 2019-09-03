import os
import signal
import time
import subprocess
import psutil


cmd = "gedit"

proc = subprocess.Popen(
    args=cmd,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

time.sleep(0.1)
res = proc.poll()  # None表示程序在运行，0表示已经完成，负数表示按信号退出
if res is None:
    print("start long-running child process")
    print("pid = %d" % proc.pid)
else:
    print("returncode: %s" % str(res))

# output, errors = proc.communicate()
# if output:
#     print(output.decode("utf8"))
# if errors:
#     print("failed to run command '%s'" % cmd)
#     print(errors.decode("utf8"))

time.sleep(5)

try:
    process = psutil.Process(proc.pid)
    print(process)
    for p in process.children(recursive=True):
        print(p)
        p.kill()
    process.kill()
except Exception as e:
    print(e)
import socket
import time
from datetime import datetime


host = "127.0.0.1"
port = 1234

with socket.socket() as s:
    s.connect((host, port))  # 客户端只需发起连接到服务器
    while True:
        msg = "%s: this is realtime data" % str(datetime.now())
        s.sendall(msg.encode("utf8"))
        time.sleep(1)
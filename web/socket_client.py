import socket
import time


host = "127.0.0.1"
port = 1234

with socket.socket() as s:
    s.connect((host, port))  # 客户端只需发起连接到服务器
    while True:
        data = s.recv(1024)
        if data:
            print(data)
        else:
            time.sleep(0.01)
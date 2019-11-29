import socket
import time


host = "127.0.0.1"
port = 1234

with socket.socket() as s:
    s.bind((host, port))  # 绑定IP和端口
    s.listen(5)  # 最多同时接收5个连接，每次只能处理一个，其余排队等待
    while True:
        conn, addr = s.accept()  # 阻塞直到有客户端连接
        with conn:
            print("get connection from %s" % str(addr))
            for i in range(10):
                msg = "num(%d)" % i
                conn.sendall(msg.encode("utf8"))
                time.sleep(1)
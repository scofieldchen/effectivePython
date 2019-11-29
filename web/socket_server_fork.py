"""
基于SocketServer构建简单的服务器，使用分叉技术实现多客户端连接
"""

from socketserver import TCPServer, ForkingMixIn, StreamRequestHandler


class Server(ForkingMixIn, TCPServer):
    pass


class Handler(StreamRequestHandler):

    def handle(self):
        addr = self.request.getpeername()
        print("get connection from %s" % str(addr))
        self.wfile.write("thank you for connection")


server = Server(("", 1234), Handler)
server.serve_forever()
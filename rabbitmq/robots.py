import os
import time
import subprocess
from queue import Queue

import pika

from config import config
from consumer import Consumer


class Signal:
    """从RMQ接收消息
    
    Attributes:
        config(dict): RMQ消费者类的配置文件
        queue(Queue): 将消息存放到队列
    """

    def __init__(self, config, queue):
        self.config = config
        self.consumer = Consumer(self.config)
        self._queue = queue

    def process_msg(self, message):
        """回调函数，处理消息的逻辑"""
        pass
    
    def consume(self):
        """消费实时消息"""

        # TO-DO: 处理处理异常？出现异常后是否重新连接？
        
        with self.consumer as c:
            c.consume(self.process_msg)
    

class Robot:
    """机器人实例"""

    def __init__(self, exchange, account, symbol, **kwargs):
        self.exchange = exchange.lower()
        self.account = account.lower()
        self.symbol = symbol.replace("/", "").lower()

        self.id = "_".join([self.exchange, self.account, self.symbol])
        self.alive = False
        self.pid = None

        self.params = kwargs

    def __str__(self):
        return "Robot(%s)" % self.id

    def __eq__(self, other):
        return self.id == other.id

    def is_alive(self):
        return self.alive

    def start(self, script):
        print("start child process")
        proc = subprocess.Popen(["python", script])
        cnt = 0
        while cnt < 10:
            print("return code: %s" % str(proc.returncode))
            print("child process id: %d" % proc.pid)
            time.sleep(1)
            cnt += 1
        print("stop child process")
        proc.terminate()
        print("return code: %s" % str(proc.returncode))

    def stop(self):
        pass


robot1 = Robot("fcoin", "test123", "ETH/USDT")
robot2 = Robot("instantex", "test456", "ETH/USDT")
robot3 = Robot("fcoin", "test456", "ETH/BTC")

robots = [robot1, robot2, robot3]

robot1.start("test_script.py")
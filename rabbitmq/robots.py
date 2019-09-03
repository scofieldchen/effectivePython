import os
import signal
import subprocess
import time
import json
from queue import Queue
from pprint import pprint

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
        self._consumer = Consumer(self.config)
        self._queue = queue

    def process_msg(self, message):
        """回调函数，处理消息的逻辑"""
        data = json.loads(message)
        pprint(data)
        self._queue.put(data)
    
    def consume(self):
        """消费实时消息"""

        # TO-DO: 处理处理异常？出现异常后是否重新连接？
        
        with self._consumer as consumer:
            consumer.consume(self.process_msg)


# _queue = Queue()
# signal = Signal(config, _queue)
# signal.consume()


class Robot:
    """机器人实例"""

    def __init__(self, exchange, account, symbol, **kwargs):
        self.exchange = exchange.lower()
        self.account = account.lower()
        self.symbol = symbol.replace("/", "").lower()
        self.params = kwargs

        self.id = "_".join([self.exchange, self.account, self.symbol])
        self.pid = None

    def __str__(self):
        return "Robot(%s)" % self.id

    def __eq__(self, other):
        return self.id == other.id

    def is_alive(self):
        """检查子进程是否在运行
        Popen.poll返回错误的结果，为了正确识别子进程是否在运行，用终端命令
        'ps -p $pid'实现，如果返回结果，确定进程在运行，否则已经终止
        """
        if self.pid is None:
            return False
        else:
            cmd = ["ps", "-p", str(self.pid)]
            res = subprocess.run(cmd, stdout=subprocess.PIPE)
            stdout = res.stdout.decode("utf8")
            if str(self.pid) in stdout:
                return True
            else:
                return False

    def start(self, cmd):
        """启动机器人
        
        Args:
            cmd(str): 终端命令
        """
        # 将os.setsid()传递给preexec_fn，把shell ID作为整个进程组的父ID
        # 这样一来就能把所有子进程全部关闭
        proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
        self.pid = proc.pid  # 不管Popen是否成功，都会返回pid
        time.sleep(0.2)
        if self.is_alive():
            print("robot is running, pid = %d" % self.pid)
        else:
            print("failed to start robot")

    def stop(self):
        """关闭机器人"""
        try:
            os.killpg(os.getpgid(self.pid), signal.SIGTERM)
        except Exception as e:
            print("failed to terminate robot, error = %s" % e)
        else:
            self.pid = None


robot1 = Robot("fcoin", "test123", "ETH/USDT")
# robot2 = Robot("instantex", "test456", "ETH/USDT")
# robot3 = Robot("fcoin", "test456", "ETH/BTC")
# robots = [robot1, robot2, robot3]

robot1.start("python test_script.py")

cnt = 0
while cnt < 30:
    print("robot running: ", robot1.is_alive())
    cnt += 1
    time.sleep(1)

print("terminate robot")
robot1.stop()
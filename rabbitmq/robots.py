import os
import signal
import subprocess
import time
import json
from threading import Thread
from queue import Queue
from pprint import pprint
import logging

import pika

from config import config
from consumer import Consumer


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s"
)


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
        """回调函数，处理消息的逻辑
        
        message的格式定义为:{
            "action": 'start' or 'stop',
            "exchange": 'exchangeName',
            "account": 'accountName',
            "symbol": 'AAA/BBB',
            "params": {
                "param1": 'value',
                ...
                "paramk": 'value'
            }
        }
        """
        data = json.loads(message)
        try:
            action = data["action"]
            robot = Robot(
                exchange=data["exchange"],
                account=data["account"],
                symbol=data["symbol"],
                params=data["params"]
            )
            self._queue.put((action, robot))
        except Exception as e:
            logging.error("failed to get message, error = %s" % e)
    
    def consume(self):
        """消费实时消息"""
        with self._consumer as consumer:
            consumer.consume(self.process_msg)


class Robot:
    """机器人实例"""

    def __init__(self, exchange, account, symbol, params={}):
        self.exchange = exchange.lower()
        self.account = account.lower()
        self.symbol = symbol.replace("/", "").lower()
        self.params = params

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
        
        TODO: 设置环境和工作目录

        Args:
            cmd(str): 终端命令
        
        Returns:
            bool: True表示成功启动，False表示启动失败
        """
        # 将os.setsid()传递给preexec_fn，把shell ID作为整个进程组的父ID
        # 这样一来就能把所有子进程全部关闭
        proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
        self.pid = proc.pid  # 不管Popen是否成功，都会返回pid
        time.sleep(0.2)
        if self.is_alive():
            return True
        else:
            return False

    def stop(self):
        """关闭机器人"""
        try:
            os.killpg(os.getpgid(self.pid), signal.SIGTERM)
        except Exception as e:
            logging.error(e)
            return False
        else:
            return True


class RobotManagement:
    """管理所有机器人实例"""

    def __init__(self):
        self._queue = Queue()
        self._signal = Signal(config, self._queue)
        self.signals = []  # 推送的最新信号
        self.robots = []  # 正在运行的机器人实例

    def recieve_signals(self):
        """从队列中取出信号"""
        cnt = 0
        while not self._queue.empty():
            signal = self._queue.get()
            self.signals.append(signal)
            cnt += 1
        logging.info("recieve %d signals" % cnt)
    
    def handle_signals(self):
        """根据信号启动/关闭机器人"""
        for action, robot in self.signals:
            if action == "start":  # 启动机器人
                if robot in self.robots:  # 已经启动
                    logging.info("%s: already running" % str(robot))
                else:  # 未启动
                    res = robot.start("python test_script.py")
                    if res:
                        logging.info("%s: start running" % str(robot))
                        self.robots.append(robot)
            else:  # 关闭机器人
                for bot in self.robots:
                    if bot == robot:  # 已经启动
                        res = bot.stop()
                        if res:
                            logging.info("%s: stop running" % str(bot))
                            self.robots.remove(bot)
                            break
                else:
                    logging.info("%s: robot not running, invalid stop signal" % \
                        str(robot))
        self.signals.clear()

    def check_robots(self):
        """检查机器人运行状态"""
        pass

    def run(self, interval=1):
        """主程序"""
        # 在子线程中监听信号
        t = Thread(target=self._signal.consume)
        t.start()
        time.sleep(1)

        # 在主线程中管理机器人
        while True:
            self.recieve_signals()
            self.handle_signals()
            print(self.robots)
            time.sleep(interval)


if __name__ == "__main__":
    rm = RobotManagement()
    rm.run(interval=1)
import time
import json
import random

import pika

from config import config
from publisher import Publisher


## 机器人参数
actions = ["start", "stop"]
exchanges = ["fcoin", "instantex", "mxc"]
accounts = ["abc", "123456", "kkk"]
symbols = ["ETH/USDT", "BTC/USDT", "ETH/BTC"]
param1 = [1, 2, 3, 4, 5]
param2 = [6, 7, 8, 9, 10]

## 发送消息，内容随机，模拟用户请求的过程
p = Publisher(config)
while True:
    time.sleep(random.randint(2, 10))
    request = {
        "action": random.sample(actions, k=1)[0],
        "exchange": random.sample(exchanges, k=1)[0],
        "account": random.sample(accounts, k=1)[0],
        "symbols": random.sample(symbols, k=1)[0],
        "param1": random.sample(param1, k=1)[0],
        "param2": random.sample(param2, k=1)[0]
    }
    msg = json.dumps(request)
    p.publish(msg)
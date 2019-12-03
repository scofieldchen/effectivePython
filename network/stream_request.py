"""
流式请求(stream request): 有的接口返回值包含多个结果，而不是常规的一个结果，
这时可以使用流式请求技术。

就结果而言，stream request类似于websocket.
"""

import json
import requests


# 请求时设置stream=True，这样requests不会一次性下载请求的结果
resp = requests.get('http://httpbin.org/stream/20', stream=True)

# 调用response.iter_lines()，返回生成器，迭代以获得每一条数据
for line in resp.iter_lines():
    if line:
        data = json.loads(line.decode("utf8"))
        print(data)
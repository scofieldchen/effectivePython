"""
异步核心概念

https://cheat.readthedocs.io/en/latest/python/asyncio.html
https://medium.com/python-pandemonium/asyncio-coroutine-patterns-beyond-await-a6121486656f
https://medium.com/@yeraydiazdiaz/asyncio-coroutine-patterns-errors-and-cancellation-3bb422e961ff
https://hackernoon.com/asyncio-for-the-working-python-developer-5c468e6e2e8e

1. 阻塞 vs 非阻塞IO

IO指input/ouput任务，例如数据库读写，请求web api等。

以请求API为例，发送请求后需要等待服务器响应，等待时间从几百毫秒到几秒不等，
在等待过程中CPU无法处理其它任务，这就是阻塞IO。

非阻塞IO即绕过这个等待时间，发送请求后不等待响应，直接处理下一个任务，
直到前一个请求得到回复，才回过头来处理响应结果。

2. 协程(coroutine)

协程是能够主动停止和启动的函数，由async/await关键字定义。async def定义
协程函数，await等待协程返回结果，等待的过程可理解为：先处理其它任务，等到
该协程返回结果再尽可能快地处理。

一个程序可以创建数千个协程，这就需要一个统筹所有协程的“任务调度中心”，
asyncio提供了统一的接口，称为“事件环(event loop)”.

3. async/await

async --> 定义协程函数
await --> 暂停协程的执行，把控制权交给事件环

4. 事件环(event loop)

asyncio的事件环负责调度所有的可等待对象，包括协程(coroutine),任务(task),未来(future).

在asyncio中执行异步程序的权威实现是'asyncio.run(main())'，run会创建并管理事件环，
main()是顶级协程(top-level coroutine)，是很多子协程的集合。

5. 任务(task)

task是装饰协程的对象，'装饰'可理解为将很多协程组合在一起，例如在请求API的过程中，先创建
两个协程，一个负责请求，另一个负责解析，然后创建一个任务，把两个协程结合起来，负责完整的
数据获取。

创建一个task相当于告诉事件环，只要没有其它协程在工作，马上执行该任务。

6. 可等待对象(awaitable)

coroutine,task,future都是可等待对象，意味着它们都可以被'await'。

asyncio提供了批量创建任务的接口，asyncio.gather(*awaitables)，返回一个可等待对象。
"""

import sys
import asyncio  
import aiohttp  
import json
import datetime


async def get_json(client, url):
    # 定义协程函数
    async with client.get(url) as response:  # 等待结果返回，等价于resp = await client.get(url)
        assert response.status == 200
        return await response.read()


async def get_reddit_top(subreddit, client, numposts):
    # 装饰get_json协程，对结果进行解析，chained coroutines
    data = await get_json(client, 'https://www.reddit.com/r/' + 
        subreddit + '/top.json?sort=top&t=day&limit=' +
        str(numposts))

    print(f'\n/r/{subreddit}:')

    j = json.loads(data.decode('utf-8'))
    for i in j['data']['children']:
        score = i['data']['score']
        title = i['data']['title']
        link = i['data']['url']
        print('\t' + str(score) + ': ' + title + '\n\t\t(' + link + ')')

async def main():
    # 顶级协程(top-level coroutine)，收集所有任务，提交给事件环
    print(datetime.datetime.now().strftime("%A, %B %d, %I:%M %p"))
    print('---------------------------')
    loop = asyncio.get_running_loop()
    async with aiohttp.ClientSession(loop=loop) as client:
        # gather负责收集收集所有任务，也可以用asyncio.create_task()
        await asyncio.gather(
            get_reddit_top('python', client, 3),
            get_reddit_top('programming', client, 4),
            get_reddit_top('asyncio', client, 2),
            get_reddit_top('dailyprogrammer', client, 1)
        )

# asyncio.run负责创建和运行事件环，这是最简单也是最权威的实现方式
asyncio.run(main())
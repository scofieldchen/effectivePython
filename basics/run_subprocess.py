"""
用subprocess调用python脚本

subprocess是在python代码中启动其它进程的工具，主要用途包括执行终端命令行操作，如'ls -l'，
也可以启动其它程序，包括启动和关闭python脚本。

subprocess库提供3大类接口：run(), call(), Popen()。run()和call()是高级接口，基于
Popen()实现，run()已经实现了call()的所有功能，适合操作简单的子进程，如果要实现
复杂的功能，则调用Popen()。

Popen函数接收的重要参数：

1. args: 要执行的命令
2. shell: 是否在新的shell中执行命令，一般设置为False
3. stdout/stderr，是否与子进程通信，如果传入None，默认不接收任何子进程的输出，若父进程要和
    子进程通信，必须传递参数'subprocess.PIPE'，通过管道进行交互
4. env/cwd：环境和工作目录，如果要启动复杂的python脚本，必须准确设置环境和目录

调用Popen启动子进程，返回Popen对象。

Popen对象的重要属性：

1. proc.pid，子进程的进程ID
2. proc.returncode，状态码
    None：子进程尚未结束
    0: 子进程整场退出
    >0: 子进程异常退出
    <0: 子进程被信号杀死
3. proc.stdout, proc.stderr，如果调用Popen函数时stdout,stderr参数的值是subprocess.PIPE，
    则属性是类似file的可读文件

Popen对象的重要方法：

1. proc.poll()  检查子进程是否终止，返回returncode
2. proc.wait()  阻碍主线程直到子进程结束
3. proc.communicate()  与子进程交互，proc.communicate(input=None)从父进程向子进程传输数据，
    返回一个元组(stdout, stderr)，分别包含子进程的标准输出和标准错误输出。
    父进程和子进程通过管道交互数据，在调用Popen函数时，务必指定stdin,stdout,stderr参数的值
    为subprocess.PIPE，否则communicate将不返回任何结果。
4. proc.terminate()  终止子进程，等于向子进程传送SIGTERM信号。
5. proc.kill()  杀死子进程，等于向子进程发送SIGKILL信号。

注意：proc.wait(), proc.communicate()会阻塞主线程，直到子进程运行结束。
"""


import subprocess
import time
import os
import signal


def start(cmd, cwd=None):
    """启动python脚本"""
    pid = None
    
    try:
        proc = subprocess.Popen(
            args=cmd, cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except Exception as e:
        print(e)
    else:
        time.sleep(0.5)  # 等待程序响应
        # proc.wait()  # 阻碍主线程，直到子进程结束，适合于debug长久运行的python脚本
        returncode = proc.poll()
        if returncode is None:
            pid = proc.pid
            print("subprocess is running, pid=%d" % pid)
        else:
            print("subprocess exit, exit code=%d" % returncode)
            stdout, stderr = proc.communicate()
            print(stdout.decode("utf8"))
            print(stderr.decode("utf8"))
    
    return pid


def stop(pid):
    try:
        os.kill(pid, signal.SIGTERM)
    except Exception as e:
        print(e)


cmd = ["python", "sample.py", "cmd_xoxo_test_lgcusdt"]
# cwd = "/home/scofield/marketmaking"
cwd = None

pid = start(cmd, cwd)

time.sleep(15)

if pid is not None:
    stop(pid)
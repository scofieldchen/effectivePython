# coding = utf8

"""
Python处理异常的范式是try,except,else,finally，每一个部分都有独特的作用，
善用不同的组合能高效的处理编程问题。
"""

## try + finally
## 不管try的代码是否有异常，finally都会执行，在处理IO任务时尤其有用
import sqlite3

con = sqlite3.connect("test.db")
c = con.cursor()
try:
    c.execute("select * from some_table;")  # 查询异常
finally:
    con.close()  # 不管查询是否成功都会关闭数据库连接


## try + except + else
## 这个组合能够清晰的区分哪些异常会被处理，哪些异常会传播，except会处理
## try部分代码的异常，但不会处理else代码的异常
d = {"numerator":2.0,"denominator":0}
try:
    a = d["numerator"]  # 可能引发KeyError
    b = d["denominator"]
except KeyError as e:
    print(e)
else:
    print(a / b)  # KeyError以外的异常


## try + except + else + finally
## try：主任务
## except：处理最有可能出现的异常
## else：在try成功后运行，往往用于区分无法被预测的异常
## finally: 善后工作
import sqlite3

try:
    con = sqlite3.connect("test.db")  # 可能引发IO异常
    c = con.cursor()
    c.execute("DROP TABLE IF EXISTS info;")  # 可能引发数据库操作异常
    c.execute("CREATE TABLE info(name TEXT, age INT);")
    c.execute("INSERT INTO info(name,age) VALUES('bob',25);")
    c.execute("INSERT INTO info(name,age) VALUES('alice',28);")
    c.execute("INSERT INTO info(name,age) VALUES('kobe',32);")
    con.commit()  # 若修改数据库需提交记录
except Exception as err:
    print(err)
else:
    c.execute("SELECT * FROM info;")
    all_rows = c.fetchall()
    print(all_rows)
finally:
    con.close()


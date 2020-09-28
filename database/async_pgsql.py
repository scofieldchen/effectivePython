import asyncio
import datetime as dt
from pprint import pprint
from typing import Any, Dict, List, Tuple

import asyncpg


def generate_sql(tblname: str, data: Dict[str, Any]) -> Tuple[str, Tuple[Any, ...]]:
    """创建插入数据的sql语句
    
    Args:
        tblname(str): 数据表
        data(dict): 要插入的数据，键表示字段，值是要插入的行
    
    Returns:
        (sql, (val1, val2, val3, ...))
        sql是字符串，(val1, val2 ...)是要插入的数据，两个元素同时传递给
        conn.execute(sql, *args), asyncpg会自动处理类型转换
    """
    fields = ",".join(list(data.keys()))
    values = tuple(data.values())
    placeholders = ",".join([f"${i + 1}" for i in range(len(data))])
    sql = f"INSERT INTO {tblname}({fields}) VALUES({placeholders});"
    return sql, values


# data = {
#     "name": "kobe",
#     "age": 25,
#     "income": 999.3,
#     "register": dt.datetime(2020, 9, 2, 15)
# }
# sql, values = generate_sql("users", data)
# print(sql)
# print(values)


async def main():
    """测试asyncpg基本操作"""
    # 创建连接
    dsn = "postgresql://scofield:kingchen1990@localhost:5432/test"
    conn = await asyncpg.connect(dsn)

    # 创建表
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            name text,
            age int,
            income float,
            register timestamp without time zone
        );
    """)

    # 插入数据
    await conn.execute("""
        INSERT INTO users(name, age, income, register)
        VALUES('kobe', 25, 18000.50, '2020-05-15 15:00:00');
    """)

    # 插入数据，输入为字典（常见模式），将参数传递给sql
    data = {
        "name": "bob",
        "age": 15,
        "income": 999.3,
        "register": dt.datetime(2020, 9, 2, 15)
    }
    sql, values = generate_sql("users", data)
    await conn.execute(sql, *values)

    # 查询数据
    results = await conn.fetch("SELECT * FROM users;")
    pprint(results)

    # 删除表
    await conn.execute("DROP TABLE users;")

    # 关闭连接
    await conn.close()


asyncio.run(main())

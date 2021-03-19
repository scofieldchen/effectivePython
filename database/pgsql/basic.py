from contextlib import contextmanager

import psycopg2
from psycopg2.extensions import cursor as Cursor


############################ 连接字符串 ############################
DSN = "postgresql://test:test@localhost:5432/test"


############################ 连接数据库 ############################

# 使用psycopg2的第一步是连接数据库
# 交互前需要先创建connection和cursor对象
# 使用connection和cursor的两个原则：
#   1. 需要时再创建，不要一直打开连接，用户必须明智地管理资源对象的生命周期
#   2. 将管理connection的逻辑与操作数据(CRUD)的逻辑相分离

# 这里使用自定义函数(上下文管理器)获取并管理connection和cursor对象,
# 包括打开连接, 提交更改/回滚, 捕捉异常, 关闭连接等

@contextmanager
def db_session(dsn: str):
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    try:
        yield cur  # with db_session(dsn) as session ==> 将cursor赋值给session
        conn.commit()  # 若无异常, 提交更改
    except Exception as e:
        conn.rollback()  # 出现异常先回滚, 再主动引发异常, CRUD函数不需要处理异常
        raise e
    finally:
        cur.close()  # 不管操作是否成功, 最终关闭连接, 释放资源
        conn.close()


############################ 数据库模式 ############################

# 数据库模式: database schemas
# 模式可以理解为表, 表字段和表关系的集合

def drop_users_table(db: Cursor):
    db.execute("DROP TABLE IF EXISTS users;")


def create_users_table(db: Cursor):
    sql = """
    CREATE TABLE IF NOT EXISTS users(
        id serial PRIMARY KEY,
        name VARCHAR(50),
        age INT
    )
    """
    db.execute(sql)


def check_table(db: Cursor, table_name: str) -> bool:
    sql = """
    SELECT EXISTS (
        SELECT * FROM information_schema.tables
        WHERE table_name = %s
    );
    """
    db.execute(sql, (table_name, ))
    return db.fetchone()[0]


print("Create users table")
with db_session(DSN) as db:
    drop_users_table(db)
    create_users_table(db)
    res = check_table(db, "users")
    print(f"Table exists: {res}")


############################ CRUD: 插入数据 ############################

# 如何将参数传递给sql?
#   1. 在sql中使用'%s'作为占位符, cursor.execute(sql, args: Tuple[..., Any]), 用元组传递参数
#   2. 在sql中使用'%(name)s'作为占位符, cursor.execute(sql, args: Dict[str, Any]), 用字典传递参数
# 要点: 不管要传递什么类型的数据, 占位符的格式永远是'%s', psycopg2会自动进行数据结构转换

## 插入一条数据, 用元组传递参数
one_user = ("kobe", 25)
with db_session(DSN) as db:
    db.execute("INSERT INTO users(name, age) VALUES(%s, %s);", one_user)

## 插入多条数据, 用字典传递参数
# 执行多条sql语句时应该使用cursor.executemany(sql, args_list)
# 注意一点, executemany等价于循环调用execute, 处理大数据时没有优势
# 为了提高性能, 批量插入多行数据应使用execute_batch或者pgsql COPY
many_users = [
    {"name": "alice", "age": 18},
    {"name": "bob", "age": 19},
    {"name": "tracy", "age": 28}
]

with db_session(DSN) as db:
    db.executemany("INSERT INTO users(name, age) VALUES(%(name)s, %(age)s)", many_users)


############################ CRUD: 查询数据 ############################

# 如何查询数据?
# cursor.execute(select_statement) => cursor.fetch*() => 清洗和整理数据
# fetchone() -> 返回一行或None
# fetchmany() -> 返回指定长度的行
# fetchall() -> 返回全部行或空列表

# cursor对象本身也是可迭代对象
# cursor.fetchall() == [record for record in cursor] 

with db_session(DSN) as db:
    # 返回一条记录
    db.execute("SELECT * FROM users")
    record = db.fetchone()  # 若没有记录,返回None
    print(record)

    # 返回全部记录
    db.execute("SELECT * FROM users")
    records = db.fetchall()  # 若没有记录, 返回空列表
    print(records)


############################ CRUD: 更新数据 ############################

with db_session(DSN) as db:
    db.execute("""
    UPDATE users
    SET age = 9999
    WHERE name = 'kobe';
    """)

    db.execute("SELECT * FROM users ORDER BY id;")
    records = db.fetchall()
    print(records)


############################ CRUD: 删除数据 ############################

with db_session(DSN) as db:
    db.execute("""
    DELETE FROM users
    WHERE name = 'kobe';
    """)

    db.execute("SELECT * FROM users ORDER BY id;")
    records = db.fetchall()
    print(records)

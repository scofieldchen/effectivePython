"""
ORM: Object Relational Mapping

用自定义类映射数据库表：
1. 类 ==> 数据库表
2. 类实例 ==> 表行记录
3. 类属性 ==> 字段
"""
from sqlalchemy import (Column, Integer, Sequence, String, and_, create_engine,
                        desc, or_)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

################################### 数据库引擎 ###################################

# 使用sqlalchemy的第一步是创建数据库引擎
# 数据库引擎可理解为管理连接的高阶对象，但engine并不会打开具体的连接
# engine.execute(sql) --> 执行SQL语句
# engine.connect() --> 返回connection对象
engine = create_engine("postgresql://scofield:test@localhost:5432/test")

################################### 数据库模型 ###################################

# 创建数据库模型，即ORM模型，将自定义类映射到数据表
# 自定义类必须继承Base基类，同时定义表名，字段名和字段类型

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("users_id_seq"), primary_key=True)
    name = Column(String(50))
    age = Column(Integer)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, age={self.age})>"

################################### 数据库模式 ###################################

# 数据库模式(database schema)：可理解为表，表字段，表关系的集合
# MetaData对象是数据库模式的抽象
# 调用MetaData对象的方法可以初始化/重置数据库

Base.metadata.drop_all(engine)  # 删除所有表
Base.metadata.create_all(engine)  # 创建所有表，若表已存在则忽略

################################### 会话 ###################################

# 创建Session对象，Session对象实例封装具体的连接
Session = sessionmaker(bind=engine)
session = Session()

################################### 添加数据 ###################################

# 添加一行
one_row = Users(name="tracy", age=26)
session.add(one_row)

# 添加多行
rows = [
    Users(name="kobe", age=18),
    Users(name="alice", age=25),
    Users(name="bob", age=16)
]
session.add_all(rows)
session.commit()

# 检查是否成功
print("Add users to table")
print("="*30)
for user in  session.query(Users).order_by(Users.id).all():
    print(user)
print("="*30, "\n")

################################### 更改数据 ###################################

user_kobe = session.query(Users).filter(Users.name == "kobe").first()
user_kobe.name = "KOBE"
session.add(user_kobe)
session.commit()

# 检查是否成功
print("Update table row")
print("="*30)
for user in  session.query(Users).order_by(Users.id).all():
    print(user)
print("="*30, "\n")

################################### 查询数据 ###################################

# session.query() ==> 创建Query对象，可链式调用order_by, filter等方法，实现筛选和排序
# Query.first() ==> 返回匹配的第一行，无匹配返回None
# Query.all() ==> 返回全部行

# 查询整张表
print("Read the whole table")
results = session.query(Users).all()
print("="*30)
for res in results:
    print(res)
print("="*30, "\n")

# 选择部分字段
print("Select partial fields")
print("="*30)
for name, age in session.query(Users.name, Users.age).all():
    print(name, age)
print("="*30, "\n")

# 按某个字段升序排序
print("Order rows in ascending order")
print("="*30)
for res in session.query(Users).order_by(Users.age).all():
    print(res)
print("="*30, "\n")

# 按某个字段降序排列
print("Order rows in descending order")
print("="*30)
for res in session.query(Users).order_by(desc(Users.age)).all():
    print(res)
print("="*30, "\n")

# 限制返回的行数，LIMIT
print("Limit returned rows")
print("="*30)
for res in session.query(Users).order_by(Users.id).all()[:3]:
    print(res)
print("="*30, "\n")

# 筛选行，恒等于：==
print("Filter rows: ==")
print("="*30)
for res in session.query(Users).filter(Users.name == "alice").all():
    print(res)
print("="*30, "\n")

print("Filter rows: !=")
print("="*30)
for res in session.query(Users).filter(Users.name != "alice").all():
    print(res)
print("="*30, "\n")

print("Filter rows: >=")
print("="*30)
for res in session.query(Users).filter(Users.age >= 20).all():
    print(res)
print("="*30, "\n")

print("Filter rows: and")
print("="*30)
for res in session.query(Users).filter(and_(Users.name == "alice", Users.age == 25)).all():
    print(res)
print("="*30, "\n")

print("Filter rows: or")
print("="*30)
for res in session.query(Users).filter(or_(Users.name == "alice", Users.name == "bob")).all():
    print(res)
print("="*30, "\n")

print("Filter rows: in")
print("="*30)
for res in session.query(Users).filter(Users.name.in_(["alice", "bob"])).all():
    print(res)
print("="*30, "\n")

print("Filter rows: not in")
print("="*30)
for res in session.query(Users).filter(Users.name.notin_(["alice", "bob"])).all():
    print(res)
print("="*30, "\n")

print("Filter rows: like")
print("="*30)
for res in session.query(Users).filter(Users.name.like("a%")).all():
    print(res)
print("="*30, "\n")

################################### 删除数据 ###################################

session.query(Users).filter(Users.name == "alice").delete()
session.commit()

# 检查结果是否成功
print("Delete rows")
print("="*30)
for res in session.query(Users).order_by(Users.id).all():
    print(res)
print("="*30, "\n")


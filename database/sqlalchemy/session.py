"""
如何管理session的生命周期？

Sqlalchemy要求先创建engine和Session, 然后创建再Session类的实例，负责处理具体的连接。
session实例有自己的生命周期：connect -> commit/rollback -> close，为了正确管理
数据库资源，需要遵循以下两个原则：

1. 在需要与数据库交互时(增删改查)再创建session.
2. 将session管理与增删改查的实现逻辑相分离。
"""
from contextlib import contextmanager

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建数据库引擎和全局Session类
engine = create_engine("postgresql://scofield:test@localhost:5432/test")
Session = sessionmaker(bind=engine)

# 数据库模型
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    age = Column(Integer)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, age={self.age})>"


# 初始化数据库
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


# 管理session实例的生命周期，与操作数据的逻辑相分离
# contextmanager装饰器将db_session()转化为上下文管理器
# 被装饰的函数必须要使用yield，这里返回session实例
# 当调用with db_session() as db，yield session会把session赋值给db
@contextmanager
def db_session():
    session = Session()
    try:
        print("Get session object")
        yield session  # 必须使用yield返回资源对象
        print("Commit changes")
        session.commit()  # 完成数据操作后提交更改
    except Exception as e:
        print("Catch exception and rollback")
        # 由db_session()统一管理数据库异常，操作数据时不需要处理
        # 先回滚，再主动引发异常，由外层程序处理
        session.rollback()
        raise e
    finally:
        print("Close connection")
        session.close()  # 操作完毕后关闭连接，释放资源


# 操作数据的业务逻辑
def create_user(db: Session):
    user = {
        "name": "kobe",
        "age": 25
    }
    db.add(User(**user))

def read_user(db: Session):
    users = db.query(User).all()
    print(users)


# 在上下文管理器中使用session
with db_session() as session:
    create_user(session)
    read_user(session)

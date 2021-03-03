"""
数据表关系

常见的数据表关系：一对一，一对多，多对一，多对多

最常见的关系是一对多(包含多对一和一对一)。所谓一对多，即某张表的一条记录对应或包含
另一张表的多条记录。例如在电商系统中，一个客户可以拥有多条订单记录；在比赛系统中，
一只队伍可以包含多名球员。

以球类博彩为例，假设两张表：Games, Bets。Games存储投注比赛的数据，Bets存储投注的数据。
一场比赛包含多笔投注(一对多), 一笔投注对应一场比赛(一对一)。在两张表间建立连接，实现
合并查询。

建立数据表关系的目标：简化合并查询。即从一个数据库模型直接获取另一个模型的数据。
"""
from pprint import pprint

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.schema import ForeignKey


# 创建连接引擎和会话对象
engine = create_engine("postgresql://scofield:test@localhost:5432/test")
Session = sessionmaker(bind=engine)
session = Session()


# 数据库模型
Base = declarative_base()

class Games(Base):
    """比赛数据，一场比赛包含很多投注"""
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, autoincrement=True)
    home = Column(String(50))
    away = Column(String(50))
    winner = Column(Integer)

    def __repr__(self):
        return f"<Game(id={self.id}, home={self.home}, away={self.away}, winner={self.winner})>"

class Bets(Base):
    """投注数据，一笔投注对应一场比赛"""
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 定义外键(ForeignKey)
    # 外键可以理解为两张表之间的连接纽带
    # 一笔投注对应一场比赛，我们可以将Bets.game_id连接到Games.id
    # 从Bets表的角度来讲，投注和比赛的关系是"一对一"
    # 从Games表的角度来讲，比赛的投注的关系是"一对多"
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    player_name = Column(String(50))
    bet_team = Column(Integer)
    bet_amount = Column(Integer)

    # 定义relationship，关系是外键的补充，sqlalchemy要求同时定义两者，才能完全连接表
    # 注意，relationship()函数第一个参数是数据库模型(自定义类)的名称，而不是表名
    # 当在Bets模型中定义relationship后，可以直接从bets表访问games表，例如bet.games.winner
    # 但这种关系是单向的，为了实现双向关系，要使用backref参数，这样就可以从games表获取bets数据，例如game.bets
    games = relationship("Games", backref="bets")

    def __repr__(self):
        return f"<Bet(id={self.id}, player_name={self.player_name}, bet_team={self.bet_team}, bet_amount={self.bet_amount})>"


# 创建数据库模式
Base.metadata.drop_all(engine)  # 先重置数据库，test only
Base.metadata.create_all(engine)  # 创建所有表


# 录入比赛和投注数据
data_games = [
    {"home": "lakers", "away": "rockets", "winner": 1},
    {"home": "celtics", "away": "wolf", "winner": 2}
]
data_bets = [
    # 比赛1包含3个投注
    {"game_id": 1, "player_name": "kobe", "bet_team": 1, "bet_amount": 20},
    {"game_id": 1, "player_name": "alice", "bet_team": 2, "bet_amount": 100},
    {"game_id": 1, "player_name": "bob", "bet_team": 1, "bet_amount": 55},
    # 比赛2包含2个投注
    {"game_id": 2, "player_name": "king", "bet_team": 1, "bet_amount": 20},
    {"game_id": 2, "player_name": "tracy", "bet_team": 2, "bet_amount": 80}
]

games = [Games(**item) for item in data_games]
bets = [Bets(**item) for item in data_bets]
session.add_all(games)
session.add_all(bets)
session.commit()


# 查询数据
# 定义数据库关系的主要目标是实现合并查询(JOINS)，即从一个数据库模型直接获取另一个模型的数据

# 查询比赛1的数据，并列出比赛1包含的所有投注
game = session.query(Games).filter(Games.id == 1).first()
print(game)
pprint(game.bets)

# 查询投注数据，并获取该笔投注对应的比赛信息
bet = session.query(Bets).filter(Bets.player_name == "kobe").first()
print(bet)
print(bet.games)

# JOIN查询
bets = session.query(Bets).join(Games, Games.id == Bets.game_id).all()
for bet in bets:
    print({
        "player_name": bet.player_name,
        "bet_amount": bet.bet_amount,
        "bet_team": bet.bet_team,
        "home": bet.games.home,
        "away": bet.games.away,
        "winner": bet.games.winner
    })

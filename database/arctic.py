"""
什么是Arctic?

Arctic是专门存储时间序列的数据库，建立在mongodb基础之上，能够和python pandas完美兼容。

为什么使用Arctic?

1. 将pandas dataframe/series, numpy ndarray等数据结构进行序列化(转化为二进制文件)。
2. 自动使用LZ4技术压缩数据，节约存储空间。
3. 存储大型数据框时自动实现分段存储(chunking)。
4. 提供3种不同类型的存储引擎(storage engine)：
    1. VersionStore: 管理数据版本，类似于git
    2. TickStore: 处理流数据
    3. ChunkStore: 分段存储大型数据

教程：
https://github.com/manahl/arctic
https://arctic.readthedocs.io/en/latest/
https://github.com/manahl/arctic/blob/master/docs/versionstore.md
"""


from arctic import Arctic
import pandas as pd

# 连接到mongodb
store = Arctic("localhost")

# 数据存储到图书馆(libraries)，每个用户拥有1个或多个libraries
store.list_libraries()

# 创建library，默认使用VersionStore，lib_type参数可指定特定的存储引擎
store.initialize_library("NASDAQ")

# 获得library
library = store["NASDAQ"]

# 查看library包含的symbols，类似于查看数据库包含哪些表格(tables)
library.list_symbols()

# 删除symbol
# library.delete("SYMBOL")

# 存储数据到library
# 写入数据的基础方法是library.write，默认替换该symbol的所有数据，接收以下参数：
# symbol: 数据的唯一ID，类似于表格的概念，用于存储和读取数据
# data: 被存储的数据，一般是pandas.DataFrame，numpy.ndarray或其它python结构，如字典
# metadata: 元数据，必须是字典，例如说明数据源等重要信息
# prune_previous_version: bool，是否删除之前版本的数据
dates = pd.date_range(start="2019-01-01", periods=5)
df = pd.DataFrame({
    "price": list(range(5)),
    "amount": list(range(5))
}, index=dates)
library.write("SYMBOL", df, metadata={"source": "test"})

# 从library中读取数据
# 读取数据的基础方法是library.read，接收以下参数：
# symbol: 数据的唯一ID
# as_of: 筛选条件，根据特定时间戳/版本号提取数据
# date_range: 提取样本，提供一个元组，如('2018-01-01','2019-01-01')
# 返回对象包含核心数据(data)，版本号(version)和元数据(metadata)
item = library.read("SYMBOL")
print(item.data)
print(item.metadata)

# 提取指定样本的数据
# 该方法只适用于时间序列数据框，即存入的数据是包含TimeIndex的DataFrame
from arctic.date import DateRange
library.read("SYMBOL", date_range=DateRange('2019-01-01', '2019-01-03')).data

# 往library中插入数据
# 调用library.append方法，接收以下参数：
# symbol: 数据的唯一ID
# data: 待插入的数据，一般是数据框
# metadata: 元数据
# prune_previous_version: 是否删除之前版本的数据
# upsert: bool, 若设为True，在symbol未被创建的情况下插入数据前会先创建symbol,False则会报错
df2 = pd.DataFrame({
    "price": list(range(3)),
    "amount": list(range(3))
}, index=pd.date_range(start="2019-01-06", periods=3))
library.append("SYMBOL", df2, upsert=True)


"""
python如何处理时区？
"""

import datetime as dt
import pytz


# python程序员通常用datetime库处理日期/时间，但dt创建的日期对象不明确时区，
# 最好的策略是创建一个明确时区的日期对象，默认使用UTC即可
d = dt.datetime(2019, 6, 6, 12, 0, 0)  # 不明确时区
print(d)

# 方法1：创建日期对象时指定时区
d_utc = dt.datetime(2019, 6, 6, 12, 0, 0, tzinfo=pytz.utc)
print(d_utc)

# 方法2：先创建时区对象，再调用localize方法
tz = pytz.timezone("UTC")
d_utc2 = tz.localize(d)
print(d_utc2)

d_utc == d_utc2

# 转换到其它时区
d_beijing = d_utc.astimezone(pytz.timezone("Asia/Shanghai"))  # 北京时间
d_newyork = d_utc.astimezone(pytz.timezone("America/New_York"))  # 纽约时间
print(d_beijing)
print(d_newyork)

# 如何找到目标地区的时区信息？
# pytz.country_timezones字典提供了快速查找的方法，只需提供国家简码(ISO 3166)即可
print(pytz.country_timezones["CN"])  # 中国
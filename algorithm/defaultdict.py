"""
当使用字典时，如果value使用list,set,dict，可以使用collections.defaultdict，
它会初始化value的数据结构，只需往里边填充值即可。
"""

from collections import defaultdict
from pprint import pprint


d = defaultdict(list)  # 初始化value的格式为list

for k in ["a", "b", "c"]:
    for i in range(10):
        d[k].append(i)  # 直接调用append方法

pprint(d)
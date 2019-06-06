"""
当序列(list,set,str)包含重复出现的元素，有时想统计它们的频率(count/frequency),
这在数据分析中处理分类变量时尤其有用，可使用collections.Counter对象。
"""

from collections import Counter

s = [
    "A", "A", "A",
    "B", "B",
    "C", "C", "C", "C",
    "D",
    "E", "E"
]

# 创建Counter实例，自动把输入序列映射为"item":"count"格式
word_counts = Counter(s)
print(word_counts)

# 调用most_common方法，输出出现次数最多的元素
top_two = word_counts.most_common(2)
print(top_two)

# Counter实例本质上是字典，可根据key找到对应频数
word_counts["A"]

# 若查找不存在的key，输出零而不会报错
word_counts["F"]

# Counter支持更新频数统计表
more_words = ["A", "B", "E"]
word_counts.update(more_words)
print(word_counts)

"""
使用collections.Counter统计序列(list,str)中重复出现元素的频数。
"""

from collections import Counter


## 统计列表元素重复出现的次数

words_list = [
    "A", "A", "A",
    "B", "B",
    "C", "C", "C", "C",
    "D",
    "E", "E"
]

# 创建Counter实例，自动把输入序列映射为"item":"count"格式
word_counter = Counter(words_list)
print(word_counter)

# 调用most_common()，返回出现次数最多的元素
print(word_counter.most_common(2))

# Counter实例本质上是字典，可根据key找到对应频数
print(word_counter["A"])

# 若查找不存在的key，输出零而不会报错
print(word_counter["F"])

# Counter支持更新频数统计表
more_words = ["A", "B", "E"]
word_counter.update(more_words)
print(word_counter)


## 字符串

words = "acacadwadeqamkaicvanjnadca"
words_counter = Counter(words)
print(words_counter)
print(words_counter.most_common(2))
print(words_counter["a"])
import re


########################## re.match ##########################

# 给定filepath, 提取bucketName, blobName
text = "gs://bucket_name/path/to/your/file.csv"

# 正则表达式，用普通字符和特殊字符表示匹配模式
regex = "gs://(.+?)/(.+)"

# 编译正则表达式，创建模式对象
pattern = re.compile(regex, re.IGNORECASE)

# 调用模式对象的match方法
# 若匹配成功，返回匹配对象，若无匹配内容，返回None
result = pattern.match(text)

# 获取匹配内容
print(result.group())      # 返回匹配的完整字符串
print(result.groups())     # 返回匹配的所有子组
print(result.start())      # 返回匹配的开始位置
print(result.end())        # 返回匹配的结束位置
print(result.span())       # 返回包含(start, end)的原则

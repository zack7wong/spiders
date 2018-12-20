import os
import re
result = {}

print('当前目录有以下文件：')
for file in os.listdir("."):
    if file.endswith(".py"):
        py = open(file).read().splitlines()
        total_count = len(py)
        blank_count = py.count("")
        comment_count = 0
        for line in py:
            comment_single_count = len(re.findall(r"^(\s*)#",line))
            comment_count += comment_single_count
        print(file +'总行数有：'+str(len(py))+' 空行有：'+str(blank_count)+' 注释有：'+str(comment_count))
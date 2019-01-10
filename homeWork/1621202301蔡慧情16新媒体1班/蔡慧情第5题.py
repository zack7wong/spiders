#1621202301 蔡慧情 16新媒体1班  第5题 2018年12月18日 15:23

import re
mystring = input('请输入字符串：')

zimu=0
num=0
kongge=0
qita=0
for res in mystring:
    if re.search('[a-zA-Z]',res):
        zimu +=1
    elif re.search('[0-9]',res):
        num +=1
    elif res == ' ':
        kongge +=1
    else:
        qita+=1

print(mystring)
print('字母有：'+str(zimu)+'个')
print('数字有：'+str(num)+'个')
print('空格有：'+str(kongge)+'个')
print('其他有：'+str(qita)+'个')
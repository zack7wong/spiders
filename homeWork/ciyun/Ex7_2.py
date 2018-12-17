#Ex7_2.py
import matplotlib.pyplot as plt
import numpy as np
#数据读取
datals = []
f = open("SH600000.txt")#打开文件
for line in f:#将文件数据提取
    line = line.replace("\n","")#换行变为空格
    datals.append(list(line.split("\t")))
f.close()
datals = np.array(datals)

fig = plt.figure()
#设置中文显示模式
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

for i in range(6):
    ax1 = fig.add_subplot(6,1,i+1)#标题
    ax1.plot(list(map(eval,datals[1:,i+1])))#读取列表
    max_indx = np.argmax(list(map(eval,datals[1:,i+1])))
    min_indx = np.argmin(list(map(eval, datals[1:, i + 1])))
    plt.plot(max_indx, list(map(eval,datals[1:,i+1]))[max_indx], 'ks')
    plt.plot(min_indx, list(map(eval,datals[1:,i+1]))[min_indx], 'gs')
    ax1.set_ylabel(datals[0,i+1])#y轴

plt.show()


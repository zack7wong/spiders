#1621202301 蔡慧情 16新媒体1班  第3题 2018年12月18日 15:03

item_list = []
with open('ok.txt') as f:
    results = f.readlines()
    for res in results:
        item_list.append(res.strip())

print(item_list)
item_list = sorted(item_list)
print(item_list)
for res in item_list:
    with open('ok_asc.txt','a') as f:
        f.write(res+'\n')
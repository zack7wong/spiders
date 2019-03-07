
# var path = [
#         [116.203046,39.894641],
#         [116.20356,39.894641],
#         [116.203604,39.893388],
#         [116.20362,39.892784],
#         [116.203611,39.89213],
#         [116.203418,39.892143],
#         [116.203046,39.894641],
#     ]

item_list = []
with open('结果_高德.txt') as f:
    results = f.readlines()
    for res in results:
        if res == '\n':
            continue
        item_list.append(res.strip())

num=0
for item in item_list:
    splitRes = item.split(';')
    saveStr = 'var path'+str(num)+' = ['
    for res in splitRes:
        # lng = res.split('，')[0]
        # lat = res.split('，')[1]
        thisStr = '['+res.replace('，',',')+'],'
        saveStr += thisStr
    saveStr+=']'
    print(saveStr)
    num+=1
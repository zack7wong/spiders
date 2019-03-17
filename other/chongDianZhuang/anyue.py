import requests
import json

url = "http://app.anyocharging.com:8981/api/v2/station/station/get"

payload = "id=10332"
headers = {
    'Authorization': "Basic QU5EUk9JRC5hbnlvLmNvbTo5YWJiYTkxOWMyOTMzYWI3NjFiYzFjZTFkZDM3Y2I5Mg==",
    'r': "1552745029974",
    'SESSIONID': "",
    'User-Agent': "Mozilla/5.0 (Linux; U; Android 6.0; zh-cn; Redmi Note 4 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36",
    'VERSIONID': "3.8.1",
    'Accept-Language': "zh-CN,zh;q=0.8",
    'UUID': "",
    'Content-Type': "application/x-www-form-urlencoded",
    'Host': "app.anyocharging.com:8981",
    'Accept-Encoding': "gzip",
    'Connection': "keep-alive",
    'cache-control': "no-cache",
    'Postman-Token': "20a270c2-545e-4c1d-817c-a8928b707586"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)

# 名称,地址,直流桩总数，交流桩总数,运行商,直流平均费用,交流平均费用,各时段充电费用,各时段服务费用,停车费用,经度,纬度

json_obj = json.loads(response.text)
id = json_obj['data']['id']
name = json_obj['data']['name']
address = json_obj['data']['address']
zhiliu = str(json_obj['data']['dc_cnt'])
jiaoliu = str(json_obj['data']['ac_cnt'])
yunyingshang = json_obj['data']['provider']

dc_costfee = json_obj['data']['dc_costfee']
ac_costfee = json_obj['data']['ac_costfee']

dianfenStrList = []
for each in json_obj['data']['elec_cost_detail']:
    dianfenStrList.append(str(each))

dianfenStr = '--'.join(dianfenStrList)
serve_fee = json_obj['data']['serve_fee']
parking_desc = json_obj['data']['parking_desc']
longitude = json_obj['data']['longitude']
latitude = json_obj['data']['latitude']

save_res = name + '||' + address + '||' + zhiliu + '||' + jiaoliu + '||' + yunyingshang + '||' + dc_costfee + '||' + ac_costfee + '||' + dianfenStr + '||' + serve_fee + '||' + parking_desc + '||' + longitude+'||'+latitude
save_res = save_res.replace(',', '，').replace('\n', '').replace('\r', '').replace('\t', '').replace('||',',').strip() + '\n'
print(save_res)
# with open('星星充电.csv', 'a', encoding='gbk') as f:
#     f.write(save_res)




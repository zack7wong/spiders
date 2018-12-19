#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     qiwen
   Description :
   Author :        hayden_huang
   Date：          2018/11/30 19:50
-------------------------------------------------
"""

import requests
import time
from lxml.etree import HTML

headers = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'accept-encoding':'gzip, deflate, br',
'accept-language':'zh-CN,zh;q=0.9',
'cache-control':'no-cache',
'cookie':'cityPy_expire=1543665094; Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2=1543578705; UM_distinctid=16764767684676-01212373df9155-35627600-1fa400-16764767685243; cityPy=beijing; Hm_lpvt_ab6a683aa97a52202eab5b3a9042a8d2=1543632792',
'pragma':'no-cache',
'upgrade-insecure-requests':'1',
'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}

URL = 'https://lishi.tianqi.com/{city}/{date}.html'
year_list = ['2015','2016','2017','2018']
month_list = ['01','02','03','04','05','06','07','08','09','10','11','12']
city_name = ['qinhuangdao','xingtai','chengde','cangzhou','bengbu','maanshan','tongling','anqing','qiqihaer','tieling','chaoyang','huludao','siping','anyang','xinxiang','jiaozuo','huangshi','luzhou','deyang','chaozhou','chifeng','yingkou','lanzhou','wulumuqi','zhengzhou','changsha','guiyang','kunming','beijing','xuchang','handan','taiyuan','dalian','xuzhou','hangzhou','fuzhou','weifang','jian','wuzhong','liaoyuan','nantong','shaoxing','wuhu','jingdezhen','weihai','huanggang','changde','panzhihua','zunyi','yanan','jiayuguan']
city_zhongwen = ['秦皇岛','邢台','承德','沧州','蚌埠','马鞍山','铜陵','安庆','齐齐哈尔','铁岭','朝阳','葫芦岛','四平','安阳','新乡','焦作','黄石','泸州','德阳','潮州','赤峰','营口','兰州','乌鲁木齐','郑州','长沙','贵阳','昆明','北京','许昌','邯郸','太原','大连','徐州','杭州','福州','潍坊','吉安','吴忠','辽源','南通','绍兴','芜湖','景德镇','威海','黄冈','常德','攀枝花','遵义','延安','嘉峪关']
city_keyvalue = [{'value': '秦皇岛', 'key': 'qinhuangdao'}, {'value': '邢台', 'key': 'xingtai'}, {'value': '承德', 'key': 'chengde'}, {'value': '沧州', 'key': 'cangzhou'}, {'value': '蚌埠', 'key': 'bengbu'}, {'value': '马鞍山', 'key': 'maanshan'}, {'value': '铜陵', 'key': 'tongling'}, {'value': '安庆', 'key': 'anqing'}, {'value': '齐齐哈尔', 'key': 'qiqihaer'}, {'value': '铁岭', 'key': 'tieling'}, {'value': '朝阳', 'key': 'chaoyang'}, {'value': '葫芦岛', 'key': 'huludao'}, {'value': '四平', 'key': 'siping'}, {'value': '安阳', 'key': 'anyang'}, {'value': '新乡', 'key': 'xinxiang'}, {'value': '焦作', 'key': 'jiaozuo'}, {'value': '黄石', 'key': 'huangshi'}, {'value': '泸州', 'key': 'luzhou'}, {'value': '德阳', 'key': 'deyang'}, {'value': '潮州', 'key': 'chaozhou'}, {'value': '赤峰', 'key': 'chifeng'}, {'value': '营口', 'key': 'yingkou'}, {'value': '兰州', 'key': 'lanzhou'}, {'value': '乌鲁木齐', 'key': 'wulumuqi'}, {'value': '郑州', 'key': 'zhengzhou'}, {'value': '长沙', 'key': 'changsha'}, {'value': '贵阳', 'key': 'guiyang'}, {'value': '昆明', 'key': 'kunming'}, {'value': '北京', 'key': 'beijing'}, {'value': '许昌', 'key': 'xuchang'}, {'value': '邯郸', 'key': 'handan'}, {'value': '太原', 'key': 'taiyuan'}, {'value': '大连', 'key': 'dalian'}, {'value': '徐州', 'key': 'xuzhou'}, {'value': '杭州', 'key': 'hangzhou'}, {'value': '福州', 'key': 'fuzhou'}, {'value': '潍坊', 'key': 'weifang'}, {'value': '吉安', 'key': 'jian'}, {'value': '吴忠', 'key': 'wuzhong'}, {'value': '辽源', 'key': 'liaoyuan'}, {'value': '南通', 'key': 'nantong'}, {'value': '绍兴', 'key': 'shaoxing'}, {'value': '芜湖', 'key': 'wuhu'}, {'value': '景德镇', 'key': 'jingdezhen'}, {'value': '威海', 'key': 'weihai'}, {'value': '黄冈', 'key': 'huanggang'}, {'value': '常德', 'key': 'changde'}, {'value': '攀枝花', 'key': 'panzhihua'}, {'value': '遵义', 'key': 'zunyi'}, {'value': '延安', 'key': 'yanan'}, {'value': '嘉峪关', 'key': 'jiayuguan'}]

for year in year_list:
    for month in month_list:
        for city in city_name:
            start_url = URL.format(city=city,date=year+month)
            print(start_url)
            response = requests.get(start_url,headers=headers)
            html = HTML(response.text)
            date_list = html.xpath('//div[@class="tqtongji2"]/ul/li/a/text()')
            zuidi_list = html.xpath('//div[@class="tqtongji2"]/ul/li[2]/text()')[1:]
            zuigao_list = html.xpath('//div[@class="tqtongji2"]/ul/li[3]/text()')[1:]
            tianqi_list = html.xpath('//div[@class="tqtongji2"]/ul/li[4]/text()')[1:]
            # fengxiang_list = html.xpath('//div[@class="tqtongji2"]/ul/li[5]/text()')[1:]
            fengli_list = html.xpath('//div[@class="tqtongji2"]/ul/li[6]/text()')[1:]

            print(date_list)
            for i in city_keyvalue:
                if city == i['key']:
                    thiscity = i['value']
                    break

            for date,zuidi,zuigao,tianqi,fengli in zip(date_list,zuidi_list,zuigao_list,tianqi_list,fengli_list):
                rain = '0'
                snow = '0'
                if '雨' in tianqi:
                    rain = '1'

                if '雪' in tianqi:
                    snow = '1'
                with open('qiwen.csv', 'a') as f:
                    save_res = thiscity+','+date+','+zuidi+','+zuigao+','+rain+','+snow+','+fengli+'\n'
                    f.write(save_res)


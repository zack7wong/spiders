#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
import json
import time


url = 'https://landing-sb.prdasbb18a1.com/zh-cn/Service/CentralService?GetData&ts=1545453959656'
headers = {
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "418",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    # 'Cookie': "ASP.NET_SessionId=pvwij1oh0yzjrfa0d5jy4um5; mc=; HighlightedSport=; sb188cashlv=1025510410.20480.0000; _ga=GA1.2.611347971.1545364960; _gid=GA1.2.1579228103.1545364960; settingProfile=OddsType=2&NoOfLinePerEvent=1&SortBy=1&AutoRefreshBetslip=True; fav3=; CCDefaultMbPlay=eventId%3D2931219%26lsId%3D%26aTeamName%3D%E8%BE%BE%E6%8B%89%E6%96%AF%E7%8B%AC%E8%A1%8C%E4%BE%A0%26hTeamName%3D%E6%B4%9B%E6%9D%89%E7%9F%B6%E5%BF%AB%E8%88%B9%26sportId%3D2%26lang%3Dzh-cn%26vidoProvider%3Dp%26lcid%3D2931219%26lcpid%3D1%26ilup%3Dtrue; timeZone=480; CCEnlargeStatus=true; CCDefaultBgPlay=eventId%3D2935071%26lsId%3D%26aTeamName%3D%E5%9D%8E%E6%96%AF%E5%A4%A7%E7%8F%AD%26hTeamName%3D%E9%98%BF%E5%BE%B7%E8%8E%B1%E5%BE%B736%E4%BA%BA%26sportId%3D2%26lang%3Dzh-cn%26vidoProvider%3Dp%26lcid%3D2935071%26lcpid%3D1%26ilup%3Dtrue; CCCurrentMbPlay=eventId%3D2935071%26lsId%3D%26aTeamName%3D%E5%9D%8E%E6%96%AF%E5%A4%A7%E7%8F%AD%26hTeamName%3D%E9%98%BF%E5%BE%B7%E8%8E%B1%E5%BE%B736%E4%BA%BA%26sportId%3D2%26lang%3Dzh-cn%26vidoProvider%3Dp%26lcid%3D2935071%26lcpid%3D1%26ilup%3Dtrue",
    'Host': "landing-sb.prdasbb18a1.com",
    'Origin': "https://landing-sb.prdasbb18a1.com",
    'Pragma': "no-cache",
    'Referer': "https://landing-sb.prdasbb18a1.com/zh-cn/sports/all/in-play",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
}
body = 'IsFirstLoad=true&VersionL=-1&VersionU=0&VersionS=-1&VersionF=-1&VersionH=1%3A0%2C2%3A0%2C13%3A0%2C14%3A0%2C18%3A0%2C21%3A0%2C23%3A0%2C25%3A0%2C26%3A0&VersionT=-1&IsEventMenu=false&SportID=1&CompetitionID=-1&reqUrl=%2Fzh-cn%2Fsports%2Fall%2Fin-play&oIsInplayAll=false&oVersion=2%2C50181%7C23%2C4468%7C1%2C54744%7C18%2C2039&oIsFirstLoad=false&oSortBy=1&oOddsType=0&oPageNo=0&LiveCenterEventId=2935071&LiveCenterSportId=2'

def get_res():
    response = requests.post(url, headers=headers, data=body)
    json_obj = json.loads(response.text)
    # res = json_obj['mod']['d'][0]['data']['d']['c'][0]['e'][0]['o']['ou']
    # print(len(json_obj['mod']['d'][0]['data']['d']['c'][0]['e']))
    print(json.dumps(json_obj['mod']['d']))
    for diqu in json_obj['mod']['d']:
        if 'd' in diqu['data']:
            if 'c' in diqu['data']['d']:
                for bisai in diqu['data']['d']['c']:
                    tyepName = bisai['n']
                    print('\n' + tyepName)
                    for data in bisai['e']:
                        print('==============\n')
                        name1 = data['i'][0]
                        name2 = data['i'][1]

                        # 1x2
                        onetwo_res_list = []
                        if '1x2' in data['o']:
                            print('1x2')
                            onetwo = data['o']['1x2']
                            print(onetwo)
                            for i in range(0, len(data['o']['1x2']), 6):
                                obj = {
                                    'key': '1x2',
                                    'value': [data['o']['1x2'][i + 1], data['o']['1x2'][i + 3], data['o']['1x2'][i + 5]]
                                }
                                onetwo_res_list.append(obj)
                        print(onetwo_res_list)

                        # 全场让球   让盘
                        rangqiu_res_list = []
                        if 'ah' in data['o']:
                            print('全场让球')
                            rangqiu = data['o']['ah']
                            print(rangqiu)
                            for i in range(0, len(data['o']['ah']), 8):
                                obj = {
                                    'key': 'rangqiu',
                                    'value': [data['o']['ah'][i + 1], data['o']['ah'][i + 3], data['o']['ah'][i + 5],
                                              data['o']['ah'][i + 7]]
                                }
                                rangqiu_res_list.append(obj)
                        print(rangqiu_res_list)

                        # 大小
                        daxiao_res_list = []
                        if 'ou' in data['o']:
                            print('大小')
                            daxiao = data['o']['ou']
                            print(daxiao)
                            for i in range(0, len(data['o']['ou']), 8):
                                obj = {
                                    'key': 'daxiao',
                                    'value': [data['o']['ou'][i + 1], data['o']['ou'][i + 3], data['o']['ou'][i + 5],
                                              data['o']['ou'][i + 7]]
                                }
                                daxiao_res_list.append(obj)
                        print(daxiao_res_list)

                        max_len = len(onetwo_res_list)
                        if len(rangqiu_res_list) > max_len:
                            max_len = len(rangqiu_res_list)
                        if len(daxiao_res_list) > max_len:
                            max_len = len(daxiao_res_list)

                        if len(onetwo_res_list) < max_len:
                            for i in range(len(onetwo_res_list), max_len):
                                onetwo_res_list.append({'key': '1x2', 'value': ['', '', '']})

                        if len(rangqiu_res_list) < max_len:
                            for i in range(len(rangqiu_res_list), max_len):
                                rangqiu_res_list.append({'key': 'rangqiu', 'value': ['', '', '', '']})

                        if len(daxiao_res_list) < max_len:
                            for i in range(len(daxiao_res_list), max_len):
                                daxiao_res_list.append({'key': 'daxiao', 'value': ['', '', '', '']})

                        print(onetwo_res_list)
                        print(rangqiu_res_list)
                        print(daxiao_res_list)

                        for onetwo, rangqiu, daxiao in zip(onetwo_res_list, rangqiu_res_list, daxiao_res_list):
                            save_res1 = name1 + ',' + onetwo['value'][0] + ',' + rangqiu['value'][0] + ',' + \
                                        rangqiu['value'][2] + ',' + daxiao['value'][0] + ',' + daxiao['value'][2] + '\n'
                            save_res2 = name2 + ',' + onetwo['value'][1] + ',' + rangqiu['value'][1] + ',' + \
                                        rangqiu['value'][3] + ',' + daxiao['value'][1] + ',' + daxiao['value'][3] + '\n'
                            print(save_res1)
                            print(save_res2)
                            with open('res.csv', 'a') as f:
                                f.write(save_res1)
                                f.write(save_res2)

                        ############### #后面不同类型的比赛 #########################

                        # 独赢盘 #数据是按序号的，不是全放一起
                        duyingpan_res_list = []
                        if 'ml' in data['o']:
                            ml = data['o']['ml']
                            print('独赢盘')
                            print(ml)
                            for i in range(0, len(data['o']['ml']), 4):
                                obj = {
                                    'key': 'ml',
                                    'value': [data['o']['ml'][i + 1], data['o']['ml'][i + 3]]
                                }
                                duyingpan_res_list.append(obj)
                        print(duyingpan_res_list)

                        # 让分
                        rangfen_res_list = []
                        if 'ahpt' in data['o']:
                            ahpt = data['o']['ahpt']
                            print('让分')
                            print(ahpt)
                            for i in range(0, len(data['o']['ahpt']), 8):
                                obj = {
                                    'key': 'ahpt',
                                    'value': [data['o']['ahpt'][i + 1], data['o']['ahpt'][i + 3],
                                              data['o']['ahpt'][i + 5], data['o']['ahpt'][i + 7]]
                                }
                                rangfen_res_list.append(obj)
                        print(rangfen_res_list)

                        # #分数-大/小
                        fenshu_res_list = []
                        if 'oupt' in data['o']:
                            oupt = data['o']['oupt']
                            print('分数-大/小')
                            print(oupt)
                            for i in range(0, len(data['o']['oupt']), 8):
                                obj = {
                                    'key': 'oupt',
                                    'value': [data['o']['oupt'][i + 1], data['o']['oupt'][i + 3],
                                              data['o']['oupt'][i + 5], data['o']['oupt'][i + 7]]
                                }
                                fenshu_res_list.append(obj)
                        print(fenshu_res_list)

                        # 处理填充
                        max_len = len(duyingpan_res_list)
                        if len(rangfen_res_list) > max_len:
                            max_len = len(rangfen_res_list)
                        if len(fenshu_res_list) > max_len:
                            max_len = len(fenshu_res_list)

                        if len(duyingpan_res_list) < max_len:
                            for i in range(len(duyingpan_res_list), max_len):
                                duyingpan_res_list.append({'key': 'ml', 'value': ['', '']})

                        if len(rangfen_res_list) < max_len:
                            for i in range(len(rangfen_res_list), max_len):
                                rangfen_res_list.append({'key': 'ahpt', 'value': ['', '', '', '']})

                        if len(fenshu_res_list) < max_len:
                            for i in range(len(fenshu_res_list), max_len):
                                fenshu_res_list.append({'key': 'oupt', 'value': ['', '', '', '']})

                        print(duyingpan_res_list)
                        print(rangfen_res_list)
                        print(fenshu_res_list)

                        if 'ml' in data['o']:
                            for duyingpan, rangqiu, rangfen, fenshu in zip(duyingpan_res_list, rangqiu_res_list,
                                                                           rangfen_res_list, fenshu_res_list):
                                save_res1 = name1 + ',' + duyingpan['value'][0] + ',' + rangqiu['value'][0] + ',' + \
                                            rangqiu['value'][2] + ',' + rangfen['value'][0] + ',' + rangfen['value'][
                                                2] + ',' + fenshu['value'][0] + ',' + fenshu['value'][2] + '\n'
                                save_res2 = name2 + ',' + duyingpan['value'][1] + ',' + rangqiu['value'][1] + ',' + \
                                            rangqiu['value'][3] + ',' + rangfen['value'][1] + ',' + rangfen['value'][
                                                3] + ',' + fenshu['value'][1] + ',' + fenshu['value'][3] + '\n'
                                print(save_res1)
                                print(save_res2)
                                with open('res.csv', 'a') as f:
                                    f.write(save_res1)
                                    f.write(save_res2)


if __name__ == '__main__':
    while True:
        try:
            get_res()
        except:
            print('未知错误')
        print('10秒后重新请求。。')
        time.sleep(10)


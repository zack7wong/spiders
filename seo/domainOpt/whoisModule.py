#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     whoisModule
   Description :
   Author :        hayden_huang
   Date：          2018/12/17 18:43
-------------------------------------------------
"""

import download
import re
import whois
import json

class WhoisClass():
    def __init__(self):
        # self.whois_list = [{'function':'builtIn()'},{'function':'panda()'},{'function':'aizhan()'}]
        self.whois_list = [{'function':'panda()'},{'function':'aizhan()'},{'function':'chinaz()'},{'function':'tencent()'},{'function':'baidu()'},{'function':'oneonefour()'},{'function':'twotwo()'},{'function':'whois_domain()'},{'function':'threeZeroZero()'}]
        self.domain_obj = {}
        self.down = download.Download()

    def builtIn(self):
        try:
            res = whois.whois(self.domain_obj['url'])
            if res:
                print('已注册')
                return True
            else:
                print('未知错误')
                return False
        except:
            print('未注册')
            return False

    def panda(self):
        url = 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain={domain}'
        start_url = url.format(domain=self.domain_obj['domain'])
        response = self.down.get_html(start_url,timeout=15)
        if response:
            search_res = re.search('<original>(.*?)</original>', response.text)
            if search_res:
                if 'Domain name is available' in search_res.group(1):
                    # 未注册
                    print('未注册')
                    self.write_unregiste()
                    # self.query_pr(domain_obj)
                elif 'In use' in search_res.group(1) or 'Invalid Domain Name' in search_res.group(1) or 'Domain name is not available' in search_res.group(1):
                    # 已注册
                    print('已注册')
                    self.write_registe()
                    # self.write_registed(domain_obj)
                else:
                    print('未知错误')
                    self.write_error()
            else:
                print('未知错误')
                self.write_error()
        else:
            print('网络请求错误')
            self.write_error()

    def aizhan(self):
        headers = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            # 'Cookie': "_csrf=8d9060a7828457f50a810a70966f69b8063ab1bdc33f9741339f2bdfbb06e4eca%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22Fa_qo9L5skczZ-3EGc5-lSbbLId9oGSo%22%3B%7D; Hm_lvt_b37205f3f69d03924c5447d020c09192=1543924868,1545299904; allSites=hhhso.cn%7Chhhgo.cn%2C0%7Cwww.baidu.com; Hm_lpvt_b37205f3f69d03924c5447d020c09192=1545302424",
            'Host': "whois.aizhan.com",
            'Pragma': "no-cache",
            'Referer': "https://whois.aizhan.com/",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            'X-Requested-With': "XMLHttpRequest",
            'cache-control': "no-cache",
        }
        url = 'https://whois.aizhan.com/{domain}/'.format(domain=self.domain_obj['domain'])
        response = self.down.get_html(url)
        if response and re.search("'cc':'(.*?)','rn':(.*?),",response.text):
            cc = re.search("'cc':'(.*?)','rn':(.*?),",response.text).group(1)
            rn = re.search("'cc':'(.*?)','rn':(.*?),",response.text).group(2)
            start_url = 'https://whois.aizhan.com/api/whois?domain={domain}&cc={cc}&rn={rn}'.format(domain=self.domain_obj['domain'],cc=cc,rn=rn)
            response = self.down.get_html(start_url,headers=headers)
            if response:
                try:
                    json_obj = json.loads(response.text)
                    if json_obj['regrinfo']['registered'] == 'yes':
                        print('已注册')
                        self.write_registe()
                    elif json_obj['regrinfo']['registered'] == 'no':
                        print('未注册')
                        self.write_unregiste()
                    else:
                        print('未知错误')
                        self.write_error()
                except:
                    print('未知错误')
                    self.write_error()
            else:
                print('网络请求错误')
                self.write_error()
        else:
            print('网络请求错误')
            self.write_error()

    def chinaz(self):
        url = 'http://whois.chinaz.com/{domain}'.format(domain=self.domain_obj['domain'])
        response = self.down.get_html(url)
        if response:
            if '未被注册或被隐藏' in response.text:
                print('未注册')
                self.write_unregiste()
            elif 'WhoisWrap clearfix' in response.text:
                print('已注册')
                self.write_registe()
            else:
                print('未知错误')
                self.write_error()
        else:
            print('网络请求错误')
            self.write_error()

    def tencent(self):
        headers = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            'Content-Length': "16",
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            # 'Cookie': "_ga=GA1.2.320374222.1525655369; pgv_pvi=419130368; pt2gguin=o0775340093; language=zh; qcloud_uid=35205008fb7e99a7cf41cb53fc2748d7; pgv_pvid=1417695788; __root_domain_v=.tencent.com; _qddaz=QD.m67761.3m427r.jj8dp70t; _gcl_au=1.1.77901751.1538011988; lastLoginType=wx; qcloud_from=qcloud.google.seo-1544602653156; isQcloudUser=false; qcmainCSRFToken=BkdFK8lYe4; intl=; qcloud_visitId=a28f8cd7ae500cb0926301c4162c91fa; wss_xsrf=987214d0a5c8c2415110cd712012cdbb%7C1545303683; ci_session=cb8f1a5ef4797f58e13fbff271c42207d32a07b3; _gat=1; pgv_si=s8430718976; C_AID=16866de89892b58a31b4ac9d12808f5e",
            'Host': "wss.cloud.tencent.com",
            'Origin': "https://wss.cloud.tencent.com",
            'Pragma': "no-cache",
            'Referer': "https://wss.cloud.tencent.com/postproxy",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            'X-Requested-With': "XMLHttpRequest",
            'cache-control': "no-cache",
        }
        url = 'https://wss.cloud.tencent.com/buy/api/domains/domain/whois_info?mc_gtk='
        body = 'domain={domain}'.format(domain=self.domain_obj['domain'])
        response = self.down.get_html(url, method='post',headers=headers,body=body)
        if response:
            json_obj = json.loads(response.text)
            if json_obj['status']['code'] == 0 and json_obj['result']['code'] == 0:
                print('已注册')
                self.write_registe()
            elif json_obj['status']['code'] == 2089:
                print('未注册')
                self.write_unregiste()
            else:
                print('未知错误')
                self.write_error()
        else:
            print('网络请求错误')
            self.write_error()

    def baidu(self):
        headers = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            'Content-Length': "36",
            'Content-Type': "application/json",
            # 'Cookie': "BAIDUID=B970C50F46C7D21D75F357B0CE8E1E51:FG=1; PSTM=1545137137; BIDUPSID=DCAE3195BFEA154D50EA26B9F9412D65; delPer=0; PSINO=6; ZD_ENTRY=google; H_PS_PSSID=26523_1467_21120_28131_26350_27751_27245_22159; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; Hm_lvt_28a17f66627d87f1d046eae152a1c93d=1544363968,1545307157; Hm_lpvt_28a17f66627d87f1d046eae152a1c93d=1545307172; BAIDU_CLOUD_TRACK_PATH=https://cloud.baidu.com/product/bcd/whois.html?domain=abc.com",
            'Host': "cloud.baidu.com",
            'Origin': "https://cloud.baidu.com",
            'Pragma': "no-cache",
            'Referer': "https://cloud.baidu.com/product/bcd/whois.html?domain=abc.com",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            'X-Requested-With': "XMLHttpRequest",
            'cache-control': "no-cache",
            'Postman-Token': "4ce2488d-c22d-4891-a1d2-788ad7254432"
        }
        url = 'https://cloud.baidu.com/api/bcd/whois/detail'
        body = '{"domain":"'+self.domain_obj['domain']+'","type":"NORMAL"}'
        response = self.down.get_html(url, method='post', headers=headers, body=body)
        if response:
            json_obj = json.loads(response.text)
            if json_obj['result']['code'] == 0:
                print('已注册')
                self.write_registe()
            elif json_obj['result']['code'] == 1:
                print('未注册')
                self.write_unregiste()
            else:
                print('未知错误')
                self.write_error()
        else:
            print('网络请求错误')
            self.write_error()

    def twotwo(self):
        url = 'https://whois.22.cn/{domain}'.format(domain=self.domain_obj['domain'])
        response = self.down.get_html(url)
        if response:
            if '该域名尚未注册' in response.text:
                print('未注册')
                self.write_unregiste()
            elif 'whois-list' in response.text:
                print('已注册')
                self.write_registe()
            else:
                print('未知错误')
                self.write_error()
        else:
            print('网络请求错误')
            self.write_error()

    def whois_domain(self):
        url = 'https://whois.domain.cn/'
        headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            # 'Content-Length': "11",
            'Content-Type': "application/x-www-form-urlencoded",
            'Host': "whois.domain.cn",
            'Origin': "https://whois.domain.cn",
            'Pragma': "no-cache",
            'Referer': "https://whois.domain.cn/",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            'cache-control': "no-cache",
        }
        body = 'name={domain}'.format(domain=self.domain_obj['domain'])
        response = self.down.get_html(url,method='post',headers=headers,body=body)
        if response:
            if '该域名可能尚未注册' in response.text:
                print('未注册')
                self.write_unregiste()
            elif 'table whois-info-list' in response.text:
                print('已注册')
                self.write_registe()
            else:
                print('未知错误')
                self.write_error()
        else:
            print('网络请求错误')
            self.write_error()

    def threeZeroZero(self):
        url = "https://api-shop.300.cn/domain/whois?domain={domain}".format(domain=self.domain_obj['domain'])
        headers = {
            'Accept': "*/*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            # 'Cookie': "ch_session=tq; GUID=6ece4b03-24ed-4419-826d-c747b8dc49a7; BROWSEID=022265f1-ee59-4ab7-8e08-6c777c1b1416; existFlag=1; pvc=1; rd=; vct=1; FLOWINGID=a9b5e38a-279b-4d94-bb89-eb087b9880ce; vt_origin_url=; vt_url=https%3A//www.300.cn/domain/info%3Fdomain%3Dabc.com; vt_origin=guanwang",
            'Host': "api-shop.300.cn",
            'Origin': "https://www.300.cn",
            'Pragma': "no-cache",
            'Referer': "https://www.300.cn/domain",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            'X-Requested-With': "XMLHttpRequest",
            'cache-control': "no-cache",
        }
        response = self.down.get_html(url, method='get', headers=headers)
        # print(response.text)
        if response:
            json_obj = json.loads(response.text)
            if json_obj['status'] == 101:
                print('已注册')
                self.write_registe()
            elif json_obj['status'] == 102:
                print('未注册')
                self.write_unregiste()
            else:
                print('未知错误')
                self.write_error()
        else:
            print('网络请求错误')
            self.write_error()

    def cnkuai(self):
        url = 'http://whois.cnkuai.cn/'
        headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            # 'Content-Length': "13",
            'Content-Type': "application/x-www-form-urlencoded",
            'Cookie': "ASP.NET_SessionId=gon2pziqsf1za5450t2mxg55",
            'Host': "whois.cnkuai.cn",
            'Origin': "http://whois.cnkuai.cn",
            'Pragma': "no-cache",
            'Referer': "http://whois.cnkuai.cn/",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            'cache-control': "no-cache",
        }
        body = 'ym={domain}'.format(domain=self.domain_obj['domain'])
        response = self.down.get_html(url,method='post',body=body,headers=headers)
        if response:
            if '没有找到域名的whois信息' in response.text:
                print('未注册')
                self.write_unregiste()
            elif 'domaintop' in response.text:
                print('已注册')
                self.write_registe()
            else:
                print('未知错误')
                self.write_error()
        else:
            print('网络请求错误')
            self.write_error()



    # 114
    def oneonefour(self):
        this_domain = self.domain_obj['domain'][::-1]
        url = "http://www.link114.cn/get.php?func=createdtime&site={this_domain}&r=31487611".format(this_domain=this_domain)
        headers = {
            'Accept': "*/*",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cache-Control': "no-cache",
            'charset': "utf-8",
            'Connection': "keep-alive",
            'Content-Type': "text/html",
            'Cookie': "latestversion=18.1116_2.032.362.811",
            'Host': "www.link114.cn",
            'Pragma': "no-cache",
            'Referer': "http://www.link114.cn/whois/",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            'cache-control': "no-cache",
            'Postman-Token': "79d4d279-8d23-449b-b4a7-8c343d3b6d5c"
        }
        response = self.down.get_html(url, method='get', headers=headers)
        print(response.text)
        if response:
            json_obj = json.loads(response.text)
            if json_obj['status'] == '1':
                if int(json_obj['result']['data']) >= 1:
                    print('已注册')
                    self.write_registe()
                elif int(json_obj['result']['data']) == 0:
                    print('未注册')
                    self.write_unregiste()
                else:
                    print('未知错误')
                    self.write_error()
            else:
                print('未知错误')
                self.write_error()
        else:
            print('网络请求错误')
            self.write_error()


#######################################
    def write_unregiste(self):
        with open('未注册.txt','a') as f:
            f.write(self.domain_obj['url']+'\n')

    def write_registe(self):
        with open('已注册.txt','a') as f:
            f.write(self.domain_obj['url']+'\n')

    def write_error(self):
        with open('未知错误.txt', 'a') as f:
            f.write(self.domain_obj['url']+'\n')

if __name__ == '__main__':
    obj = WhoisClass()
    obj.domain_obj['domain'] = 'hhhsa1aago.cn'
    obj.domain_obj['url'] = 'www.hsdafhhso.cn'
    obj.cnkuai()


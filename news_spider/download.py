import requests
import urllib.request
import json
import os
from time import sleep
from news_spider import config
from requests import RequestException

class Download(object):
    def __init__(self):
        self.retry_num = 0

    def get_ip(self,url):
        print('正在获取IP。。')
        try:
            response = requests.get(url)
            if response.status_code == 200:
                res_json = json.loads(response.text)
                if res_json['ERRORCODE'] == '0':
                    ip = res_json['RESULT'][0]['ip']
                    port = res_json['RESULT'][0]['port']
                    ip_res = ip + ':' + port
                    print('获取IP成功，当前IP为：',str(ip_res))
                    return ip_res
                elif res_json['ERRORCODE'] == '10036' or res_json['ERRORCODE'] == '10038' or res_json['ERRORCODE'] == '10055':
                    print('提前IP过快，5秒后重新请求', res_json)
                    sleep(5)
                    return self.get_ip(url)
                else:
                    print('未知错误，5秒后重新请求',res_json)
                    sleep(5)
                    return self.get_ip(url)
        except RequestException:
            print('请求IP_url出错，正在重新请求',url)
            sleep(5)
            return self.get_ip(url)

    def get_html(self,url):
        if self.retry_num > config.ERROR_MAX:
            self.retry_num = 0
            print('请求出错次数大于最大出错次数，已终止')
            return None

        proxies = {
                'http': 'http://xxx',
                'https': 'http://xxxx'
        }
        try:
            if config.COOKIES_SWITCH:
                response = requests.get(url, headers=config.HEADERS, cookies=config.COOKIES, proxies=proxies)
            else:
                if config.PROXY_SWITCH:
                    response = requests.get(url, headers=config.HEADERS, proxies=proxies)
                else:
                    response = requests.get(url, headers=config.HEADERS)
            if response.status_code == 200:
                return response
            return None
        except requests.exceptions.ConnectTimeout:
            print('请求RUL连接超时，正在重试', url)
            self.retry_num +=1
            return self.get_html(url)
        except requests.exceptions.Timeout:
            print('请求RUL超时，正在重试', url)
            self.retry_num += 1
            return self.get_html(url)
        except RequestException:
            print('未知错误，正在重试',url)
            self.retry_num += 1
            return self.get_html(url)

    def download_ressource(self,url_boj,ressource_url):
        print('正在下载。。。' + ressource_url)
        pwd = os.getcwd()
        if os.path.exists(pwd + '/' + url_boj['domain'] + '/' + 'index'):
            pass
        else:
            os.makedirs(pwd + '/' + url_boj['domain'] + '/' + 'index')
        file_path = pwd + '/' + url_boj['domain'] + '/' + 'index'
        file_name = ressource_url.split('/')[-1]
        try:
            urllib.request.urlretrieve(ressource_url, file_path + '/' + file_name)
        except:
            pass


if __name__ == '__main__':
    download = Download()
    res = download.get_html('https://xxx')
    print(res)
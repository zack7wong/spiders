import requests
import urllib.request
import json
import os
from time import sleep
import config
from requests import RequestException

class Download(object):
    def __init__(self):
        self.retry_num = 0
        self.chang_ip_num = 0
        self.ip = ''

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

    def get_html(self, url, method='get', body=None, headers=config.HEADERS,proxy=False):
        if self.retry_num > config.ERROR_MAX:
            self.retry_num = 0
            print('请求出错次数大于最大出错次数，已终止')
            return None
        if config.PROXY_SWITCH and proxy:
            if self.chang_ip_num % config.CHANGE_IP == 0:
                my_ip_url = ''
                with open('讯代理.txt') as f:
                    my_ip_url = f.read().strip()
                self.ip = self.get_ip(my_ip_url)
        self.chang_ip_num += 1
        proxies = {
                'http': 'http://' + self.ip,
                'https': 'http://' + self.ip
        }
        try:
            if config.COOKIES_SWITCH:
                response = requests.get(url, headers=headers, cookies=config.COOKIES, proxies=proxies)
            else:
                if config.PROXY_SWITCH:
                    if method == 'get':
                        response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
                    elif method == 'post':
                        response = requests.post(url, headers=headers, data=body, proxies=proxies)
                else:
                    if method == 'get':
                        response = requests.get(url, headers=headers)
                    elif method == 'post':
                        response = requests.post(url, headers=headers, data=body)
            if response.status_code == 200:
                return response
            return None
        except requests.exceptions.ConnectTimeout:
            print('请求RUL连接超时，正在重试', url)
            self.retry_num +=1
            return self.get_html(url,headers=headers)
        except requests.exceptions.Timeout:
            print('请求RUL超时，正在重试', url)
            self.retry_num += 1
            return self.get_html(url,headers=headers)
        except RequestException:
            print('未知错误，正在重试',url)
            self.retry_num += 1
            return self.get_html(url,headers=headers)


if __name__ == '__main__':
    download = Download()
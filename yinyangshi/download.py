import requests
import json
from time import sleep
import config
import redis
from requests import RequestException

HOST = 'localhost'
PORT = 6379
db = 1

class Download(object):
    def __init__(self):
        self.retry_num = 0
        self.chang_ip_num = 0
        self.ip = ''
        self.redis_client = redis.Redis(host=HOST, port=PORT, decode_responses=True, db=db)

        # http代理接入服务器地址端口
        proxyHost = "http-proxy-t1.dobel.cn"
        proxyPort = "9180"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": config.proxyUser,
            "pass": config.proxyPass,
        }

        self.proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }


    # def get_ip(self,url):
    #     print('正在获取IP。。')
    #     try:
    #         response = requests.get(url)
    #         if response.status_code == 200:
    #             res_json = json.loads(response.text)
    #             if res_json['ERRORCODE'] == '0':
    #                 ip = res_json['RESULT'][0]['ip']
    #                 port = res_json['RESULT'][0]['port']
    #                 ip_res = ip + ':' + port
    #                 print('获取IP成功，当前IP为：',str(ip_res))
    #                 self.redis_client.lpop('thisIp')
    #                 self.redis_client.rpush('thisIp',str(ip_res))
    #                 return ip_res
    #             elif res_json['ERRORCODE'] == '10036' or res_json['ERRORCODE'] == '10038' or res_json['ERRORCODE'] == '10055':
    #                 print('提前IP过快，5秒后重新请求', res_json)
    #                 sleep(5)
    #                 return self.get_ip(url)
    #             else:
    #                 print('未知错误，5秒后重新请求',res_json)
    #                 sleep(5)
    #                 return self.get_ip(url)
    #     except RequestException:
    #         print('请求IP_url出错，正在重新请求',url)
    #         sleep(5)
    #         return self.get_ip(url)

    def get_ip(self):
        proxies = self.proxies
        requests.get('http://ip.dobel.cn/switch-ip', proxies=proxies, verify=False)

    def get_html(self,url,method='get',headers=config.HEADERS,data='',timeout=10):
        # if self.retry_num > config.ERROR_MAX:
        #     self.retry_num = 0
        #     print('请求出错次数大于最大出错次数，已终止')
        #     return None
        # if config.PROXY_SWITCH:
        #     if self.chang_ip_num % config.CHANGE_IP == 0:
        #         self.ip = self.get_ip(config.IP_URL)
        # self.chang_ip_num += 1
        # proxies = {
        #         'http': 'http://' + self.ip,
        #         'https': 'http://' + self.ip
        # }

        if self.retry_num > config.ERROR_MAX:
            self.retry_num = 0
            print('请求出错次数大于最大出错次数，已终止')
            return None
        if config.PROXY_SWITCH:
            if self.chang_ip_num % config.CHANGE_IP == 0:
                self.get_ip()
        self.chang_ip_num += 1

        proxies = self.proxies

        try:
            if config.COOKIES_SWITCH:
                response = requests.get(url, headers=config.HEADERS, cookies=config.COOKIES, proxies=proxies,timeout=timeout)
            else:
                if config.PROXY_SWITCH:
                    if method == 'post':
                        response = requests.post(url, headers=headers, data=data,proxies=proxies,timeout=timeout)
                    else:
                        response = requests.get(url, headers=headers, proxies=proxies,timeout=timeout)
                else:
                    if method == 'post':
                        response = requests.post(url, headers=headers, data=data,timeout=timeout)
                    else:
                        response = requests.get(url, headers=headers,timeout=timeout)
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

if __name__ == '__main__':
    download = Download()
    res = download.get_html('https://xxx')
    print(res)
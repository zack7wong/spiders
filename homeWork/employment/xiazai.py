import requests
import json

#请求头配置
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Connection':'keep-alive',
    #'Host':'m.weibo.cn',
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With':'XMLHttpRequest',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8'
}

class Download(object):
    def get_html(self,url):
        try:
            response = requests.get(url, headers=HEADERS)
            if response.status_code == 200:
                return response.text
            return None
        except:
            pass

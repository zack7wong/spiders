MONGO_URL = 'localhost'
MONGO_DB = 'weibo'
MONGO_TABLE_USER = 'weibo_user'
MONGO_PORT = 27017
MONGO_PASSWORD = None

REQUEST_NUM = 0
CHANGE_IP = 150

IP = ''
PROXY_SWITCH = True
COOKIES = ''

COOKIES_SWITCH = False
ERROR_MAX = 5

#初始URL配置
#姚晨的微博主页
START_URL = 'https://m.weibo.cn/u/1266321801?uid=1266321801&featurecode=20000320'
START_ID = '1266321801'

IP_URL =''

#请求头配置
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Connection':'keep-alive',
    'Host':'m.weibo.cn',
    'Referer':'https://m.weibo.cn/',
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With':'XMLHttpRequest',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8'
}
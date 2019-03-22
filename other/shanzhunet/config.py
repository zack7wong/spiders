
#当前请求次数
REQUEST_NUM = 0

#请求多少次后换IP配置
CHANGE_IP = 150


#是否开启代理
PROXY_SWITCH = False


#请求最大出错次数
ERROR_MAX = 5

#初始URL配置
HOST_URL = 'https://www.zhipin.com'

#讯代理配置
IP_URL =''

#请求头配置
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Connection':'keep-alive',
    #'Host':'m.weibo.cn',
    #'Referer':'https://m.weibo.cn/',
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With':'XMLHttpRequest',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8'
}
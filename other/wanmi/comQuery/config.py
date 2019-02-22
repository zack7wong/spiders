#当前请求次数
REQUEST_NUM = 0

#请求多少次后换IP配置
CHANGE_IP = 10

#代理IP
IP_URL = ''


#是否开启代理
PROXY_SWITCH = True
#是否使用cookies
COOKIES_SWITCH = False
#请求最大出错次数
ERROR_MAX = 3

#请求头配置
HEADERS = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    # 'Cookie': "PHPSESSID=01v4vblblrlqhcpld57s1u3m15; Hm_lvt_f719ef2a0af90fabae8f4b23c8b0a340=1546956492; tprice=1793950; tnum=2858; yprice=101978; ynum=2271; jprice=1691972; jnum=587; Hm_lpvt_f719ef2a0af90fabae8f4b23c8b0a340=1547021625",
    'Host': "www.wanmi.cc",
    'Pragma': "no-cache",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
}

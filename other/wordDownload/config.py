#当前请求次数
REQUEST_NUM = 0

#请求多少次后换IP配置
CHANGE_IP = 10

#代理IP
IP_URL = ''

START_URL = 'http://www.77tj.org/tencent'


#是否开启代理
PROXY_SWITCH = True
#是否使用cookies
COOKIES_SWITCH = False
#请求最大出错次数
ERROR_MAX = 3

#请求头配置
HEADERS = {
    'connection': "keep-alive",
    'cache-control': "max-age=0",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Content-Type': 'application/x-www-form-urlencoded'
}

BODY ='PageIndex={pageToken}&__RequestVerificationToken=CfDJ8GFb1P15V9tAonTahCRuop9hvvEFAsMEgf0eSsndTVK9E2VkbpxihV4Yygxii2zD-puspgughgb44cUOkS5GpRuZGQOf7zLvfq1IrQa9jROH_EjyQuW7ZAEV6ev99WXavXLLBwKs9cbmw7g_bIBiyag'

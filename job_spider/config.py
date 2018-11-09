#mongodb配置
MONGO_URL = 'localhost'
MONGO_DB = ''
MONGO_TABLE_USER = ''
MONGO_PORT = 27017
MONGO_PASSWORD = None

#mongodb配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = ''
REDIS_EMPLOYMENT = ''

#mysql配置
MYSQL_HOST = 'localhost'
MYSQL_DB = 'job_spider'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_CHARSET = 'utf8'


#当前请求次数
REQUEST_NUM = 0

#请求多少次后换IP配置
CHANGE_IP = 0

#代理IP
IP = ''

DETAIL_URL = 'https://rd5.zhaopin.com/api/rd/resume/detail?resumeNo={id}_1_1%3B{key}%3B{time}'

#是否开启代理
PROXY_SWITCH = False
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
    'cookie': 'ZP_P_VERSION=v2; index=0; rd_resume_srccode=402101; sts_deviceid=166ce4675cf449-014ce3d36735ba-1e3c6655-2073600-166ce4675d07be; sts_sg=1; sts_chnlsid=Unknown; dywec=95841923; __utmc=269921210; login_point=113386110; NTKF_T2D_CLIENTID=guest5B486913-3AEF-74A8-EBB8-CE46CC249D0C; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_60756792,tid:1541059038243049}; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3Fy7bRbP%3DdrDlkAq.tn7.tn7.tgU0awSjko_u7InJ_G4epvcQoAG.; diagnosis=0; urlfrom=121114584; urlfrom2=121114584; adfcid=www.google.com; adfcid2=www.google.com; adfbid=0; adfbid2=0; rd_resume_actionId=1541403819577709130737; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22709130737%22%2C%22%24device_id%22%3A%22166ce46760f550-0516aea2ec08f6-1e3c6655-2073600-166ce4676112c9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com.sg%2F%22%2C%22%24latest_referrer_host%22%3A%22www.google.com.sg%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%2C%22first_id%22%3A%22166ce46760f550-0516aea2ec08f6-1e3c6655-2073600-166ce4676112c9%22%7D; dywea=95841923.1754148472041244400.1541059016.1541410138.1541732199.5; dywez=95841923.1541732199.5.3.dywecsr=google.com.sg|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/; __utma=269921210.1500883269.1541059017.1541410138.1541732199.5; __utmz=269921210.1541732199.5.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1540894844,1540895364,1541403757,1541732200; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1541732200; sts_sid=166f66680b474e-08f4799d4e866-1e3c6655-2073600-166f66680b5469; JsOrglogin=2127392213; Token=4fe23bb6fe0f4d6c8b1a78ba13badc5b; at=4fe23bb6fe0f4d6c8b1a78ba13badc5b; rt=16421b3c2ca64266b310e12e60aee44b; RDsUserInfo=; uiioit=; puid=1016744359; mobile=15768653949; zp-route-meta=uid=709130737,orgid=60756792; sts_evtseq=3; dyweb=95841923.7.6.1541732217037; __utmb=269921210.7.6.1541732217042'
}

#mongodb配置
MONGO_URL = 'localhost'
MONGO_DB = ''
MONGO_TABLE_USER = ''
MONGO_PORT = 27017
MONGO_PASSWORD = None

#redis配置
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
    'cookie': 'sts_deviceid=169155d77f067-0d9cfea9ba6f-36627102-2073600-169155d77f12a; urlfrom2=121114584; adfcid2=www.google.com; adfbid2=0; dywez=95841923.1550841642.1.1.dywecsr=google.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/; __utmz=269921210.1550841642.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); Hm_lvt_38ba284938d5eddca645bb5e02a02006=1550841642; _jzqa=1.3832701134525368000.1550841648.1550841648.1550841648.1; _jzqx=1.1550841648.1550841648.1.jzqsr=passport%2Ezhaopin%2Ecom|jzqct=/account/register.-; __xsptplus30=30.1.1550841647.1550841647.1%234%7C%7C%7C%7C%7C%23%238wpOCTq5ZYkW6NVEPf8YOIFg6UflpfIj%23; acw_tc=2760820c15513406634544451ec432be85ff301ba9055d35bf3a406deb47e8; sts_sg=1; sts_chnlsid=Unknown; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%3Fbkurl%3Dhttps%253A%252F%252Frd5.zhaopin.com%252F; dywec=95841923; __utmc=269921210; puid=1027829929; mobile=15245392563; zp-route-meta=uid=1018126177,orgid=59579072; login_point=59579072; companyCuurrentCity=715; NTKF_T2D_CLIENTID=guestD09B909B-7E8B-16D9-3E81-469A7EC6AD6B; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_59579072,tid:1551667723973201}; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221018126177%22%2C%22%24device_id%22%3A%22169155d78a77e0-0206ec39d0de7-36627102-2073600-169155d78a8493%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22169155d78a77e0-0206ec39d0de7-36627102-2073600-169155d78a8493%22%7D; dywea=95841923.1586841291721068800.1550841642.1551445440.1551670167.5; __utma=269921210.504785009.1550841642.1551445441.1551670167.5; sts_sid=16946bfcb821c1-02af6df3b03568-36637102-2073600-16946bfcb834e7; rd_resume_srccode=402101; __utmt=1; JsOrglogin=3054378533; at=f1249419fe054c1187079e91819c8e52; Token=f1249419fe054c1187079e91819c8e52; rt=e6f0f6e83497430ab3c89eb01326df38; RDsUserInfo=3d692e695671467155775875516a557542775e695b695c7140715e772575276a597503770c690d690d711f7103771d750e6a0e751677536939693f714a71547752752b6a20754d775d6953695e7140715c7759755e6a56754b7729693e695671447148775d75496a5575417752695f695a714c7124772575546a54754b773d692b6956713d712c775875516a557542775e695b695c714071507752753c6a30754d7759695f6958714c7136772075546a54754b776; uiioit=3d753d6849684564553808644b6844795a745e7455650f39537353753b683068496450380064466842795174587453650a395f734; rd_resume_actionId=15516715121631018126177; sts_evtseq=21; dyweb=95841923.24.6.1551671506176; __utmb=269921210.24.6.1551671506185'
}

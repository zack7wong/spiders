#当前请求次数
REQUEST_NUM = 0

#请求多少次后换IP配置
CHANGE_IP = 0

#代理IP
IP = ''

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
    'cookie': 'ZP_P_VERSION=v2; index=0; rd_resume_srccode=402101; sajssdk_2015_cross_new_user=1; sts_deviceid=166c8283ff63a7-098ea79927d969-1e3c6655-2073600-166c8283ff7396; sts_sg=1; sts_chnlsid=Unknown; dywec=95841923; dywez=95841923.1540956373.1.1.dywecsr=(direct)|dyweccn=(direct)|dywecmd=(none)|dywectr=undefined; __utmc=269921210; __utmz=269921210.1540956373.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); at=1ff30e8b89314c1b966648613e2189b5; Token=1ff30e8b89314c1b966648613e2189b5; rt=8cc0f88ee8744b66a70614f5fbcfe311; RDsUserInfo=3d753d6857645f754968536459754a685a645f754a685d6453753568246455750a680f641e751c680464597549685a6453752a683e645575486851642a753d6857645e7549685d645d754f685d6451754b68516429752d6857645975496847645b7548684a645975486850645a754f685164297535685764587542683f6429754468206424754968536459754a685a645f754a685d645c7542683f643c7544685b645e75496851643b7530685764587542683; uiioit=3d752c6452695c6a04355e6459755b645f695c6a0735506453752a642b69566a023557645f755d6459695c6a0d35556453751; zp-route-meta=uid=709130737,orgid=60756792; login_point=113386110; NTKF_T2D_CLIENTID=guest5599B4EC-746D-CA4C-AAB1-C828AD78185B; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_60756792,tid:1540956401016466}; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22709130737%22%2C%22%24device_id%22%3A%22166c8283fea8f8-0ef3aefded9bf8-1e3c6655-2073600-166c8283febab9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22166c8283fea8f8-0ef3aefded9bf8-1e3c6655-2073600-166c8283febab9%22%7D; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3Fy7bRbP%3Ddrmmqqkp0wop0wop03U0a1b.qe6na6e1FDHk02eanbop; diagnosis=0; sts_sid=166c848f4354f5-06a9f3fad8eb54-1e3c6655-2073600-166c848f437124; dywea=95841923.2678522126308734000.1540956373.1540956373.1540958520.2; dyweb=95841923.1.10.1540958520; __utma=269921210.2132798144.1540956373.1540956373.1540958520.2; __utmb=269921210.1.10.1540958520; sts_evtseq=6; rd_resume_actionId=1540959209773709130737'
}

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
    'cookie': 'ZP_P_VERSION=v2; index=0; rd_resume_srccode=402101; sts_deviceid=166ce4675cf449-014ce3d36735ba-1e3c6655-2073600-166ce4675d07be; sts_sg=1; sts_chnlsid=Unknown; dywec=95841923; __utmc=269921210; login_point=113386110; NTKF_T2D_CLIENTID=guest5B486913-3AEF-74A8-EBB8-CE46CC249D0C; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_60756792,tid:1541059038243049}; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3Fy7bRbP%3DdrDlkAq.tn7.tn7.tgU0awSjko_u7InJ_G4epvcQoAG.; diagnosis=0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22709130737%22%2C%22%24device_id%22%3A%22166ce46760f550-0516aea2ec08f6-1e3c6655-2073600-166ce4676112c9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com.sg%2F%22%2C%22%24latest_referrer_host%22%3A%22www.google.com.sg%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%2C%22first_id%22%3A%22166ce46760f550-0516aea2ec08f6-1e3c6655-2073600-166ce4676112c9%22%7D; urlfrom=121114584; urlfrom2=121114584; adfcid=www.google.com; adfcid2=www.google.com; adfbid=0; adfbid2=0; dywea=95841923.1754148472041244400.1541059016.1541068747.1541403757.3; dywez=95841923.1541403757.3.2.dywecsr=google.com.sg|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1540887006,1540894844,1540895364,1541403757; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1541403757; __utma=269921210.1500883269.1541059017.1541068747.1541403757.3; __utmz=269921210.1541403757.3.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; sts_sid=166e2d2e8d5120-07232ef89a1343-1e3c6655-2073600-166e2d2e8d67f9; JsOrglogin=2127392213; at=8b96d82474814741abbbc81ee787c681; Token=8b96d82474814741abbbc81ee787c681; rt=aae804ef23404d9cbee7780216449f60; RDsUserInfo=386b2e69567140655f700c69446d586a596b4677566f47355275216b2469567104650a704369106d056a586b4177556f4b353a75396b57695a714c652d707169486d5d6a596b4677506f46355e75546b5869507136653b700869446d5a6a446b4477456f43355375596b59695071366523700869456d506a3c6b3077586f3a3525755d6b53695a7144655f700269466d5c6a5d6b4a77306f243554755c6b5c695b714c653c707c69486d5b6a526b9; uiioit=2179306559640f3754770d6454744a7455645338046440345f653679306559640e375477036450744f7452645d3805644c343; zp-route-meta=uid=709130737,orgid=60756792; dyweb=95841923.9.6.1541403777532; __utmb=269921210.9.6.1541403777538; rd_resume_actionId=1541403814759709130737; sts_evtseq=5'
}

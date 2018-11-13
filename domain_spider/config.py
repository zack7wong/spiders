#当前请求次数
REQUEST_NUM = 0

#请求多少次后换IP配置
CHANGE_IP = 50

#代理IP
IP_URL = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=a9363202c98d47149a95ba299927b1e0&orderno=YZ201811139742062xj6&returnType=2&count=1'

START_URL = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={datetime}&leftTicketDTO.from_station={start}&leftTicketDTO.to_station={end}&purpose_codes=ADULT'

QUERY_DOMAIN_URL = 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain={domain}'
QUERY_PR_URL = 'https://pr.aizhan.com/{domain}/'
SOGOU_URL = 'https://www.sogou.com/web?query={domain}&_asf=www.sogou.com'

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
    # 'cookie':' SUV=1522740796080229; SMYUV=1522740796081448; SUID=12C710B7572B8B0A5AC449150002FF06; wuid=AAHMaltFHwAAAAqLK1fWjgoApwM=; CXID=96B7F31133531AC7F5BFB5EBA3EFDB1D; IPLOC=CN4403; pgv_pvi=606208; sw_uuid=8342716051; ssuid=6295371917; dt_ssuid=8529746536; start_time=1540134704266; pex=C864C03270DED3DD8A06887A372DA219231FFAC25A9D64AE09E82AED12E416AC; ad=$yllllllll2bf01JlllllVs$5y6lllllWv2XEZllll9lllllRqxlw@@@@@@@@@@@; ABTEST=0|1542102394|v17; browerV=3; osV=2; SNUID=BF4B1356303555B882B52BE53082AD5C; sct=78; sst0=213; ld=eyllllllll2bfILnlllllVs$IdklllllWv260ZllllklllllRylll5@@@@@@@@@@'
}

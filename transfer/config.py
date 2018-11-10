
#mysql配置
MYSQL_HOST = 'localhost'
MYSQL_DB = 'transfer'
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

START_URL = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={datetime}&leftTicketDTO.from_station={start}&leftTicketDTO.to_station={end}&purpose_codes=ADULT'

# TIME_LIST = ['2018-11-11','2018-11-12','2018-11-13','2018-11-14','2018-11-15','2018-11-16','2018-11-17','2018-11-18','2018-11-19','2018-11-20']
TIME_LIST = ['2018-11-12']
CITY = ['北京','上海','天津','重庆','长沙','成都','福州','广州','合肥','杭州','济南','昆明','兰州','南京','南昌','沈阳','武汉','西安','深圳','厦门']

#爬虫模式
SPIDER = False
#计算模式
Calculation = True

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
}

#1621202301 蔡慧情 16新媒体1班  第2题 2018年12月18日 14:50


from datetime import datetime
import time

dayOfWeek = datetime.today().weekday()
start_date = datetime.strptime('20180903','%Y%m%d').weekday()
end_date = datetime.strptime('20190111','%Y%m%d').weekday()

# all_time =
a = int(time.mktime(time.strptime('2018-09-03',"%Y-%m-%d")))
b = int(time.mktime(time.strptime('2019-01-11',"%Y-%m-%d")))
mydate = int((b - a )/(60*60*24))

def get_week(week):
    if week == 0:
        res = '星期一'
    elif week == 1:
        res = '星期二'
    elif week == 2:
        res = '星期三'
    elif week == 3:
        res = '星期四'
    elif week == 4:
        res = '星期五'
    elif week == 5:
        res = '星期六'
    elif week == 6:
        res = '星期日'

    return res

print('开学时间为：20180903, 是'+get_week(start_date))
print('结束时间为：20190111, 是'+get_week(end_date))
print('一共有：'+str(mydate)+'天')


#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lxml.etree import HTML
from openpyxl import Workbook
import requests

wb = Workbook()
sheet = wb.active
sheet.title = 'Sheet1'

start_url = "http://www.lnggzy.gov.cn/lnggzy/showinfo/Morejyxx.aspx"

querystring = {"timebegin":"2018-12-05","timeend":"2019-01-05","timetype":"05","num1":"001","num2":"001004","jyly":"005","word":""}

payload = "__VIEWSTATE=I5efweZkJ5gGXep%2FCnWN91qx60aJLEn0xbSRBsbDU%2BRzX9Vf8oQSYLttqKZV9lCUiGjVxtaFyUYRLnppagn4WroNsOGuikY0y0VIfRDgbWKJW7zRnAx9%2F4pkYE6MX5HFH2WFGD%2B6jqGGgpu%2FXy8ophQyAc92SOWHs8HzzQRVbz%2FSlGLvuaWfXpY8XCYtBkOW2yM07wA4%2B5%2F1z%2F2OEQyR5L2Eq%2BzYi5L0e6PaXEqrA6CvHiHVz5XRhZylNpTQclYDevOZnqk7GbL3R3xRPCZu%2Bmx3%2F8UNAdBbbiKGdx9O9b%2B9vK5s%2BQuzq81Qd5325TqWv619OZAjapKiUET0kJS%2FnxO8jF6xiq61HHINoMAUicQ7Ku0eWVDs8yDBJIKLfhGeXOjgajMGtTf0kydPvX%2FjAwSRuEGCTBKHuWxaD5yHtzcJkphyz8byf3fN%2BARR5TYbSXXnJH9wsQV0Os%2BNJGdNY7BkvCwP7WfB7ePlCBYX8rEnsPUKOPRFCNUmskAZc87LMuTB1%2Fe%2BCjIWlU%2FD%2BCb3Q2KmEMU2yPZ2n2la6qTYzpQAfxgS7IguUGNAWgpLvTpASUodHR4E6ACI%2FKw5ERk9BTwXzieWIGv5dv1KzGlPO%2FeIYRCkX1uXf6qUV8pF%2BtlKbO4a162HHv8fLi4LOw%2BTfJGcOIKywPrRqVrbt5vW6wicdOHwrc%2BHwfQ4sw%2BWMouZo4Du7xasz9%2B2nwtPP7NuPyGKNy5ggzn2ZINNAlNo3EBE3nSb0%2F3R9CHZrL%2FZfwTUrfGV2G8mkZj7tDFJvC%2F7aSXZQX7szgYxoLO7AIXDE730rLw2%2BT6OnT8hMeLHbvKLaJSSvlnpJ8NF3wD5%2FfjehORPnoWif9iBhpCan2YeR7rnONRv7I2QXthf8%2BZXzeKYgBHl3DtVX6KezqNSJU6fYsf6D4kngDkIwXTsTsfZyMtismXeb%2BrVeZHBO5FuLp0O1KJ1aVwAafMErk7peLIarqOAAXN8GaHhmrt10zhp3DkH0dVo094KWjFVydgiqISiQPpZ1Iw9NF3ZojVJ3gu8nVYcdFlRjdUeskndkQpvCb3fdH%2FWeceW1o4gyNytA0IXBHgdcyER8QzcRnNipg%2BO7LQCkdCKNxIjC%2FRWOl1vJ0ZJmZxoEKWgTyoSF70Z2JHoeXj1mRxOsFhk%2FMYuKVDv%2FJXn6XEK3yh9BKfAj27Ss9MMrhwAoFu58jE%2Bg%2FnM2lIrZ94EBjCbp%2FrHNKewwKRnzvmla2DvVjs2nFhJi7PK6OLClIkof1pVluCca%2B8gEOKfl%2FRv9Ja8QH3sihEMokLOpyYEAlZJSRb0b3tRPc9eYloVY1y5wQiG3R%2FNOT9xpV5pSufae6V1J2MCxpkMbxSn7fakFtJUmCPVJrcVgPdtsOYaymK0hBF03pEK8SCVKCWjHr2OGZXBnVOUQPO9Q%2B4oOYE1nriil7ZzlzkXyIpjqT4PRHRQhzGAYZyVqZHfO4rOM0SSetIrxSNie1AXndGOvPzcEcX2FfiBcJ7m0nc3Q6apz8GyoJHw7i3t16weRREwKgv%2F%2F6KPeaVDsqc%2B5%2Fi%2BI%2FTnejSDJyS3r6QNbgScwPuPotvk%2B5XeLn%2BtZc7ZutZh4Jh%2BEeO%2BlOW8%2B7P8sKMX2iHfGwiWTxOrnISjTpnvfi1z6DE%2BvsMdPDmmV71gLkcmgmbMxMl8lR0WbDAOTsv3%2Favy3jMv40MSFZCfa5zo1xDtio9VutWjbO4mxuum6F46C58xSkn%2BAnGDEdPGvHm%2BQT%2FAhSvkhfkqqpZl0RRuBTdj8QVJXCKwPrt%2BgkBq%2BkJpJYMspYHUBFxVhIZNm2E1IUyabHBoYFSPXjvX9IRDnP2hWLlWUL97qIiuTDYMtn4uwIB4rw%2B538ClKj0rwDKjtxl44rT8iPrckhXeH0%2Byo1rohD9sYEIxCw6rNHDc4swMzjx0fQHaydEXGWzAlGFpXYQSWhD9XceQMCuIWFVU63dbZ%2FOawg%2BXn70jYQkvndjWGo6seEoSF%2BSsrT273VngscxPi1gdI05MdpOExPZz0QiNRM7PL2SDEY3Jyr26hQNNn98TCtcj9IcB7hbHGvsOMcWh%2BLkM8ZbK1PsBTN2Lp%2FCKb73Nj8Y4aJoIar2ugiYiBiRsviGcCHMQXvT%2BAdUJXZDojdI75gqUpaoTVTx1j0TC3Q5OuG2wKa5rFt1xTFQjO2wPUfj%2Fjl69%2BlS3gWYAGvAqLSorqD9O48YJZjiVZERpveyIKDWuN8fOe%2BEQ47vnqsN7uwodlNP7tlar5Qqvj%2FtqRR3ApRsvjc%2BQIeFejexhyfzcDVZTCUpQ1PoqkTHeKWrkvBG0apxSMyw2RGJ6Wy3Cd7%2Bjj6rCB5IxPB6T%2FMRqEPj9CAslzLwRdBhdOIFOFEJo1w1Ba%2Fp%2B6634Jj1WUOdnUZAOlMEr7e%2FzDJoDBCMRPtIiqyo%2BFBiZDh5k2lE2a7rPZ7QkAJ3b2Am%2B73GUWIkavnRFxFu550ADqrTsTiKRyDAjn%2FuR%2FujAoCe0cYuzw7sMXEkAOhilH3HTsNE99AvBE5USi1Oee7g%2FbOa9FkW9P7QnrCf1HSGQmBNmEenfns8zrv9m0TqoHaV4nGXRMsXz3reBn0ZLHbAmifVD%2Bdi0g4qAc43rVIr7MSp1OFHJukhxHI6MVBtS4K%2FdbrZ2N%2FeHBgRFaQ1GaPVdivky%2B3hA5%2FK1xoIYcdt2IAIJeb88bDF67duTbBF9ims1Yr8t6s8ysppoToYtj0z0Ug0xvOlRNwp6yRUow%2FvNYUFEtH2kz0AO0%2FUhDJMKI9yN8riFZDEPtA0gsOhhfm6f2fIq63u4FTpfSCzoDTAjx1dgGniqyXw1%2B1gw3oyKWHtkyj2jzf98WlSrPMWASwhZrA1pFEAoenCbQL6OkKafqJeUv%2FGsQdQsxJznwyvDIV5GBfGuqu78v3EWAmZ3ciBEAwIjmAKTKWaRKuJDYuQDk6vIgK1S%2BhkMKL8r%2FET%2FPy0ZMOnyC3Cm3LxZTYExMf%2BcgLgL7AUXI%2FK5QUij1DO1wqmwmxfqI32eL8IoewGuDtMk9qkfA%2BRYDq5NtTIVwMpt9NOr2i005WbgrgwAI3oHjqCrGFQZvChhMS7Gv6Kn6uFJDzW21LMfmyiIZiJnaYqZ9aalChju%2FuK6l5ZUr0MBLmWhxqvPVhJMPUIKQPUbgDg2mH8d8ROE1XAvYmWdtMdYLGsf%2FcQdv1paC5M4ZGo2cTuGP%2FiMVOuMe06uO4jDzU1491W%2B6MzLrdsfbGsIm6ZuJDJer4w7PKCZcpiF4GWyGdJYsjHh06VCsK%2B5ARvj3jhSUA7gTdkLd0koejnsCkxg%2BcOGBQfl1Of4qd9zBQfqZW%2BCfY0mcZ3Fy1%2B7%2BE9krzLU%2BTPKAPWZIbjsgS9UQwuae75Q8GGwzM%2Bu0XlCOwyTDZIURYjsIrxNtV%2BKW6JSA86ymyfKQCgntXJCqbRJlTVNGCI8EWmT2DGAtwOiiMWKuqhgv3vJRM%2F2CmTBNr6I4%2B1FvkORmK6x4ag1Hc2ovkU%2FR6SHmEOSnwFS3OMDWW3m%2Bv9CX2A3e1a7L3f028%2FOeiY%2FkYQn7jbbjn7%2BHz6MGt8vcq4Fh7RRk2tuW208K1P0xzqA0B6%2BpwZrV%2FfT61qGBzCMyBrGN4PfnZbdDfOoK%2B1w4WONprlc28D6NZUkDl8gssQ4tIrl07Tm8b59cDMzsYvJLzmh%2FjJWNJetgfRp6GRTc%2FB%2B9dS%2F42qD64l0oJww%2B%2FNfCKVXFqXvsjCKzFs8YsNRJM2qgTGY7hsv2xG2jAemYKCKsa%2FeLpjWUeaQzZazM%2FZ79ott%2FTHbvFmERTcFLG3DVEqGIIbI1islxMp6qPoB6FT%2Bge%2B7t%2F1ba1O6zMfI2B4znHR0o25w79MvlPe7bobRWOgzG1pSsDDbSZ1N67kbVZ8yVdfYnKKEOnQdhkedbZLWCeJK4qqNulRwbR4qjq6x5G8ugSVSlTdQbDJ6KULvNhJDqRPjsTwDl0u6RMS7eritd8i9uap%2FfTIw4%2FmP2I%2Fny7aX%2BqICHMgYB3czBP%2Fmx0ZDGmq1P%2Ba74iIgFzfJFJCPw3vxsSNBbjobpibO4%2BMM62ChxtptHl%2FB3Di4KvHEWVVzKDlEnZEevOJjCH7C2kktDaaBiYjZB4VLqEzVUSYNcvziryMuqE4pnV%2FQ3mRYikBjpRFSJBlC%2Bp%2BVsOYFl94NNnI1FDV5mXAWN1%2BFff5JV0wy9uAhb0BQdxmlrVnCNZD6sHWCsI5CxJXYm7AInS4L2FA0Ehw3sI%2Bw%2FuS8XAE3m0rdqkH0gchKSgO17%2B%2B%2FRZV3lJ93%2BDgMxi02sLwQ93p3ugT3Opr6SaWGRVNDs%2BdKRRxOqsASn6IDK4x%2FP9UHevKVYC0hYmiNHZQu0IGnFesHQfsared5r4hORUvWp3%2F9bmW1XN9kCe0FJ%2FGaGG%2FeKT3wYFgJLENgEzi79%2F0WrGq%2BXAx9Lbj%2Fv7DtATy5jjyia6vt%2BLtwlM5aUGfHlsW%2FBZUPBt0TGU3oj6mRKYNhQ1QuXmQT7M8nXqMYc52Xii1P%2BFtKzc%2B9adaNUuMOF131smaZ0z6uJFnkUSiS%2F4r5To1SHg9IMT6PWbnlP7PZ8%2BwE5spTHJ6Sk1IRzd5BomHXPNYaLhIcSZhsp71lDTP8CJwJwmP4szx0GI%2BZw8svsamayJtqO1Vlsovv2wpiNk%2Bd7vn%2BQNi7TkVTqBDyPblKaX%2F5Mf37yeFKXM7e%2FPNbP2WuxUy8XJr3I5FyPjk8VqKvHj%2F9lreimu7tpy83TPNLhLE37aW57co9MNdK2fXN0Bw5n8%2B%2FJAPLq8bzaX%2B4S7m4mKRb8cvTG7SOWN1%2FCyQSyCEe5Gml7asfZg%3D%3D&__VIEWSTATEGENERATOR=5E8AF86B&__EVENTTARGET=MoreInfoListjyxx1%24Pager&__EVENTARGUMENT={pageToken}&__VIEWSTATEENCRYPTED=&MoreInfoListjyxx1%24Pager_input=1"
headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "5328",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cookie': "ASP.NET_SessionId=xxfahrrbl1xtdavlxfkupua0",
    'Host': "www.lnggzy.gov.cn",
    'Origin': "http://www.lnggzy.gov.cn",
    'Pragma': "no-cache",
    'Referer': "http://www.lnggzy.gov.cn/lnggzy/showinfo/Morejyxx.aspx?timebegin=2018-12-05&timeend=2019-01-05&timetype=05&num1=001&num2=001004&jyly=005&word=",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "f7b7b72c-5808-4275-88a9-276cb71646e2"
    }
for i in range(1,432):
    print('当前页数：'+str(i))
    body = payload.format(pageToken=i)
    try:
        response = requests.request("POST", start_url, data=body, headers=headers, params=querystring,timeout=10)
    except:
        continue


    html = HTML(response.text)
    urls = html.xpath('//h4/a/@href')
    titles = html.xpath('//h4/a/@title')
    print(urls)
    for url,title in zip(urls,titles):
        try:
            link = 'http://www.lnggzy.gov.cn'+url.replace('InfoDetail/Default.aspx','ZtbInfo/Zfcg.aspx')
            print(link)
            print(title)
            detail_response = requests.get(link,timeout=10)
            detail_response.encoding = 'utf8'
            detail_html = HTML(detail_response.text)
            content_list=detail_html.xpath('//td[@id="zfcg_zbgs1_TDContent"]//text()')
            content = ''.join(content_list)
            # print(content)
            row = [link, title,content.strip()]
            sheet.append(row)
        except:
            continue

path = "results.xlsx"
wb.save(path)



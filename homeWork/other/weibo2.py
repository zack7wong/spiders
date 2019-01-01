import openpyxl
from openpyxl import Workbook
from bs4 import BeautifulSoup
from selenium import webdriver
import time

#     print(title.get_text())
wb = Workbook()
sheet = wb.active
sheet.title = 'Sheet1'


driver = webdriver.Chrome()
driver.get('https://weibo.com/?category=1760')

time.sleep(10)
driver.get('https://weibo.com/?category=1760')
time.sleep(5)
num = 1
for i in range(1,14):
    soup = BeautifulSoup(driver.page_source)
    # print(driver.page_source)
    titles = soup.select('h3[class="list_title_b"]')[((i-1)*8):]
    urls = soup.select('h3[class="list_title_b"] a')[((i-1)*8):]
    authors = soup.select('div[class="list_des"] div a span[class="subinfo S_txt2"]')[((i-1)*8):]
    times = soup.select('div[class="list_des"] div span[class="subinfo S_txt2"]')[((i-1)*8):]
    alls = soup.select('div[class="list_des"] div span[class="subinfo_rgt S_txt2"] em') [((i-1)*48):]
    print(titles)
    print(len(titles))
    print(alls)
    print(len(alls))
    likes = []
    comments = []
    zhuanfas = []
    for i in range(1,16,2):
        likes.append(alls[i])
    for i in range(17,32,2):
        comments.append(alls[i])
    for i in range(33,48,2):
        zhuanfas.append(alls[i])
    print(titles)
    print(likes)
    print(comments)
    print(zhuanfas)
    for title,url,author,mytime,like,comment,zhuanfa in zip(titles,urls,authors,times,likes,comments,zhuanfas):
        title = title.get_text()
        url = url.attrs['href']
        author = author.get_text()
        mytime = mytime.get_text()
        like = like.get_text()
        comment = comment.get_text()
        zhuanfa = zhuanfa.get_text()
        print(title,url,author,time,like,comment,zhuanfa)
        row = [num, title, url, author, mytime, like, comment, zhuanfa]
        sheet.append(row)
        num +=1
    driver.execute_script("window.scrollBy(0,1000)")
    driver.execute_script("window.scrollBy(0,1000)")
    driver.execute_script("window.scrollBy(0,1000)")
    driver.execute_script("window.scrollBy(0,1000)")
    driver.execute_script("window.scrollBy(0,-1000)")
    driver.execute_script("window.scrollBy(0,1000)")
    time.sleep(8)
# for url in urls:
#     print(url.attrs)
# for title in titles:

path = "results.xlsx"
wb.save(path)




# #请求头
# headers = {
#     'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     'Accept-Encoding': "gzip, deflate, br",
#     'Accept-Language': "zh-CN,zh;q=0.9",
#     'Cache-Control': "no-cache",
#     'Connection': "keep-alive",
#     'Cookie': "SINAGLOBAL=2741068042226.078.1532572562158; ALF=1564197669; SCF=AlH-htFhOOtuSJnrHnxgPfbVUuhc309qQH8-v0vpUXbAbnOJAXdyFYL75ERUfLp902-2ZhL-N-C5EPYHxHQaA3Y.; SUHB=0vJJ693_OWEkoX; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WF2Fpw_IYGa.AsddpW7kNnw; SUB=_2AkMst3o8f8NxqwJRmP4WzGnra4pxygzEieKa64vnJRMxHRl-yj83ql1ftRB6BzdU0q7brxMtYcVdjROQykm65y2CuSoO; login_sid_t=c3362b9c30d56616b37fdfb2bd627030; cross_origin_proto=SSL; YF-V5-G0=b4445e3d303e043620cf1d40fc14e97a; _s_tentry=www.google.com; UOR=www.google.ie,www.weibo.com,www.google.com; Apache=2472285430995.336.1545100310150; ULV=1545100310161:12:4:2:2472285430995.336.1545100310150:1544502363780; YF-Page-G0=e3ff5d70990110a1418af5c145dfe402; Ugrow-G0=56862bac2f6bf97368b95873bc687eef; WBStorage=bfb29263adc46711|undefined; wb_view_log=1920*10801",
#     'Host': "weibo.com",
#     'Pragma': "no-cache",
#     'Upgrade-Insecure-Requests': "1",
#     'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
#     'cache-control': "no-cache",
# }
# #请求url
# URL = 'https://weibo.com/a/aj/transform/loadingmoreunlogin?category=1760&page='
#
#
# import requests
# import json
# from lxml.etree import HTML
#
# #表头
# save = '序号,标题,链接,作者,时间,点赞数,评论数,转发数\n'
# with open('res.csv','w') as f:
#     f.write(save)
#
# account=1
# #翻页
# for page in range(1,14):
#     url = URL+str(page)
#     response = requests.get(url,headers=headers)
#     json_obj = json.loads(response.text)
#     html_str = json_obj['data']
#     html = HTML(html_str)
#     #lxml 的 xpath解析
#     titles = html.xpath('//div[@class="UG_list_b"]//h3[@class="list_title_b"]/a/text()')
#     hrefs = html.xpath('//div[@class="UG_list_b"]//h3[@class="list_title_b"]/a/@href')
#     authors = html.xpath('//div[@class="UG_list_b"]//div[@class="subinfo_box clearfix"]/a[2]/span[1]/text()')
#     times = html.xpath('//div[@class="UG_list_b"]//div[@class="subinfo_box clearfix"]/span[1]/text()')
#     likes = html.xpath('//div[@class="UG_list_b"]//div[@class="subinfo_box clearfix"]/span[2]/em[2]/text()')
#     comments = html.xpath('//div[@class="UG_list_b"]//div[@class="subinfo_box clearfix"]/span[4]/em[2]/text()')
#     zhufas = html.xpath('//div[@class="UG_list_b"]//div[@class="subinfo_box clearfix"]/span[6]/em[2]/text()')
#     for title,url,author,time,like,comment,zhufa in zip(titles,hrefs,authors,times,likes,comments,zhufas):
#         save = str(account)+','+title+','+url+','+author+','+time+','+like+','+comment+','+zhufa+'\n'
#         print(save)
#         with open('res.csv','a') as f:
#             f.write(save)
#         account+=1
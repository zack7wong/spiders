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
    if num==101:
        exit(0)
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


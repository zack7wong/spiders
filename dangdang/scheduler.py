import datetime
import json
import threading
from time import sleep
import multiprocessing
import config
import re
import time
import redis
import html as HT
from lxml import etree
from lxml.etree import HTML
from download import Download
from db import MysqlClient


class Scheduler(object):
    def __init__(self):
        self.download = Download()
        self.db = MysqlClient()

    def run(self):
        self.get_books()

    def get_books(self):
        kw = input('请输入要查找的书籍（例如:python编程）:')
        host_url = 'http://search.dangdang.com/?key={kw}&act=input&page_index={page}'

        #删除原有数据
        sql = 'delete from books'
        self.db.save(sql)


        for i in range(1, 10):
            print('当前页：'+str(i))
            start_url = host_url.format(kw=kw, page=i)
            print(start_url)
            response = self.download.get_html(start_url)
            response.encoding = 'gbk'
            # print(response.text)
            html = HTML(response.text)


            item_xpath_list = html.xpath('//div[@id="search_nature_rg"]/ul/li')

            for item in item_xpath_list:
                url = item.xpath('string(.//a[@name="itemlist-title"]/@href)')
                bookId = re.search('http://product.dangdang.com/(\d+).html',url)
                if bookId:
                    bookId = bookId.group(1)
                else:
                    bookId = ''
                title = item.xpath('string(.//a[@name="itemlist-title"]/@title)').strip()
                now_price = item.xpath('string(.//span[@class="search_now_price"]/text())').replace('¥','')
                old_price = item.xpath('string(.//span[@class="search_pre_price"]/text())').replace('¥','')
                discount = item.xpath('string(.//span[@class="search_discount"]/text())').replace('(','').replace(')','').replace('折','').strip()
                commentCount = item.xpath('string(.//a[@class="search_comment_num"]/text())').replace('条评论','')

                author = item.xpath('string(.//p[@class="search_book_author"]/span[1]/a/@title)')
                publishDateStr = item.xpath('string(.//p[@class="search_book_author"]/span[2]/text())').replace('/','').strip()
                publishing = item.xpath('string(.//p[@class="search_book_author"]/span[3]/a/text())')

                # print(url)
                # print(title)
                # print(now_price)
                # print(old_price)
                # print(discount)
                # print(commentCount)
                # print(author)
                # print(publishDateStr)
                # print(publishing)

                sql = "insert into books(bookId,url,title,now_price,old_price,discount,commentCount,publishDateStr,author,publishing)" \
                      " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                      % (bookId,url,title,now_price,old_price,discount,commentCount,publishDateStr,author,publishing) \
                      + "ON DUPLICATE KEY UPDATE title='%s'" % (title)
                print(sql)
                self.db.save(sql)


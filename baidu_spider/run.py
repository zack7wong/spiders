#!/usr/bin/env python
# -*- coding:utf-8 -*-

from baidu_spider import download, config,type_two


if __name__ == '__main__':
    spider = type_two.TypeTwoSpider()
    spider.get_urls()
    download = download.Download()
    for url_boj in spider.urls:
        print(url_boj)
        # response = download.driver_get_html(url_boj['url'])
        response = download.get_html(url_boj['url'])
        if response is None:
            print('该URL请求失败')
            print(url_boj['url'])
            with open('failed_urls.txt', 'a') as f:
                f.write(str(url_boj) + '\n')
        else:
            spider.parse_html(url_boj, response)
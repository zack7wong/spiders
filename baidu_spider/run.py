#!/usr/bin/env python
# -*- coding:utf-8 -*-

from baidu_spider import download, config, type_one, type_two


if __name__ == '__main__':
    spiderone = type_one.TypeOneSpider()
    spidertwo = type_two.TypeTwoSpider()
    spiderone.get_urls()
    spidertwo.get_urls()
    download = download.Download()

    #type1
    for url_boj in spiderone.urls:
        print(url_boj)
        response = download.get_html(url_boj['url'])
        if response is None:
            print('该URL请求失败')
            print(url_boj['url'])
            with open('failed_urls.txt', 'a') as f:
                f.write(str(url_boj) + '\n')
        else:
            spiderone.parse_html(url_boj, response)

    #type2
    # for url_boj in spidertwo.urls:
    #     print(url_boj)
    #     # response = download.driver_get_html(url_boj['url'])
    #     response = download.get_html(url_boj['url'])
    #     if response is None:
    #         print('该URL请求失败')
    #         print(url_boj['url'])
    #         with open('failed_urls.txt', 'a') as f:
    #             f.write(str(url_boj) + '\n')
    #     else:
    #         spidertwo.parse_html(url_boj, response)


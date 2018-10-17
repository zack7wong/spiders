#!/usr/bin/env python
# -*- coding:utf-8 -*-

import download
import re
import os
import config

class NewsSpider(object):
    def __init__(self):
        self.urls = []

    def get_urls(self):
        with open('urls.txt') as f:
            results = f.readlines()
            for res in results:
                url = res.split('|')[0]
                domian = res.split('|')[1]
                title = res.split('|')[2]
                keyword = res.split('|')[3]
                description = res.split('|')[4].strip()
                url_obj = {
                    'url':url,
                    'domain':domian,
                    'title':title,
                    'keyword':keyword,
                    'description':description,
                }
                self.urls.append(url_obj)

    def parse_html(self,url_boj,response):
        #处理编码问题
        charset = 'utf-8'
        try:
            try:
                search_res = re.search('meta.*?charset="(.*?)"', response.text)
                charset = search_res.group(1)
            except:
                search_res = re.search('meta.*?charset=(.*?)"', response.text)
                charset = search_res.group(1)
        except:
            pass
        response.encoding = charset
        html = response.text
        #抽取下载 image，js, css
        images_list = re.findall('<img.*?src="(.*?)"', html)
        css_list = re.findall('<link.*?href="(.*?)"', html)
        js_list = re.findall('<script.*?src="(.*?)"', html)
        self.parse_ressource(url_boj, images_list)
        self.parse_ressource(url_boj, css_list)
        self.parse_ressource(url_boj, js_list)
        #把引用地址替换
        html = self.replace_src(html,images_list)
        html = self.replace_src(html,css_list)
        html = self.replace_src(html,js_list)
        #删除原有的描述，keyword
        html = re.sub('<meta.*?name="description".*?>|<meta.*?name="keywords".*?>','',html)
        #增加描述,标题，keyword
        html = re.sub('<title>.*?</title>', '<title>{title}</title>'.format(title=url_boj['title']), html)
        end = re.search('</title>', html).span()[1]
        html = html[0:end] + config.keyword_text.replace('mydescription', url_boj['description']).replace('mykeywords', url_boj['keyword']) + html[end:]

        #增加固定代码
        res_html = re.sub('<a.*?href=".*?".*?>', '<a href="#">', html)
        res_html = re.sub("<a.*?href='.*?'.*?>", '<a href="#">', res_html)
        if '</body>' in res_html:
            begin = re.search('</body>', res_html).span()[0]
            res_html = res_html[0:begin] + config.html_text.replace('domain',url_boj['domain']) + res_html[begin:]
        elif '</html>' in res_html:
            begin = re.search('</html>', res_html).span()[0]
            res_html = res_html[0:begin] + config.html_text.replace('domain',url_boj['domain']) + res_html[begin:]
        else:
            res_html = res_html + config.html_text

        #保存文件
        pwd = os.getcwd()
        file_path = pwd + '/' + url_boj['domain']
        file_name = 'index.html'
        file_path_name = file_path + '/' + file_name
        with open(file_path_name, 'w', encoding=charset) as f:
            f.write(res_html)

    def parse_ressource(self,url_boj,ressource):
        for res in ressource:
            print(res)
            if res[0] == '/':
                if url_boj['url'][-1] == '/':
                    download_url = url_boj['url'] + res[1:]
                else:
                    download_url = url_boj['url'] + res
            elif res[0:2] == './':
                if url_boj['url'][-1] == '/':
                    download_url = url_boj['url'] + res[2:]
                else:
                    download_url = url_boj['url'] + res[1:]
            elif res[0:3] == '../':
                if url_boj['url'][-1] == '/':
                    download_url = url_boj['url'] + res[3:]
                else:
                    download_url = url_boj['url'] + res[2:]
            elif res[0:7] == 'http://' or res[0:8] == 'https://':
                download_url = res
            else:
                if url_boj['url'][-1] == '/':
                    download_url = url_boj['url'] + res
                else:
                    download_url = url_boj['url'] + '/' +res

            download.download_ressource(url_boj, download_url)

    def replace_src(self,html, results):
        for res in results:
            file_name = res.split('/')[-1]
            replace_str = './index/' + file_name
            html = html.replace(res, replace_str)
        return html

if __name__ == '__main__':
    spider = NewsSpider()
    spider.get_urls()
    download = download.Download()
    for url_boj in spider.urls:
        response = download.get_html(url_boj['url'])
        spider.parse_html(url_boj,response)
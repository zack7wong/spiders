#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lxml.etree import HTML
import aiohttp
import asyncio
import db
import re
import json

headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache,no-cache",
    'cookie': '_zap=50af1b98-7805-4c4a-8f05-9f1e3424b5a6; d_c0="ACAht9pWgw6PTqx9jfnwsW8fnM_wTXZJyHo=|1542112198"; z_c0="2|1:0|10:1542164496|4:z_c0|92:Mi4xSXA0cERRQUFBQUFBSUNHMzJsYUREaVlBQUFCZ0FsVk5FTjdZWEFBc3RuaVk2Nl9hTXQzWmIwZ2Rtcl9UNS1MTWhR|111bf9b6acdaf199673434d853a90d9d05fcf44c710304a8b60b435e528c0e3b"; __gads=ID=be1e735e6b592253:T=1542717011:S=ALNI_Ma38G5lweYYnzBFZf4g5_MKQOdA-A; q_c1=af449665f85f4fb78561d7ec006f88c5|1550749109000|1542116350000; tst=r; infinity_uid="2|1:0|10:1552048225|12:infinity_uid|28:MTA4NzQ0OTc1NzE2NDgwNjE0NA==|45833bd1f028ae44273553cd9b110157e95002b01b1a0de151990d3647cf08f3"; __utma=155987696.576827583.1552048227.1552048227.1552048227.1; __utmz=155987696.1552048227.1.1.utmcsr=zhihuapp|utmccn=zhi_three|utmcmd=button; __utmv=155987696.|1=userId=1087449757164806144=1; _xsrf=1c0dc0a9-1e33-446f-83ba-ac8241823e9d',
    'pragma': "no-cache",
    'referer': "https://www.zhihu.com/topic/19592502/questions",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    'Postman-Token': "aad7f6e7-9f9d-4b99-a39e-fefda8b1aa7a"
    }


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:

        mysql_cli = db.MysqlClient()
        item_list = []
        with open('zhihu_id.txt') as f:
            results = f.readlines()
            for res in results:
                id = res.split(',')[0]
                question = res.split(',')[1]
                obj ={
                    'id':id,
                    'question':question,
                }
                item_list.append(obj)

        for obj in item_list:
            print(obj['id'])
            url = 'https://www.zhihu.com/question/' + obj['id']
            print(url)
            response = await fetch(session, url)

            jsonStr = re.search('<script id="js-initialData".*?>(.*?)</script>',response).group(1)
            json_obj = json.loads(jsonStr)
            print(json.dumps(json_obj))

            for data in json_obj['initialState']['entities']['questions']:
                questionAuthor = json_obj['initialState']['entities']['questions'][data]['author']['name']
                questionAuthorId = json_obj['initialState']['entities']['questions'][data]['author']['urlToken']
                questionAuthor_hashId = json_obj['initialState']['entities']['questions'][data]['author']['id']

                save_re = questionAuthor.replace(',','，') + ',' + questionAuthorId + ',' + questionAuthor_hashId + '\n'
                with open('author.txt', 'a') as f:
                    f.write(save_re)

            for data in json_obj['initialState']['entities']['answers']:
                question = obj['question']

                answerId = str(json_obj['initialState']['entities']['answers'][data]['id'])
                answer = json_obj['initialState']['entities']['answers'][data]['content']

                html = HTML(answer)
                content_list = html.xpath('//text()')
                answer = ''.join(content_list)
                answerAuthor = json_obj['initialState']['entities']['answers'][data]['author']['name']
                answerAuthorId = json_obj['initialState']['entities']['answers'][data]['author']['urlToken']
                answerAuthor_hashId = json_obj['initialState']['entities']['answers'][data]['author']['id']
                commentCount = str(json_obj['initialState']['entities']['answers'][data]['commentCount'])
                likeCount = str(json_obj['initialState']['entities']['answers'][data]['voteupCount'])

                # print(question)
                # print(answerId)
                # print(answer)
                # print(answerAuthor)
                # print(answerAuthorId)
                # print(answerAuthor_hashId)
                # print(commentCount)
                # print(likeCount)

                save_re = answerAuthor.replace(',','，')+','+answerAuthorId+','+answerAuthor_hashId+'\n'
                with open('author.txt', 'a') as f:
                    f.write(save_re)

                sql = "insert into questionDetail(question,answerId,answer,answerAuthor,answerAuthorId,answerAuthor_hashId,commentCount,likeCount)" \
                      " VALUES ('%s', '%s', '%s','%s', '%s', '%s','%s', '%s')" \
                      % (question,answerId,answer,answerAuthor,answerAuthorId,answerAuthor_hashId,commentCount,likeCount)
                print(sql)

                mysql_cli.save(sql)



loop = asyncio.get_event_loop()
loop.run_until_complete(main())
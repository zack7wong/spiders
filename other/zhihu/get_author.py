import aiohttp
import asyncio
import json
import db
import math

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:

        mysql_cli = db.MysqlClient()
        item_list = []
        with open('author.txt') as f:
            results = f.readlines()
            for res in results:
                name = res.split(',')[0]
                if name == '匿名用户' or name == '知乎用户':
                    continue
                authorId = res.split(',')[1]
                obj = {
                    'name': name,
                    'authorId': authorId,
                }
                item_list.append(obj)

        for obj in item_list:
            print(obj)
            name = obj['name']
            authorId = obj['authorId']

            start_url = 'https://www.zhihu.com/api/v4/members/{authorId}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit={pageToken}'
            url = start_url.format(authorId=authorId,pageToken=0)
            response = await fetch(session, url)
            print(response)

            json_obj = json.loads(response)
            if 'paging' not in json_obj:
                continue

            total = json_obj['paging']['totals']
            if total == 0:
                continue

            #处理第一页
            for data in json_obj['data']:
                followName = data['name']
                sql = "insert into author(name,followName)" \
                      " VALUES ('%s', '%s')" \
                      % (name,followName)
                print(sql)
                mysql_cli.save(sql)

            pageNum = math.ceil(total/20)

            #获取其他页数
            for i in range(1,pageNum+1):
                pageToken = i*20
                url = start_url.format(authorId=authorId, pageToken=pageToken)
                response = await fetch(session, url)
                print(response)

                json_obj = json.loads(response)

                for data in json_obj['data']:
                    followName = data['name']
                    sql = "insert into author(name,followName)" \
                          " VALUES ('%s', '%s')" \
                          % (name, followName)
                    print(sql)
                    mysql_cli.save(sql)



        # for i in range(40):
        #     url = start_url.format(pageToken=i * 10)
        #     html = await fetch(session, url)
        #     print(html)
        #     json_obj = json.loads(html)
        #     for data in json_obj['data']:
        #         id = str(data['target']['id'])
        #         title = str(data['target']['title'])
        #         name = str(data['target']['author']['name'])
        #         save_re = id+','+title.replace(',','，')+','+name.replace(',','，')+'\n'
        #         print(save_re)
        #         with open('zhihu_id.txt','a') as f:
        #             f.write(save_re)
        #
        #         sql = "insert into question(postId,title,name)" \
        #               " VALUES ('%s', '%s', '%s')" \
        #               % (id,title,name)
        #         print(sql)
        #
        #         mysql_cli.save(sql)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
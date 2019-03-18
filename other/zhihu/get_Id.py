import aiohttp
import asyncio
import json
import db

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        start_url = 'https://www.zhihu.com/api/v4/topics/19592502/feeds/timeline_question?include=data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=article)].target.content,voteup_count,comment_count,voting,author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=people)].target.answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics;data[?(target.type=answer)].target.annotation_detail,content,hermes_label,is_labeled,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=answer)].target.author.badge[?(type=best_answerer)].topics;data[?(target.type=article)].target.annotation_detail,content,hermes_label,is_labeled,author.badge[?(type=best_answerer)].topics;data[?(target.type=question)].target.annotation_detail,comment_count;&limit=10&offset={pageToken}'

        mysql_cli = db.MysqlClient()
        for i in range(40):
            url = start_url.format(pageToken=i * 10)
            html = await fetch(session, url)
            print(html)
            json_obj = json.loads(html)
            for data in json_obj['data']:
                id = str(data['target']['id'])
                title = str(data['target']['title'])
                name = str(data['target']['author']['name'])
                save_re = id+','+title.replace(',','，')+','+name.replace(',','，')+'\n'
                print(save_re)
                with open('zhihu_id.txt','a') as f:
                    f.write(save_re)

                sql = "insert into question(postId,title,name)" \
                      " VALUES ('%s', '%s', '%s')" \
                      % (id,title,name)
                print(sql)

                mysql_cli.save(sql)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
#导入包
import requests
import json
from lxml.etree import HTML

#起始url
URL = 'https://weibo.com/a/aj/transform/loadingmoreunlogin?category=1760&page={page}'

#初始化文件信息
save = '序号,标题,链接,作者,时间,点赞数,评论数,转发数\n'
#写文件
with open('results.csv','w') as f:
    f.write(save)

#初始化序号值
num=1
#for循环遍历，取14页的内容
for i in range(1,14):
    #每一页的请求url
    start_url = URL.format(page=str(i))
    #发送请求
    response = requests.get(start_url)
    #解析返回的json数据
    json_obj = json.loads(response.text)
    #获取html标签数据
    html_str = json_obj['data']
    #lxml解析
    html = HTML(html_str)

    #获取标题
    titles = html.xpath('//div[@class="UG_list_b"]//h3/a/text()')
    #获取链接
    hrefs = html.xpath('//div[@class="UG_list_b"]//h3/a/@href')
    #获取作者
    authors = html.xpath('//div[@class="UG_list_b"]//div[@class="subinfo_box clearfix"]/a[2]/span[1]/text()')
    # 获取时间
    times = html.xpath('//div[@class="UG_list_b"]//div[@class="subinfo_box clearfix"]/span[1]/text()')
    # 获取点赞数
    likes = html.xpath('//div[@class="UG_list_b"]//div[@class="subinfo_box clearfix"]/span[2]/em[2]/text()')
    # 获取评论数
    comments = html.xpath('//div[@class="UG_list_b"]//div[@class="subinfo_box clearfix"]/span[4]/em[2]/text()')
    # 获取转发数
    zhufas = html.xpath('//div[@class="UG_list_b"]//div[@class="subinfo_box clearfix"]/span[6]/em[2]/text()')
    #将这几条数据合并
    for title,url,author,time,like,comment,zhufa in zip(titles,hrefs,authors,times,likes,comments,zhufas):
        #存储的结果拼接
        save = str(num)+','+title+','+url+','+author+','+time+','+like+','+comment+','+zhufa+'\n'
        #符号转换
        save = save.replace(',','，')
        print(save)
        #写文件
        with open('results.csv','a') as f:
            f.write(save)
        #序号加1
        num+=1
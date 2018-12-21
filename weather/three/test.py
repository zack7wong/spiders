import requests

url = "http://219.146.175.226:8406/webs/ajax/WasteWater/QueryAnalysis/HistoryReportQUIDYN/HistoryReport.ashx"

payload = "Method=QueryHistoryReport&subid=1671&subname=%E4%B8%9C%E6%98%8E%E7%9F%B3%E5%8C%96%E9%9B%86%E5%9B%A2&start=2018-12-19+00%3A00%3A00&end=2018-12-20+23%3A59%3A59&index=1&sort=1&showValidate=0&multiCode=311%2C313%2C316%2C466%2C494&showUpload=0&YWGS=&codes=302%2C311%2C316%2C494%2C495&page=1&rows=20"
headers = {
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Length': "293",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Cookie': "autoLogin=null; user=null; pwd=null; ASP.NET_SessionId=mgo1ur55g1yfwvqjpz251hb4",
    'Host': "219.146.175.226:8406",
    'Origin': "http://219.146.175.226:8406",
    'Pragma': "no-cache",
    'Referer': "http://219.146.175.226:8406/webs/WasteWater/QueryAnalysis/HistoryReportQUIDYN/HistoryReport.aspx",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'cache-control': "no-cache",
    'Postman-Token': "15ee7101-9fb4-4b05-b897-4aa8c8048cb6"
    }

proxies={
    'http':'http://127.0.0.1:9999'
}

response = requests.request("POST", url, data=payload, headers=headers,proxies=proxies)

print(response.text)


# import aiohttp
# import asyncio
#
# async def fetch(session, url):
#     async with session.post(url,headers=headers,data=payload) as response:
#         return await response.text()
#
# async def main():
#     async with aiohttp.ClientSession() as session:
#         html = await fetch(session, "http://219.146.175.226:8406/webs/ajax/WasteWater/QueryAnalysis/HistoryReportQUIDYN/HistoryReport.ashx")
#         print(html)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
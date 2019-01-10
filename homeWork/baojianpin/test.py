#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :        hayden_huang
   Date：          2018/12/25 18:23
-------------------------------------------------
"""

import requests

url = "http://app1.sfda.gov.cn/datasearch/face3/content.jsp"

querystring = {"tableId":"30","tableName":"TABLE30","tableView":"%B9%FA%B2%FA%B1%A3%BD%A1%CA%B3%C6%B7","Id":"8252","MmEwMD":"GBK-26k_P8toYN9.P.Afkusm3.3H3mnWvzZeSkogTMdE7fx9wDH6cuVnHP82cPxfJLUDqdC._cEFdlU5uS6sO44_fz7NE.E_fUCLFVAkvvcNrc2rSkdys.tPm.6xiv7N.QEHrO2V75lrDW0NpwAnyKuJPbjAdB9yMDc0G4CCsW3wV8YeetIWCLasqHKOy0vKk03thkDsgrgmth8OechQwGVei5xo2eJ7CQB_ntkQ1sZTVddHEnOezcH_YE21QjQF77oZX2pnYOIi839n3CMS_cxiasvBdXG9rMZTbhyCbo4FvqBM3iHsjlR2v9dOIU3GTaDuoofitQ1T0nt0N80c.zyY9_PyyImH5ah3.t7ldNUl6nHgXsafq.TxmYwjm3MoRiVGi8RvlWyZKrTlLoQuWZhQkySeD4pQoT8jJRWRecEbcrJ3UG9"}

payload = ""
headers = {
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Type': "text/html;encoding=gbk",
    'Cookie': "JSESSIONID=80DA45B3399F3188A340C73186AE9107.7; FSSBBIl1UgzbN7N82S=wRHqUsTAHx8QQ4i5DA66H7EehCpI.ocuNF9Y_J0Vv4Oy1WcVMwwXX9riPVt.kLil; security_session_verify=507450bc9197ab115d5a0b7848fe6dee; FSSBBIl1UgzbN7N82T=2erFtVEveObhtf1r.yp2afFBaHa7Hv5wRxm3wpeLl.hlTWJUjyK1vLQmjLhr2PYbLT0h1Et_UiY8M4TuhSyFxvXxGMtV9fj3JwBZC9_BgyHsDyZBiVGkd1TnrMcI_160o3LWUU1tziaNcH5KtBAJooUdK2iKtkEJEicPRf_vQSjjQEGPp2.TkeqE.T5iiqXGI.qOmLROVdBcsFj9mig.qbvOvekUrXiWH01bzPAijWtE8Gm6NUCzCeM6eOdWkcGYxim96pw2wStFzjlmxCFWWXSgoluqYvCuaP4qEuvLZu0WSqQNPZFwPw2YfZ5IVYa7kCbd20lbfUTaqNOvEJZpQqqZr.KibJxVbAua9w52GYrIZ.q",
    'Host': "app1.sfda.gov.cn",
    'Pragma': "no-cache",
    'Referer': "http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=30&tableName=TABLE30&title=%B9%FA%B2%FA%B1%A3%BD%A1%CA%B3%C6%B7&bcId=118103385532690845640177699192",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "d05b5086-1a5c-4cf4-8c3e-01b52be708ef"
    }

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

print(response.text)
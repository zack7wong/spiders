import requests
import http.cookiejar
import os
import time
import re
import logging
from config import account
from config import cookies
from urllib.parse import urljoin
import json

url = "http://readfree.me"
post_url = "https://readfree.me/accounts/login/?next=/"
current_path = os.path.dirname(os.path.abspath(__file__))
cookies_path = os.path.join(current_path, "readfree.cookies")
logfile_path = os.path.join(current_path, "readfree.log")
captcha_path = os.path.join(current_path, "captcha.png")

headers = {}
headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/51.0"
s = requests.Session()
s.headers.update(headers)

logging.basicConfig(filename=logfile_path, level='DEBUG')
date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
logging.info("===============Log Started at " + date + "===============")


def load_cookies():
    load_cj = http.cookiejar.LWPCookieJar()
    load_cj.load(cookies_path, ignore_expires=True, ignore_discard=True)
    load_ck = requests.utils.dict_from_cookiejar(load_cj)
    return load_ck


def save_cookies(cookies):
    save_cj = http.cookiejar.LWPCookieJar()
    save_ck = {c.name: c.value for c in cookies}
    requests.utils.cookiejar_from_dict(save_ck, save_cj)
    save_cj.save(cookies_path, ignore_expires=True, ignore_discard=True)
    logging.info('Cookies updated.')


def process_cookies():
    save_cj = http.cookiejar.LWPCookieJar()
    requests.utils.cookiejar_from_dict(cookies, save_cj)
    save_cj.save(cookies_path, ignore_expires=True, ignore_discard=True)
    logging.info('Cookies generated.')


def login_by_cookies():
    ck = load_cookies()
    s.cookies.update(ck)
    req = s.get(url)
    if req.status_code == 200:
        save_cookies(s.cookies)
        logging.info("=============Login by cookies successfully at %s =============" % date)
    else:
        logging.warning('Cookies expired, please update the cookies')


def login():
    s.headers = {}
    headers = {}
    headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/51.0"
    s.headers.update(headers)
    # print(s.headers)
    req = s.get(url)
    captcha_url = re.findall(r'<img src="(.*?)"', req.text)[0]
    captcha_url = urljoin(url, captcha_url)
    req2 = s.get(captcha_url)
    with open(captcha_path, 'wb') as f:
        f.write(req2.content)
        logging.info('Captcha saved.')

    headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
        'Content-Length': "198",
        'Content-Type': "application/x-www-form-urlencoded",
        # 'Cookie': "csrftoken=f9JGfvmCjBC8AwvukUy4KCUC0YVd253w8rjHwIqCUVJWbm4lyORoVhqForQmS5cA; Hm_lvt_375aa6d601368176e50751c1c6bf0e82=1547555195; Hm_lpvt_375aa6d601368176e50751c1c6bf0e82=1547601746",
        'Host': "readfree.me",
        'Origin': "https://readfree.me",
        'Pragma': "no-cache",
        'Referer': "https://readfree.me/accounts/login/?next=/",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        'cache-control': "no-cache",
    }
    s.headers.update(headers)

    # form_data = {}
    # form_data['email'] = account['email']
    # form_data['password'] = account['password']
    # form_data['captcha_0'] = re.findall(r'name="captcha_0".*?value="(.*?)"', req.text)[0]
    # form_data['csrfmiddlewaretoken'] = re.findall(r"name='csrfmiddlewaretoken' value='(.*?)'", req.text)[0]
    # form_data['captcha_1'] = input('Please open captcha.png and input it:')
    #
    # print(form_data)

    dataStr = 'csrfmiddlewaretoken={csrfmiddlewaretoken}&email={email}&password={password}&captcha_0={captcha_0}&captcha_1={captcha_1}'
    csrfmiddlewaretoken = re.findall(r"name='csrfmiddlewaretoken' value='(.*?)'", req.text)[0]
    captcha_0 = re.findall(r'name="captcha_0".*?value="(.*?)"', req.text)[0]
    captcha_1 = input('请刷新图片输入验证码:')

    form_data = dataStr.format(csrfmiddlewaretoken=csrfmiddlewaretoken,email=account['email'],password=account['password'],captcha_0=captcha_0,captcha_1=captcha_1)
    # print(form_data)
    # req2 = s.post(post_url, json.dumps(form_data), allow_redirects=False, verify=False)
    req2 = s.post(post_url, form_data, allow_redirects=False, verify=False)
    # print(req2.status_code)
    # print(req2.text)
    # save_cookies(s.cookies)
    if req2.status_code != 302:
        logging.info('Login failed.')
        print('登录失败，验证码或者账号密码错误')
        return False
    else:
        headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            # 'Cookie': "Hm_lvt_375aa6d601368176e50751c1c6bf0e82=1547555195; Hm_lpvt_375aa6d601368176e50751c1c6bf0e82=1547601746; sessionid=a7xrz7vwpanlsd2yho9g0ehcwh9l6qqk; csrftoken=FVzB06dnkFo0ieNwtg0oVoj8zdz6blwyyDw51jWZzWO1Sso4uH6LeNnwf1yfBYcK",
            'Host': "readfree.me",
            'Pragma': "no-cache",
            'Referer': "https://readfree.me/accounts/login/?next=/",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            'cache-control': "no-cache",
        }
        s.headers.update(headers)
        s.get(url)
        logging.error('Login successfully.')
        print('登录成功')
        save_cookies(s.cookies)
        return True


def main():
    if os.path.exists(cookies_path):
        print('使用cookie登录')
        login_by_cookies()
    elif (cookies["csrftoken"] != "") & (cookies["sessionid"] != ""):
        process_cookies()
        login_by_cookies()
    else:
        while True:
            flag = login()
            if flag is True:
                break


if __name__ == '__main__':
    main()

#当前请求次数
REQUEST_NUM = 0

#请求多少次后换IP配置
CHANGE_IP = 50

#代理IP
IP_URL = ''

START_URL = 'https://ahrefs.com/site-explorer/overview/v2/subdomains/live?target={url}'


#是否开启代理
PROXY_SWITCH = True
#是否使用cookies
COOKIES_SWITCH = False
#请求最大出错次数
ERROR_MAX = 3

#请求头配置
HEADERS = {
    'connection': "keep-alive",
    'cache-control': "max-age=0",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'cookie':'_iub_cs-794932=%7B%22consent%22%3Atrue%2C%22timestamp%22%3A%222018-11-26T07%3A13%3A14.264Z%22%2C%22version%22%3A%221.2.4%22%2C%22id%22%3A794932%7D; _fbp=fb.1.1543227556011.1520211835; ljs-lang=zh; XSRF-TOKEN=eyJpdiI6ImFlZTJGbXEzdmsyMXF6REZXZnRmSlE9PSIsInZhbHVlIjoibzl4OVA2UHpmRDVWZXdxVHFjTEdEajJ1a2hRK2N0OG1QV3o2Q0ljdGo3MXJ1a0R1d1ZiVHlWVVNzUHRcL2M3Q0l4WGhDUG9NRjdKV0ttNU5PekplaGt3PT0iLCJtYWMiOiI0Njk3YmNkNzg5Njc1NThhMjA2Yjk5ZWU0ZDExM2FlODQ4ODQ3MDM3NzQwNjI0ZjhjYzU1YjU2NDgwZjU1ZTM1In0%3D; ahrefs_cookie=eyJpdiI6IjQrWlZuV0diNFFZU3hcL3Z5S2tYeVZBPT0iLCJ2YWx1ZSI6ImR1MWo3WnRmRjNxaVB6Nkc2eFlMR3EwVFpVcWExVEd4Y2lPNXpINzF3VktHdDZHbUdBTFpyZVF4cTRGclwvbEQyK1FPQ1M5d1k0QTRGRlBtN09tTlJTUT09IiwibWFjIjoiN2IzODc5MTM2YjJhMWQwMThmZjRjMjczMTNiMzRmODlhYzg1YTQ2OWVjMWNhOTRkMDg5ZmZiZjU5NjExZTYyNSJ9; intercom-session-dic5omcp=Z2xoZ3FsRFhMT0ZqQ2VUeVpkZ1o3Q3hlWURiQjBJeEFtMzk5RXFFSTlNT2w3YVdBVzd4ak9XbnZnbzIwalV3Ri0tNFFsV2FEazMwRjM3NTlxMDJyZGpXUT09--e3e7fad78d38bbecb66ffa2d690a70ea475b5731'
}

XMLHttpRequest_HEADERS = {
'connection': "keep-alive",
    'cache-control': "max-age=0",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'cookie':'_iub_cs-794932=%7B%22consent%22%3Atrue%2C%22timestamp%22%3A%222018-11-26T07%3A13%3A14.264Z%22%2C%22version%22%3A%221.2.4%22%2C%22id%22%3A794932%7D; _fbp=fb.1.1543227556011.1520211835; ljs-lang=zh; XSRF-TOKEN=eyJpdiI6ImFlZTJGbXEzdmsyMXF6REZXZnRmSlE9PSIsInZhbHVlIjoibzl4OVA2UHpmRDVWZXdxVHFjTEdEajJ1a2hRK2N0OG1QV3o2Q0ljdGo3MXJ1a0R1d1ZiVHlWVVNzUHRcL2M3Q0l4WGhDUG9NRjdKV0ttNU5PekplaGt3PT0iLCJtYWMiOiI0Njk3YmNkNzg5Njc1NThhMjA2Yjk5ZWU0ZDExM2FlODQ4ODQ3MDM3NzQwNjI0ZjhjYzU1YjU2NDgwZjU1ZTM1In0%3D; ahrefs_cookie=eyJpdiI6IjQrWlZuV0diNFFZU3hcL3Z5S2tYeVZBPT0iLCJ2YWx1ZSI6ImR1MWo3WnRmRjNxaVB6Nkc2eFlMR3EwVFpVcWExVEd4Y2lPNXpINzF3VktHdDZHbUdBTFpyZVF4cTRGclwvbEQyK1FPQ1M5d1k0QTRGRlBtN09tTlJTUT09IiwibWFjIjoiN2IzODc5MTM2YjJhMWQwMThmZjRjMjczMTNiMzRmODlhYzg1YTQ2OWVjMWNhOTRkMDg5ZmZiZjU5NjExZTYyNSJ9; intercom-session-dic5omcp=Z2xoZ3FsRFhMT0ZqQ2VUeVpkZ1o3Q3hlWURiQjBJeEFtMzk5RXFFSTlNT2w3YVdBVzd4ak9XbnZnbzIwalV3Ri0tNFFsV2FEazMwRjM3NTlxMDJyZGpXUT09--e3e7fad78d38bbecb66ffa2d690a70ea475b5731',
    'x-requested-with': 'XMLHttpRequest'
}
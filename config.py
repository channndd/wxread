# config.py 自定义配置
import os
import re

"""
github action部署或本地部署
从环境变量获取值,如果不存在使用默认本地值
每一次代表30秒，比如你想刷1个小时这里填120，你只需要签到这里填2次
"""

# 阅读次数 默认120次/60分钟
READ_NUM = int(os.getenv('READ_NUM', '480'))
# pushplus or telegram
PUSH_METHOD = "" or os.getenv('PUSH_METHOD')
# push-plus
PUSHPLUS_TOKEN = "" or os.getenv("PUSHPLUS_TOKEN")
# telegram
TELEGRAM_BOT_TOKEN = "" or os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "" or os.getenv("TELEGRAM_CHAT_ID")
# 复制的curl_bath命令
curl_str = os.getenv('WXREAD_CURL')

# 对应替换
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'baggage': 'sentry-environment=production,sentry-release=dev-1738835404736,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=e6d8981aa07947b58a4ddbcd3bfbeb98',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://weread.qq.com',
    'priority': 'u=1, i',
    'referer': 'https://weread.qq.com/web/reader/b6632b2071bf49e5b66c4b7k02e32f0021b02e74f10ece8',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'e6d8981aa07947b58a4ddbcd3bfbeb98-931e995311a0c82f',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}
#
# #对应替换
cookies = {}

# 保留| 默认读三体，其它书籍自行测试时间是否增加
# data = {
#     "appId": "wb182564874663h152492176",
#     "b": "ce032b305a9bc1ce0b0dd2a",
#     "c": "7cb321502467cbbc409e62d",
#     "ci": 70,
#     "co": 0,
#     "sm": "[插图]第三部广播纪元7年，程心艾AA说",
#     "pr": 74,
#     "rt": 30,
#     "ts": 1727660516749,
#     "rn": 31,
#     "sg": "991118cc229871a5442993ecb08b5d2844d7f001dbad9a9bc7b2ecf73dc8db7e",
#     "ct": 1727660516,
#     "ps": "b1d32a307a4c3259g016b67",
#     "pc": "080327b07a4c3259g018787",
# }
data = {
    'appId': 'wb182564874663h1964571299',
    'b': 'b6632b2071bf49e5b66c4b7',
    'c': '02e32f0021b02e74f10ece8',
    'ci': 27,
    'co': 377,
    'sm': '§351有色盲，也有确定色盲的方法。一般',
    'pr': 98,
    'rt': 35,
    'ts': 1741848470676,
    'rn': 208,
    'sg': 'd4d2f013368dfc004ccac4850619b362935c21d582182b924312e3bc3dc36bfa',
    'ct': 1741848470,
    'ps': '08f321807a61d97cg015fd4',
    'pc': 'f3d32c407a61d980g016bb6',
    's': '65f94d8a'
}


def convert(curl_command):
    """提取bash接口中的headers与cookies
    支持 -H 'Cookie: xxx' 和 -b 'xxx' 两种方式的cookie提取
    """
    # 提取 headers
    headers_temp = {}
    for match in re.findall(r"-H '([^:]+): ([^']+)'", curl_command):
        headers_temp[match[0]] = match[1]

    # 提取 cookies
    cookies = {}
    
    # 从 -H 'Cookie: xxx' 提取
    cookie_header = next((v for k, v in headers_temp.items() 
                         if k.lower() == 'cookie'), '')
    
    # 从 -b 'xxx' 提取
    cookie_b = re.search(r"-b '([^']+)'", curl_command)
    cookie_string = cookie_b.group(1) if cookie_b else cookie_header
    
    # 解析 cookie 字符串
    if cookie_string:
        for cookie in cookie_string.split('; '):
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()
    
    # 移除 headers 中的 Cookie/cookie
    headers = {k: v for k, v in headers_temp.items() 
              if k.lower() != 'cookie'}

    return headers, cookies


headers, cookies = convert(curl_str) if curl_str else (headers, cookies)

import random, requests, httpx
import logging
from fish_tool.log_tool import logs, InfoError


# 代理验证信息
web_info = '115.231.107.229:6460:16WASOTM:085764'
web_infos = web_info.split(':')
proxyUser = web_infos[2]  # "16WASOTM"
proxyPass = web_infos[3]  # "085764"
proxyHost = f'{web_infos[0]}:{web_infos[1]}'  # "115.231.107.229:6460"

proxyMeta = f'http://{proxyUser}:{proxyPass}@{proxyHost}'

ua_list = [
    'Mozilla/5.0 (compatible; MSIE 10.0; qdesk 2.4.1266.203; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0; Touch; MAARJS)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; Touch; QQBrowser/8.0.3345.400)',
    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/601.5.17 (KHTML, like Gecko) Version/9.1 Safari/601.5.17',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.68 Safari/534.24',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.31 (KHTML, like Gecko) Chrome/13.0.748.0 Safari/534.31',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.801.0 Safari/535.1',
]


def get(url, proxy=False):
    ua = random.choice(ua_list)
    headers = {'User-Agent': ua}
    if proxy:
        tunnel = random.randint(1, 900000)
        headers["Proxy-Tunnel"] = str(tunnel)
        proxies = {"http": proxyMeta, "https": proxyMeta}
    else:
        proxies = None
    resp = requests.get(url, proxies=proxies, headers=headers, timeout=3)
    return resp


async def async_get(url, proxy=False):
    tunnel = random.randint(1, 800000)
    ua = random.choice(ua_list)
    headers = {"Proxy-Tunnel": str(tunnel), 'User-Agent': ua}
    if proxy:
        proxies = {"http": proxyMeta, "https": proxyMeta}
    else:
        proxies = None
    async with httpx.AsyncClient(proxies=proxies, headers=headers, timeout=3) as client:
        # resp = await client.get(url, headers=headers, timeout=3)
        resp = await client.get(url)
    return resp

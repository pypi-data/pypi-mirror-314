from typing import Union
import time
import os
import requests
from urllib.parse import urljoin
import urllib.request
import lxml.etree
import aiofiles
from fish_tool import sys_tool
from fish_tool.net.proxy_16yun import async_get
from fish_tool.log_tool import logs, InfoError

html_char__file_char = {  # 支持windows文件系统 也支持压缩成zip文件
    '/': '·┇',
    '\t': '·t',
    '\\': '·┊',
    '?': '·？',
    ' ': '·▅',
    ':': '·▋',
    '*': '·▆',
    '"': "·'",
    '|': '·▎',
    '<': '·〈',
    '>': '·〉',
}
start__file_char = [
    ('https://', '·S'),
    ('http://', '·H'),
]


def decode_content(content):
    try:
        return content.decode('utf8')
    except Exception as e:
        return str(content)


def _get(url, headers=None, cookies=None, timeout=None):
    kv = {}
    if timeout is not None:
        kv['timeout'] = timeout
    if cookies is not None:
        kv['cookies'] = cookies
    response = requests.get(url, headers=headers, verify=False, **kv)
    return response


def get(url, headers=None, cookies=None, timeout=None, show_log=True, repeat=3, try_sleep=0) -> Union[requests.Response, None]:
    e = None
    for i in range(repeat):
        try:
            response = _get(url, headers=headers, cookies=cookies, timeout=timeout)
            if show_log or response.status_code != 200:
                max_len = 120 if response.status_code == 200 else 1200
                logs.all.info(f'{sys_tool.stacks_to_txt(stop_index=-2)} GET {url} code={response.status_code} '
                              f'response={decode_content(response.content)[:max_len]}')
            return response
        except Exception as error:
            e = error
            if try_sleep:
                time.sleep(try_sleep)
    logs.all.error(f'{sys_tool.stacks_to_txt(stop_index=-2)} GET {url} error={e}')
    return


def _post(url, jsondata=None, files=None, data=None, stream=False, headers=None, cookies=None, timeout=None):
    kv = {}
    if timeout is not None:
        kv['timeout'] = timeout
    if cookies is not None:
        kv['cookies'] = cookies
    response = requests.post(url, json=jsondata, files=files, data=data, stream=stream, headers=headers, verify=False, **kv)
    return response


def post(url, jsondata=None, files=None, data=None, stream=False, headers=None,
         cookies=None, timeout=None, show_log=True, repeat=3, try_sleep=0) -> Union[requests.Response, None]:
    e = None
    for i in range(repeat):
        try:
            start = time.time()
            response = _post(url, jsondata, files=files, data=data, stream=stream, headers=headers, cookies=cookies, timeout=timeout)
            if show_log or response.status_code != 200:
                max_len = 120 if response.status_code == 200 else 1200
                logs.all.info(f'{sys_tool.stacks_to_txt(stop_index=-2)} POST {url} code={response.status_code} '
                              f'response={decode_content(response.content)[:max_len]} spend={time.time() - start:0.3f}')
            return response
        except Exception as error:
            e = error
            if try_sleep:
                time.sleep(try_sleep)
    logs.all.error(f'{sys_tool.stacks_to_txt(stop_index=-2)} POST {url} error={e}')
    return


def root(*paths):
    path = os.path.join(os.path.dirname(__file__), '../../', *paths)
    return os.path.abspath(path)


def html_to_file_name(html_name):
    file_name = urllib.request.unquote(html_name)  # url编码转成中文
    for start, char in start__file_char:
        if file_name.startswith(start):
            file_name = file_name.replace(start, char)

    for html_char, file_char in html_char__file_char.items():
        file_name = file_name.replace(html_char, file_char)
    return file_name


def file_to_html_name(file_name):
    pre = ''
    for start_html, start_char in start__file_char:
        if file_name.startswith(start_char):
            pre = start_html
            file_name = file_name.replace(start_char, '')
    for html_char, file_char in html_char__file_char.items():
        file_name = file_name.replace(file_char, html_char)
    html_name = pre + urllib.request.quote(file_name)  # 中文转成url编码
    return html_name


def _test_file_name():
    assert len(set(html_char__file_char.values())) == len(html_char__file_char)
    for url in [
        'https://www.bilibili.com/video/BV1cA{41}1s7Kz',
        'https://www.ciweimao.com/book_list/weilai<huan>xiang/',
        'http://www.xiaolvji.com/u/aif(i)sh'
    ]:
        file = html_to_file_name(url)
        url2 = file_to_html_name(file)
        if url2 != url:
            logs.brief.info(f'Error {url2} {url}')
        logs.brief.info(f'{file} ===> {url2}')


async def async_read(path, encoding="utf-8"):
    async with aiofiles.open(path, encoding=encoding) as f:
        return await f.read()


async def async_write(txt, path, mod='w', encoding="utf-8"):
    assert mod in ['w', 'a']
    async with aiofiles.open(path, mod, encoding=encoding) as f:
        await f.write(txt)


async def async_write_html(url, path, charset=None, proxy=False):
    resp = await async_get(url, proxy=proxy)
    if charset:
        text = resp.content.decode(charset, "ignore")
        await async_write(text, path, mod='w', encoding=charset)
    else:
        text = resp.text
        await async_write(text, path, mod='w', encoding="utf-8")


class Enode:
    def __init__(self, html, url='', tree=None):
        """
        :param html: 网页的文本内容
        :param url:  网页地址
        """
        if tree is None:
            self.tree = lxml.etree.HTML(html)
        else:
            self.tree = tree
        self.raw_url = url
        self.name = self.tree.tag
        self.kv = self.tree.attrib
        self._txt = None
        self._subnodes = None

    def __getitem__(self, item):  # tree[属性]
        return self.tree.attrib[item]

    def __setitem__(self, key, value):
        self.tree.attrib[key] = value

    def __repr__(self):
        txts = []
        if self.kv:
            txts.append(f'kv={self.kv}')
        if self.subnodes:
            txts.append(f'sub={len(self.subnodes)}')
        return f'{self.name}({len(self)})'

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return len(self.subnodes)

    @property
    def subnodes(self):
        if self._subnodes is None:
            self._subnodes = [Enode(html='', url=self.raw_url, tree=c) for c in self.tree.iterchildren()]
        return self._subnodes

    @property
    def txt(self):
        if self._txt is None:
            txts = []
            if self.tree.text:
                txts.append(self._strip(self.tree.text))
            if self.name == 'br':
                txts.append('\n')
            if self.subnodes:
                for sub in self.subnodes:
                    txts.append(sub.txt)
            if self.tree.tail:
                txts.append(self._strip(self.tree.tail))
            self._txt = ''.join(txts)
        return self._txt

    def _strip(self, txt):
        if txt:
            txt = txt.replace(u'\xa0', '')  # \xa0 是不间断空白符
            txt = txt.replace(u'\u3000', ' ')  # \u3000 是全角的空白符
            return txt
        else:
            return ''

    def urls(self, path):
        # path中的键名必须是小写的（不区分大小写）， 而值是区分大小写的
        ts = self.tree.xpath(path)
        out = [urljoin(self.raw_url, t) if t else '' for t in ts]
        return out

    def xpath(self, path):
        # path中的键名必须是小写的（不区分大小写）， 而值是区分大小写的
        trees = self.tree.xpath(path)
        out = [Enode(html='', url=self.raw_url, tree=tree) for tree in trees if tree is not None]
        return out

import os
import zipfile
from fish_tool.log_tool import logs
from fish_tool import sys_tool

default_compress_type = zipfile.ZIP_LZMA  # zipfile.ZIP_BZIP2   zipfile.ZIP_DEFLATED


class ZipTool:
    def __init__(self, path, mode=None, compress_type=None):
        if mode is None:
            if os.path.exists(path):
                mode = 'a'  # r只读  w创建  x独占创建  a后续添加
                logs.brief.info(f'自动指定 mode=a 文件已经存在 {path}')
            else:
                mode = 'w'
                logs.brief.info(f'自动指定 mode=w 文件不存在 {path}')
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self.compress_type = default_compress_type if compress_type is None else compress_type
        self.f = zipfile.ZipFile(path, mode, self.compress_type)

    def add(self, name, content):
        # content 可以是二进制文件 也可以是文本内容
        with sys_tool.DelayKeyboardInterrupt():
            self.f.writestr(name, data=content, compress_type=self.compress_type, compresslevel=None)

    def namelist(self):
        return self.f.namelist()

    def read(self, name):
        info = self.f.NameToInfo[name]  # 获取name对应得最新的 zipinfo（同一个name可以多次写入数据）
        return self.f.read(info)

    def open(self, name, mode="r", pwd=None, force_zip64=False):
        return self.f.open(name, mode=mode, pwd=pwd, force_zip64=force_zip64)

    def is_exist(self, name):
        return name in self.f.NameToInfo

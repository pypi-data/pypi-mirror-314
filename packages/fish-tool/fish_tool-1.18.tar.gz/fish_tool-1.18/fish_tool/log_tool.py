import inspect
from pprint import pformat
import logging.handlers
import os
from os.path import join
import tqdm

try:
    from fastapi import HTTPException
except ImportError:
    HTTPException = Exception

logging.basicConfig(level=logging.INFO, format='[%(levelname)s %(filename)s %(funcName)s:%(lineno)d] %(message)s')

long_fmt = logging.Formatter(fmt='[%(asctime)s %(levelname)s %(filename)s %(funcName)s:%(lineno)d] %(message)s', datefmt='%H:%M:%S')
long_time_fmt = logging.Formatter(fmt='[%(asctime)s %(levelname)s %(filename)s %(funcName)s:%(lineno)d] %(message)s', datefmt=None)


class InfoError(HTTPException):
    def __init__(self, detail, status_code=500):
        if HTTPException is not None:
            super().__init__(status_code=status_code, detail=detail)
        else:
            super().__init__(detail)


class TqdmLoggingHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.tqdm.write(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


# 标准输出（正常也就是打印到屏幕, 不会破坏tqdm进度条）
std_handler = TqdmLoggingHandler(logging.DEBUG)
std_handler.setFormatter(long_fmt)


def remove_handler(logger):
    for h in list(logger.handlers):
        logger.removeHandler(h)


class Logs:
    # 临时日志（只在屏幕上显示，不存储到文件）
    tmp = logging.getLogger('log_tmp')
    tmp.setLevel(logging.DEBUG)
    tmp.addHandler(std_handler)
    tmp.propagate = False

    def __init__(self, folder, level='INFO'):
        # brief 记录简要日志， 通常是统计分数等 (也会存储到all的日志文件里，时all的上下文更加完整）
        # all 记录细节日志， 全部存储到文件里，通常是训练过程中的细节，便于发现错误和debug
        # rotate 滚动细节日志， 滚动存储到文件里， 通常是部署服务后的日志，因为持续时间长，所以要滚动存储，避免占满硬盘
        self.folder = os.path.abspath(folder)
        os.makedirs(self.folder, exist_ok=True)
        self.brief = logging.getLogger('log_brief')
        self.all = logging.getLogger('log_all')
        self.rotate = logging.getLogger('log_rotate')

        self.set_logger(folder, level)

    def print(self, *args, width=200, show_path=-3):
        caller = inspect.stack()[1]
        paths = caller.filename.split('/')
        file = '/'.join(paths[show_path:])
        pre = f'[{file} {caller.function}:{caller.lineno}]'
        for arg in args:
            print(f'{pre}{pformat(arg, width=width)}')

    def reset(self, folder, level='INFO'):
        # 重置日志存储位置
        folder = os.path.abspath(folder)
        if self.folder != folder:
            self.folder = folder
            os.makedirs(folder, exist_ok=True)
            remove_handler(self.brief)
            remove_handler(self.all)
            remove_handler(self.rotate)
            self.set_logger(folder, level)

    def set_logger(self, folder, level='INFO'):
        handler_brief = logging.FileHandler(join(folder, 'log_brief.log'), mode='a', encoding='utf8', delay=True)
        handler_brief.setLevel(level)
        handler_brief.setFormatter(long_fmt)

        handler_all = logging.FileHandler(join(folder, 'log_detail_all.log'), mode='a', encoding='utf8', delay=True)
        handler_all.setLevel(level)
        handler_all.setFormatter(long_time_fmt)

        handler_rotate = logging.handlers.RotatingFileHandler(join(folder, 'log_detail_rotate.log'),
                                                              maxBytes=100000, backupCount=10, mode='a',
                                                              encoding='utf8', delay=True)
        handler_rotate.setLevel(level)
        handler_rotate.setFormatter(long_time_fmt)

        self.brief.setLevel(level)
        self.brief.addHandler(std_handler)
        self.brief.addHandler(handler_brief)
        self.brief.addHandler(handler_all)
        self.brief.propagate = False

        self.all.setLevel(level)
        self.all.addHandler(std_handler)
        self.all.addHandler(handler_all)
        self.all.propagate = False

        self.rotate.setLevel(level)
        self.rotate.addHandler(std_handler)
        self.rotate.addHandler(handler_rotate)
        self.rotate.propagate = False


tmp_folder = join(os.path.dirname(__file__), '../logs')
logs = Logs(tmp_folder)  # 初始化一个临时位置 存储日志

# 可以在其他位置使用 logs.reset(folder)  重置日志存储位置

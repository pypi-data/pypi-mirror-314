import sys
from glob import glob
import datetime
from copy import deepcopy
from types import MethodType, FunctionType
import inspect
import os
import json
import hashlib
import uuid
import base64
import pickle
import signal
import traceback
import time
import random
from fish_tool.log_tool import logs, InfoError
from fish_tool.db.sqlite_tool import SqliteTool


def _stack_to_txt(stack):
    file = os.path.basename(stack.filename) if stack.filename else '***'
    name = '' if stack.name == '<module>' else stack.name
    txt = f'{file}:{name}[{stack.lineno}]'
    return txt


def stacks_to_txt(stack_num=3, stop_index=-1):
    # 返回调用堆栈文本（stack_num是显示调用堆栈的数量   stop_index是截至堆栈的index，-1表示调用该函数的函数的index）
    assert stop_index < 0
    stacks = traceback.extract_stack()[-stack_num + stop_index:stop_index]
    txts = [_stack_to_txt(stack) for stack in stacks]
    txt = '--->'.join(txts)
    return txt


def sys_path_add(*paths, logs=None):
    d = os.path.abspath(os.path.join(*paths))
    if not os.path.isdir(d):
        d = os.path.dirname(d)
    if d not in sys.path:
        sys.path.insert(0, d)
        if logs is not None:
            logs.tmp.info(f'sys.path.insert("{d}")')


def get_cache_scroll_path(folder, name, max_num=5, add_one=True, show_log=False):
    # 获取滚动缓存文件名 如果文件数量达到max-num则自动删除最老的文件
    os.makedirs(folder, exist_ok=True)
    ptn = os.path.join(folder, f'*_{name}')
    paths = glob(ptn)
    pres = []
    for path in paths:
        pre = int(os.path.basename(path).split('_')[0])
        pres.append(pre)
    pres.sort()
    if len(pres) >= max_num:
        old_path = os.path.join(folder, f'{pres[0]}_{name}')
        os.remove(old_path)
        if show_log:
            logs.brief.info(f'delete {old_path}')
    if pres:
        pre = pres[-1]
        if add_one:
            pre += 1
    else:
        pre = 0
    path = os.path.join(folder, f'{pre}_{name}')
    return path


class DelayKeyboardInterrupt(object):
    # Ctrl+C 延迟关闭程序的上下文管理器， 例如避免写入文件时被关闭导致文件损坏
    # 使用方法 with DelayKeyboardInterrupt():
    #             save_code()
    def __enter__(self):
        self.signal_received = False
        # signal.SIGINT  键盘中断（如break键被按下）  （暂时没有支持kill 进程发送的15信号）
        self.old_handler = signal.signal(signal.SIGINT, self.handler)

    def handler(self, sig, frame):
        self.signal_received = (sig, frame)
        logs.brief.info('SIGINT received. Delaying KeyboardInterrupt.')

    def __exit__(self, type, value, traceback):
        signal.signal(signal.SIGINT, self.old_handler)
        if self.signal_received:
            self.old_handler(*self.signal_received)


def obj_to_sort_str(obj):
    # 把字典或数组都sort后再生成str （避免字典或者集合里的元素顺序不一致，导致str不一致）
    if isinstance(obj, set):
        txt = ', '.join(sorted(obj_to_sort_str(t) for t in obj))
        return '{' + txt + '}'
    elif isinstance(obj, dict):
        txt = ', '.join(f'{k}:{obj_to_sort_str(v)}' for k, v in sorted(obj.items()))
        return '{' + txt + '}'
    elif isinstance(obj, list):
        txt = ', '.join(obj_to_sort_str(t) for t in obj)
        return '[' + txt + ']'
    elif isinstance(obj, tuple):
        txt = ', '.join(obj_to_sort_str(t) for t in obj)
        return '(' + txt + ')'
    elif isinstance(obj, str):
        return f'"{obj}"'
    else:
        return str(obj)


_type__str = {  # 类型 对应的 类型描述文本
    type(1): 'int',
    type(0.1): 'float',
    type('a'): 'str',
    type(True): 'bool',
}


def diff_struct(o1, o2):
    if type(o1) != type(o2):
        return f'type 不同 {type(o1)} <> {type(o2)}'

    if isinstance(o1, dict):
        out = {}
        k1s = set(o1)
        k2s = set(o2)
        for k in k1s - k2s:
            out[k] = 'object1 多余的key'
        for k in k2s - k1s:
            out[k] = 'object2 多余的key'
        for k in k1s & k2s:
            diff = diff_struct(o1[k], o2[k])
            if diff:
                out[k] = diff
        return out
    if isinstance(o1, (list, tuple)):
        min_num = min(len(o1), len(o2))
        max_num = max(len(o1), len(o2))
        out = []
        for i in range(min_num):
            diff = diff_struct(o1[i], o2[i])
            if diff:
                out.append(diff)
        if len(o1) > len(o2):
            long = o1
            long_name = 'object1'
        else:
            long = o2
            long_name = 'object2'
        for i in range(min_num, max_num):
            out.append({f'{long_name}[{i}] {type(o1)}多余的元素': long[i]})
        return out
    if isinstance(o1, set):
        out = {}
        for item in o1 - o2:
            out.setdefault(f'object1 set()多余的元素', []).append(item)
        for item in o2 - o1:
            out.setdefault(f'object2 set()多余的元素', []).append(item)
        return out
    # if isinstance(o1, (int, float, bool, str)):  获取包括其他类型
    if o1 != o2:
        return f'value 不同 {o1} <> {o2}'


def obj_to_struct(obj, str_max_len=10, list_max_num=3, return_value=False):
    # 返回对象的结构  str_max_len是文本显示最大长度   list_max_num数组、元组、集合最多查看的数量上上限
    # return_value 为真时int、float、str、bool返回具体的值   为假时返回类型描述文本
    if isinstance(obj, dict):
        return {k: obj_to_struct(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple, set)):
        tmp = set()
        out = []
        for sub_obj in list(obj)[:list_max_num]:
            sub_struct = obj_to_struct(sub_obj)
            sub_txt = obj_to_sort_str(sub_struct)
            if sub_txt not in tmp:
                out.append(sub_struct)
                tmp.add(sub_txt)
        return type(obj)(out)
    elif obj is None:
        return None
    elif isinstance(obj, (int, float, bool)):
        if return_value:
            return obj
        else:
            return _type__str[type(obj)]
    elif isinstance(obj, str):
        if return_value:
            return obj[:str_max_len]
        else:
            return _type__str[type(obj)]
    else:
        return str(type(obj))


def lazy_property(func):
    # 给类的属性添加懒加载模式   使用方法，在类的属性方法上添加@lazy_property
    attr_name = "_lazy_" + func.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            logs.brief.info(f'计算懒加载属性 {func}')
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    return _lazy_property


def cache_hour_property(hour=1):
    ms = hour * 60 * 60 * 1000

    def decorator(func):
        # 给类的属性添加缓存模式(间隔时间＜hour时直接使用缓存数据)   使用方法，在类的属性方法上添加 @cache_hour_property(间隔小时)
        value_name = "_cache_" + func.__name__
        time_name = '_time_' + func.__name__

        @property
        def _cache_property(self):
            now = get_timestamp()
            if not hasattr(self, time_name) or (now - getattr(self, time_name)) > ms:
                logs.rotate.info(f'计算小时缓存属性 {func}')
                setattr(self, value_name, func(self))
                setattr(self, time_name, now)
            return getattr(self, value_name)

        return _cache_property

    return decorator


def singleton(cls):
    # 单例模式的类装饰器    在类的上一行加上 @singleton （不支持带初始化参数的类）
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


class ProcessMemory:
    pre_mem = 'mem_'  # 对应数据表里记录该条记录是否已经记录
    pre_result = 'res_'  # 对应数据表里记录数据结果

    def __init__(self, path):
        self.mem_path = path
        self.last_save_time = int(time.time() * 1000)
        self.mem = SqliteTool(path)
        self.fn_set = set()
        tables = self.mem.get_table_names()
        for table in tables:
            if table.startswith(self.pre_mem):
                num = self.mem.num(table)
                logs.tmp.info(f'{table} 数量={num}')
                self.fn_set.add(table[4:])

    def _info_to_key(self, info):
        if isinstance(info, (str, int)):
            return str(info)
        elif isinstance(info, dict):
            infos = [f'{k}={v}' for k, v in info.items()]
            infos.sort()
            return ','.join(infos)
        else:
            raise InfoError(f'未支持的类型 ({type(info)})info={info}')

    def init_fn(self, fn):
        if fn not in self.fn_set:
            table = f'{self.pre_mem}{fn}'
            self.mem.create_table(table, {'key': 'str', 'time': 'int'}, uni_keys=['key'], primary_keys=['key'])
            table = f'{self.pre_result}{fn}'
            self.mem.create_table(table, {'key': 'str', 'value': 'str', 'time': 'int'}, uni_keys=['key'], primary_keys=['key'])
            self.fn_set.add(fn)

    # 记录某个函数对某个数据的操作时间（秒级时间戳）
    def add_record(self, fn, info, result=None):
        # fn是函数名str         info可以是str，也可以是dict
        self.init_fn(fn)
        process_time = get_timestamp()
        key = self._info_to_key(info)
        self.mem.insert(f'{self.pre_mem}{fn}', {'key': key, 'time': process_time})
        if result is not None:
            self.mem.insert(f'{self.pre_result}{fn}', {'key': key, 'time': process_time, 'value': result})

    # 判断某个函数（在start_time以后的时间内）是否处理过某条数据
    def is_processed(self, fn, info, start_time=0):
        if fn not in self.fn_set:
            return False
        key = self._info_to_key(info)
        condition = f'key="{key}"'
        lines = self.mem.select(f'{self.pre_mem}{fn}', condition)
        if lines:
            process_time = lines[0]['time']
            return process_time > start_time
        else:
            return False

    def get_result(self, fn, info):
        key = self._info_to_key(info)
        condition = f'key="{key}"'
        lines = self.mem.select(f'{self.pre_mem}{fn}', condition)
        if lines:
            return lines[0]['value']
        else:
            return None

    # 主动触发把记忆存到pkl文件中
    def save(self):
        self.mem.commit()
        logs.brief.info(f'memory saved in {self.mem_path}')


def trans_excel(excel_path):
    # 每个表格的第一行是表头，下面都是数据， 转化成字典 {'表名': [{'键名': 值}]}
    import openpyxl
    from tqdm import tqdm
    table__lines = {}
    wb = openpyxl.load_workbook(excel_path, read_only=True, data_only=True)
    for sheet in wb:
        table = sheet.title
        data = sheet['A1': 'XXX500000']
        lines = []
        idx__field = {}
        for i, cell in enumerate(data[0]):
            field = cell.value
            if field:
                field = field.repalce(' ', '')
                if field:
                    field = field.lower()
                    idx__field[i] = field
            for line in tqdm(data[1:]):
                one = {}
                for i, field in idx__field.items():
                    v = line[i].value
                    if v:
                        one[field] = v
                if one:
                    lines.append(one)
            logs.brief.info(f'{table} 数据量={len(lines)}')
        table__lines[table] = lines
    return table__lines


def infos_find(infos, key, value):
    # infos = [{'key': value}]  在字典数组里找到kv一致的字典返回
    for i, info in enumerate(infos):
        if info.get(key) == value:
            return i, info
    return None, None


def differ_days(time_a, time_b):
    """
    计算日期相差天数  time_a/time_b 都是格式=“xxxx-xx-xx”的文本
    注意 如果time_a < time_b 则会返回负数
    """
    a = time_a.split('-')
    b = time_b.split('-')
    d1 = datetime.date(int(a[0]), int(a[1]), int(a[2]))
    d2 = datetime.date(int(b[0]), int(b[1]), int(b[2]))
    return (d1 - d2).days


def get_timestamp(txt='', fmt="%Y-%m-%dT%H:%M:%S"):
    # 返回毫秒时间戳（浮点数)   # txt = '2016-05-05 20:28:54'   T是标准日期+时间的表示格式
    if not txt:
        return int(time.time() * 1000)
    time_array = time.strptime(txt, fmt)
    return int(time.mktime(time_array) * 1000)


def get_timetxt(timestamp=None, fmt='%Y-%m-%dT%H:%M:%S', delta_day=0, delta_ms=0):
    # 返回时间文本   delta增量时间   # timestamp = 1462451334000   T是标准日期+时间的表示格式
    if timestamp is None:
        timestamp = time.time() * 1000
    timestamp += delta_day * 24 * 60 * 60 * 1000
    timestamp += delta_ms
    time_local = time.localtime(timestamp / 1000)
    return time.strftime(fmt, time_local)


def get_begin_timestamp(delta_day=0, day=''):
    # 获取某一天的0点的时间戳    delta是增量天数   如果day为空文本则获取当天 文本格式="2021-01-01"
    if not day:
        day = get_timetxt(fmt='%Y-%m-%d')
    out = get_timestamp(f'{day}T00:00:00')
    out += delta_day * 24 * 60 * 60 * 1000
    return out


def return_dict(obj, *keys):
    out = {}
    for key in keys:
        out[key] = obj.get(key)
    return out


def uid4():
    # 基于随机数，有一定的重复概率
    return str(uuid.uuid4()).replace('-', '')


def sha256(txt):
    return hashlib.sha256(txt.encode('utf8')).hexdigest()


def md5(txt):
    out = hashlib.md5(txt.encode('utf8')).hexdigest()
    return str(out)


def hash_url(url):
    # 把 文件的url转成哈希值的文件名
    tail = url.split('/')[-1]
    exts = tail.split('.')
    if len(exts) > 1:
        ext = f'.{exts[-1]}'
    else:
        ext = ''
    md5 = hashlib.md5(url.encode(encoding='UTF-8')).hexdigest()
    name = f'{md5}{ext}'
    return name


def hash_file(binfile):
    """该函数返回传入文件的SHA-1哈希值   输入文件二进制流：open(path, 'rb').read()"""
    # 创建一个哈希对象
    h = hashlib.sha1()
    h.update(binfile)
    # 返回摘要的十六进制表示
    return h.hexdigest()


def txt_to_base64(txt):
    # 编码
    encode_str = base64.encodebytes(txt.encode('utf8'))  # b'aGVsbG8gd29ybGQh\n'
    txt = encode_str.decode('utf8')
    txt = txt.strip()
    return txt


def base64_to_txt(msg):
    try:
        decode_str = base64.decodebytes(msg.encode('utf8'))  # b'hello world!'
        return decode_str.decode('utf8')
    except:
        return None


def make_token(user_id, seed, sha_len):
    user_id = str(user_id)
    sha = sha256(user_id + seed)
    user_64 = txt_to_base64(user_id)
    token = sha[:sha_len] + user_64
    return token


def check_token(token, seed, sha_len):
    # logs.tmp.info(f'check_token(token={token}, seed={seed}, sha_len={sha_len})')
    head = token[:sha_len]
    # logs.tmp.info(f'    head={head}')
    user_id = base64_to_txt(token[sha_len:])
    # logs.tmp.info(f'    user_id={user_id}')
    if user_id:
        sha = sha256(user_id + seed)
        # logs.tmp.info(f'    whole sha={sha}     pre={sha[:sha_len]}')
        if head == sha[:sha_len]:
            return {'ok': True, 'user_id': user_id}
        else:
            return {'ok': False, 'detail': '不一致', 'user_id': ''}
    else:
        return {'ok': False, 'detail': '解码失败', 'user_id': ''}


def cut_data(data, test_num=50, old_split_path=None):
    # 切分数据为训练集、验证集、测试集   （如果有老的切分信息，则使用老的验证集和测试集的_id）
    if old_split_path and os.path.isfile(old_split_path):
        split_info = json.load(open(old_split_path))
        valid_ids = set(split_info['valid'])
        test_ids = set(split_info['test'])
        for dtype in ['train', 'valid', 'test']:
            logs.brief.info(f'split_info: {dtype} data has {len(split_info[dtype])}')
        train, valid, test = [], [], []
        for doc in data:
            if doc['_id'] in valid_ids:
                valid.append(doc)
            elif doc['_id'] in test_ids:
                test.append(doc)
            else:
                train.append(doc)
    else:
        random.shuffle(data)
        logs.brief.info(f'未提供split_info')
        valid = data[:test_num]
        test = data[test_num:test_num + test_num]
        train = data[test_num + test_num:]
    out = {'train': train, 'valid': valid, 'test': test}
    split_info = {'num': {}}
    for dtype in ['train', 'valid', 'test']:
        split_info[dtype] = []
        split_info['num'][dtype] = len(out[dtype])
        logs.brief.info(f'{dtype} data has {len(out[dtype])}')
        for doc in out[dtype]:
            split_info[dtype].append(doc['_id'])
    out['split_info'] = split_info
    return out


def code_path(obj):
    try:
        filename = inspect.getfile(obj)
        line_no = inspect.getsourcelines(obj)[-1]
    except:
        return obj.__name__
    return f'File "{filename}", line {line_no} >> {obj.__name__}'


def get_safe_args(fn, raw_args):
    # 获取一个函数能够传入的参数（去掉多余的值） 避免多余的参数导致报错
    if isinstance(fn, (FunctionType, MethodType)):
        fn = fn
    else:  # 如果是类，则fn=对象的初始化函数
        fn = fn.__init__
    full_args = inspect.getfullargspec(fn)
    if full_args.varargs:
        raise ValueError(f'{fn} 不支持数组参数={full_args.varargs}')
    if full_args.varkw:  # 具有字典参数时，可以输入任意参数，所以全部返回
        return raw_args
    else:
        return {k: v for k, v in raw_args.items() if k in full_args.args}


def save_score_to_html(score, path, width='1000px', height='280px'):
    import pyecharts.globals
    from pyecharts import options as opts
    page = pyecharts.charts.Page()
    labels = list(score['best']['train'].keys())
    keys = [str(i) for i in range(len(score['history']))]
    line_opt = opts.InitOpts(theme=pyecharts.globals.ThemeType.CHALK, width=width, height=height)
    if 'loss' in score['best']:
        line = pyecharts.charts.Line(init_opts=line_opt)
        line.set_global_opts(title_opts=opts.TitleOpts(title='train-loss'), legend_opts=opts.LegendOpts())
        line.add_xaxis(keys)
        for label in labels:
            values = [round(t['loss'], 6) for t in score['history']]
            line.add_yaxis(label, values, is_symbol_show=False)
        page.add(line)

    for dtype in ['train', 'valid', 'test']:
        line = pyecharts.charts.Line(init_opts=line_opt)
        line.set_global_opts(title_opts=opts.TitleOpts(title=f'性能指标-{dtype}'), legend_opts=opts.LegendOpts())
        line.add_xaxis(keys)
        for label in labels:
            values = [round(t[dtype][label], 4) for t in score['history']]
            line.add_yaxis(label, values, is_symbol_show=True)
        page.add(line)
    page.render(path)


def sleep_waiting(total=10, desc=''):
    # 失眠等待N秒 同时打印出提示文本
    for i in range(1, total + 1):
        print(f'\rsleep_waiting: {i}/{total}  {desc}', end='')
        time.sleep(1)


def weight_choice(weights, items=None):
    # 按权重随机返回数组的一个元素  （items是数组内容， 如果不提供则返回元素的index）
    items = items or list(range(len(weights)))
    return random.choices(items, weights=weights, k=1)[0]


def weight_sample(k, weights, items=None):
    # (不重复的）按权重采样k个元素  （items是数组内容， 如果不提供则返回元素的index）
    weights = deepcopy(weights)  # deepcopy避免改变输入的参数内容
    items = deepcopy(items) or list(range(len(weights)))
    if len(items) <= k:
        return items
    out = []
    for _ in range(k):
        index = weight_choice(weights)
        out.append(items.pop(index))
        weights.pop(index)
    return out


def recursion_round_dict(data, ndigits=2):
    # 递归的把字典里的浮点数四舍五入（便于查看时候方便）
    out = {}
    for k, v in data.items():
        if isinstance(v, float):
            out[k] = round(v, ndigits)
        elif isinstance(v, dict):
            out[k] = recursion_round_dict(v, ndigits)
        else:
            out[k] = v
    return out


def cache_glob(ptn, cover=False):
    # 有一些 glob递归读取太慢了， 放在缓存里面   如果cover=True则读取新的glob结果覆盖缓存
    if os.path.exists('C:/'):
        d = 'C:/.fish_tool_cache'
    else:
        d = '~/.fish_tool_cache'
    d = os.path.abspath(d)
    os.makedirs(d, exist_ok=True)
    name = sha256(ptn) + '.pkl'
    path = os.path.join(d, name)
    if cover or not os.path.exists(path):
        logs.tmp.info(f'get new glob({ptn}) path={path}')
        out = sorted(glob(ptn))  # 排序后可以固定顺序
        with open(path, 'wb') as f:
            pickle.dump(out, f)
    else:
        logs.tmp.info(f'get cache glob({ptn}) path={path}')
        out = pickle.load(open(path, 'rb'))
    return out


def read_jsonlist(path):
    data = []
    for line in open(path, encoding='utf8').readlines():
        line = line.strip('\n').strip(' ')
        if line:
            data.append(json.loads(line))
    return data


def write_jsonlist(data, path):
    f = open(path, 'w', encoding='utf8')
    for doc in data:
        txt = json.dumps(doc, ensure_ascii=False)
        f.write(f'{txt}\n')
    f.close()

import inspect
import importlib
import pkgutil
from fish_tool.log_tool import logs, InfoError

__registry = {}

import_cache = set()


def __walk_import(package_name):
    if package_name not in import_cache:
        import_cache.add(package_name)
        module = importlib.import_module(package_name)
        path = getattr(module, '__path__', [])
        if path:
            for finder, name, is_package in pkgutil.walk_packages(path, prefix=package_name + '.'):
                __walk_import(name)


def walk_import(package_name):
    # 递归载入一个包的全部子包和子模块
    logs.tmp.info(f'walk_import {package_name}')
    __walk_import(package_name)


# def add(name):
#     # 装饰器：新增注册
#     def decorator(cls):
#         if name in __registry:
#             if cls.__module__ == '__main__' or __registry[name].__module__ == '__main__':
#                 # 在某个模块下直接执行 会重复注册, 避免第二次时报错
#                 return cls
#             if len(cls.__module__) < len(__registry[name].__module__):
#                 # 如果短的模块名字属于长的模块名字， 说明是重复的
#                 short = cls.__module__
#                 long = __registry[name].__module__
#             else:
#                 short = __registry[name].__module__
#                 long = cls.__module__
#             if short in long:
#                 return cls
#             if cls == __registry[name]:
#                 return cls
#             message = f'"{cls}"的名称"{name}"已经被"{__registry[name]}"注册'
#             raise InfoError(message)
#         else:
#             __registry[name] = cls
#         return cls
#
#     return decorator


def add(name):
    # 装饰器：新增注册
    def decorator(cls):
        if name in __registry:
            if __registry[name] == cls:
                return cls
            old = code_path(__registry[name])
            new = code_path(cls)
            message = f'名称="{name}  重复注册\n{old}\n{new}'
            raise InfoError(message)
        else:
            __registry[name] = cls
        return cls

    return decorator


def get(name: str):
    # 通过名字获取类
    if name not in __registry:
        raise InfoError(f'"{name}" 未注册')
    return __registry.get(name)


def code_path(obj):
    try:
        filename = inspect.getfile(obj)
        lineno = inspect.getsourcelines(obj)[-1]
    except:
        return obj.__name__
    return f'File "{filename}", line {lineno} >> {obj.__name__}'


def show():
    # 显示已经注册的对象
    items = [f'\t{code_path(subclass): <100} 名称: {k}' for k, subclass in __registry.items()]
    items_txt = '\n'.join(items)
    head = '=' * 43 + ' 注册的类 ' + '=' * 43
    tail = '=' * 130
    logs.tmp.info(f'{head}\n{items_txt}\n{tail}')

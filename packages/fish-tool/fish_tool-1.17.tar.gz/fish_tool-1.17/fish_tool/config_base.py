import os
from fish_tool.log_tool import logs, InfoError


class BaseConfig:

    def load(self, path: str):
        import yaml
        data = yaml.load(open(path, encoding='utf-8'), Loader=yaml.loader.Loader)
        self.__dict__.update(data)
        logs.tmp.info(f'load config: {self}  path={path}')
        return self

    def __getattr__(self, item):  # 未定义的属性返回None 避免引起异常
        return None

    def all_kv(self):
        kv = {k: v for k, v in self.__class__.__dict__.items() if not k.startswith('_')}  # 不保存以下划线开头的变量名
        kv.update(self.__dict__)
        return kv

    def save(self, path):
        import yaml
        path_dir = os.path.dirname(path)
        os.makedirs(path_dir, exist_ok=True)
        logs.tmp.info(f'save config: {path}')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(yaml.dump(self.all_kv(), allow_unicode=True))
        return self

    def __str__(self):
        return f'{self.__class__.__name__}({self.all_kv()})'

    def check(self, *keys):
        # 检查config是否包含 这些字段
        kv = self.all_kv()
        error_keys = [k for k in keys if k not in kv]
        if error_keys:
            raise InfoError(f'config 缺少字段 {error_keys}')

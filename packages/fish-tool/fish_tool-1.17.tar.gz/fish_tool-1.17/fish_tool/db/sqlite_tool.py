import json
import sqlite3
from fish_tool.log_tool import logs, InfoError


class ScrollIter:
    # 包装一个迭代器， 使其增加长度属性， 便于tqdm等显示进度条
    def __init__(self, db, table, condition=None, num=100):
        self.return_num = 0
        self.db = db
        self.table = table
        self.condition = condition
        self.num = num
        self.total = db.num(table, condition=condition)
        self.data = []

    def __len__(self):
        return self.total

    def __iter__(self):
        while self.return_num < self.total:
            if self.data:
                for one in self.data:
                    self.return_num += 1
                    yield one
            self.data = self.db.select(self.table, condition=self.condition, num=self.num, start=self.return_num)


class SqliteTool:
    def __init__(self, path):
        self.db = sqlite3.connect(path)

    def get_table_names(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        cur = self.db.cursor()
        cur.execute(sql)
        lines = cur.fetchall()
        out = [t[0] for t in lines]
        return out

    def add_field(self, table, field, ftype, default):
        if ftype == 'int':
            ftype = 'integer'
        elif ftype == 'float':
            ftype = 'real'
        elif ftype == 'str':
            ftype = 'text'
        sql = f"alter table {table} add column '{field}' {ftype} default '{default}'"
        cur = self.db.cursor()
        out = cur.execute(sql)
        return out

    def create_table(self, table, field__type, uni_keys=None, primary_keys=None, auto_key=None):
        # uni_key 值必须唯一      primary_key 主键（便于搜索）   auto_key 自增key
        # field__type.type in ['str', 'int', 'float', 'blob']
        uni_keys = uni_keys or []
        primary_keys = primary_keys or []
        primary_keys = [t for t in primary_keys if t != auto_key]
        if primary_keys and auto_key:
            raise ValueError(f'如果有自增主键 则不能有其他主键 primary={primary_keys} auto={auto_key}')

        cur = self.db.cursor()
        field__type_txt = ''
        for k, v in field__type.items():
            if field__type_txt:
                field__type_txt += ', '
            if v == 'int':
                v = 'integer'
            elif v == 'float':
                v = 'real'
            elif v == 'str':
                v = 'text'
            if k in uni_keys:
                v = f'{v} UNIQUE'
            field__type_txt += f'"{k}" {v}'
        if primary_keys:
            keys = ', '.join(f'"{t}"' for t in primary_keys)
            field__type_txt += f', PRIMARY KEY({keys})'
        elif auto_key:
            field__type_txt += f', PRIMARY KEY("{auto_key}" AUTOINCREMENT)'

        sql = f'CREATE TABLE "{table}" ({field__type_txt});'
        cur.execute(sql)

    def num(self, table, k=None, v=None, condition=''):
        cur = self.db.cursor()
        sql = f'select count(*) from {table}'
        if condition:
            sql += f' where {condition}'
        elif k and v:
            if isinstance(v, str):
                v = f'"{v}"'
            condition = f'{k}={v}'
            sql += f' where {condition}'

        cur.execute(sql)
        lines = cur.fetchall()
        line = lines[0]
        out = line[0]
        return out

    def select(self, table, condition=None, num=None, start=None):
        cur = self.db.cursor()
        sql = f'select * from {table}'
        if condition:
            sql += f' where {condition}'
        if num is not None:
            sql += f' limit {num}'
        if start is not None:
            sql += f' OFFSET {start}'
        cur.execute(sql)
        fields = [t[0] for t in cur.description]
        out = []
        for row in cur.fetchall():
            obj = {}
            for k, v in zip(fields, row):
                if isinstance(v, bytes):
                    v = json.loads(v.decode())
                obj[k] = v
            out.append(obj)
        return out

    def scroll(self, table, condition=None, num=1000):
        return ScrollIter(self, table, condition=condition, num=num)

    def commit(self):
        self.db.commit()

    def insert(self, table, field__value, commit=True):
        cur = self.db.cursor()
        fields = list(field__value)
        field_txt = ','.join(fields)
        ask_txt = ','.join('?' for _ in fields)
        values = []
        for k in fields:
            v = field__value[k]
            if not isinstance(v, (int, float, str)):
                v = json.dumps(v).encode()
            values.append(v)
        sql = f'insert into {table} ({field_txt}) values ({ask_txt})'
        cur.execute(sql, values)
        if commit:
            self.db.commit()

    def update(self, table, condition, field__value, commit=True):
        cur = self.db.cursor()
        fields = list(field__value)
        field_txt = ','.join(f'{t}=?' for t in fields)
        values = []
        for k in fields:
            v = field__value[k]
            if not isinstance(v, (int, float, str)):
                v = json.dumps(v).encode()
            values.append(v)
        sql = f'update  {table} set {field_txt} where {condition}'
        cur.execute(sql, values)
        if commit:
            self.db.commit()

    def delete(self, table, condition, commit=True):
        cur = self.db.cursor()
        sql = f'delete from {table} where {condition}'
        cur.execute(sql)
        if commit:
            self.db.commit()

    def exist(self, table, k, v):
        cur = self.db.cursor()
        sql = f"select exists(select 1 from {table} where {k}='{v}')"
        # log.info(f'sql={sql}')
        cur.execute(sql)
        resp = cur.fetchone()
        return resp[0]
        # if cur.fetchone():
        #     return True
        # else:
        #     return False


if __name__ == '__main__':
    db = SqliteTool('test.sqlite')

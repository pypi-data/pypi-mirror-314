import pymysql
from fish_tool.log_tool import logs


class MysqlTool:
    def __init__(self, user, password, database, host='127.0.0.1', port=3306, charset='utf8'):
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)

    def exec(self, sql, cursor=None):
        if not sql.endswith(';'):
            sql += ';'

        close = cursor is None
        cursor = cursor or self.conn.cursor()
        cursor.execute(sql)
        out = cursor.fetchall()
        if close:
            cursor.close()
        return out

    def count(self, table):
        sql = f'select count(*) from {table} limit 1;'
        resp = self.exec(sql)
        return resp[0][0]

    def keys(self, table):
        sql = f'show columns from {table};'
        resp = self.exec(sql)
        out = []
        for line in resp:
            one = {k: v for k, v in zip(['field', 'type', 'null', 'key', 'default', 'extra'], line)}
            # key: PRI-主键的组成部分    空-可以重复，没有索引     UNI-唯一值，不能为空    MUL-可以重复
            logs.rotate.info(one)
            out.append(one['field'])
        return out

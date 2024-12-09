import inspect
from pprint import pprint, pformat
from copy import deepcopy
import math
import time
import sys
import traceback
import os
import json
import pickle
import requests
from fish_tool.db.zip_tool import ZipTool
from tqdm import tqdm
import httpx
from fish_tool.log_tool import logs, InfoError


class ScrollIter:
    # 包装一个迭代器， 使其增加长度属性， 便于tqdm等显示进度条
    def __init__(self, host, index, query, wait='3m', timeout=20000):
        self.return_num = 0
        self.wait = wait
        url = f'{host}/{index}/_doc/_search?scroll={wait}'
        resp = requests.post(url, json=query, timeout=timeout).json()

        self.url_scroll = f'{host}/_search/scroll'
        try:
            self.total = resp['hits']['total']['value']
            self._scroll_id = resp['_scroll_id']
            self.hits = resp['hits']['hits']
        except:
            logs.rotate.error(f'url={url}')
            logs.rotate.error(f'query={query}')
            logs.rotate.error(f'resp={resp}')
            raise

    def __len__(self):
        return self.total

    def __iter__(self):
        while self.return_num < self.total:
            if self.hits:
                for one in self.hits:
                    self.return_num += 1
                    yield one
            body_scroll = {'scroll': self.wait, 'scroll_id': self._scroll_id}
            resp = requests.post(self.url_scroll, json=body_scroll).json()
            self._scroll_id = resp['_scroll_id']
            self.hits = resp['hits']['hits']


class ScrollBatch:
    def __init__(self, es, index, query, wait='3m', timeout=20000):
        self.es = es
        self.wait = wait
        url = f'{self.es.host}/{index}/_doc/_search?scroll={wait}'
        self.url_scroll = '{}/_search/scroll'.format(self.es.host)
        resp = requests.post(url, json=query, timeout=timeout).json()
        try:
            self.total = math.ceil(resp['hits']['total']['value'] / query.get('size', 10))
            self._scroll_id = resp['_scroll_id']
            self.hits = resp['hits']['hits']
        except:
            logs.rotate.error(f'url={url}')
            logs.rotate.error(f'query={query}')
            logs.rotate.error(f'resp={resp}')
            raise

    def __len__(self):
        return self.total

    def __iter__(self):
        while self.hits:
            yield self.hits
            body_scroll = {'scroll': self.wait, 'scroll_id': self._scroll_id}
            resp = requests.post(self.url_scroll, json=body_scroll).json()
            self._scroll_id = resp['_scroll_id']
            self.hits = resp['hits']['hits']


class Query:
    def __init__(self, _query):
        self._query = self.extract_query(_query)
        self.functions = []

    def __call__(self, size=20, start=0, sort='', desc=True, _source=None, excludes=None, fn_boost_mode='multiply', fn_boost=None, fn_min_score=None):
        # desc是降序排序（sort有参数时才有用）
        # _source 返回数据的字段数组
        # fn_boost 函数分数的boost   fn_boost_mode 函数和query的分数结合模式   fn_min_score最小值（会筛选掉不符合的doc）
        if self.functions:
            assert fn_boost_mode in ['multiply', 'replace', 'sum', 'avg', 'max', 'min']
            if len(self.functions) == 1:
                fn = deepcopy(self.functions)[0]
                fn['boost'] = fn.pop('weight', 1)  # 一个函数则字段是boost  多个函数则字段是weight
                fn['query'] = self._query
                fn['boost_mode'] = fn_boost_mode
                _query = {'function_score': fn}
            else:
                _query = {
                    'function_score': {
                        'query': self._query,
                        'functions': self.functions,
                        'boost_mode': fn_boost_mode,
                    }
                }
            if fn_boost is not None:
                _query['function_score']['boost'] = fn_boost
            if fn_min_score is not None:
                _query['function_score']['min_score'] = fn_min_score
            out = {'query': _query}
        else:
            out = {'query': self._query}
        out['size'] = size
        out['from'] = start
        if sort:
            order = {'order': 'desc' if desc else 'asc'}
            out['sort'] = [{sort: order}]
        body_source = {}
        if _source:
            if isinstance(_source, str):
                body_source["includes"] = [_source]
            elif isinstance(_source, list):
                body_source["includes"] = _source
            if isinstance(excludes, str):
                body_source["excludes"] = [excludes]
            elif isinstance(excludes, list):
                body_source["excludes"] = excludes
        if body_source:
            out['_source'] = body_source
        return out

    @classmethod
    def _recurrence_json_to_query(cls, kv):
        if isinstance(kv, dict):
            if '_fn' in kv:
                fn = getattr(Query, kv['_fn'])
                param = Query._recurrence_json_to_query(kv.get('_param', {}))
                query = fn(**param)
                if '_call' in kv:
                    query = query(**kv['_call'])
                return query
            else:
                return {k: Query._recurrence_json_to_query(v) for k, v in kv.items()}
        if isinstance(kv, (list, tuple, set)):
            return [Query._recurrence_json_to_query(t) for t in kv]
        else:
            return kv

    @classmethod
    def json_to_query(cls, kv):
        # 通过json字典转换成query（便于不能直接写代码的环境使用， 例如客户端调用）
        # {‘_fn’: 'query函数名', '_call': {query(参数字典)}， ‘_param’： {_fn（参数字典）}}
        kv = deepcopy(kv)
        query = cls._recurrence_json_to_query(kv)
        if isinstance(query, Query):
            query = query()
        return query

    @classmethod
    def all(cls, size=20, start=0, sort='', desc=True, _source=None, _name='', excludes=None):
        # 直接返回的是query的字典
        q = {"match_all": {}}
        if _name:
            q['match_all']['_name'] = _name
        query = cls(q)
        return query(size=size, start=start, sort=sort, desc=desc, _source=_source, excludes=excludes)

    @staticmethod
    def extract_query(query):
        # 提取内部的query字典
        if isinstance(query, Query):
            query = query._query
        if 'query' in query:
            query = query['query']
        return query

    @classmethod
    def analyze(cls):
        url = 'http://{host}:{port}/{index}/_analyze'.format(host='', port='', index='')
        return url

    def fn_decay(self, fn, key, weight=1, origin=None, offset=None, scale=None, decay=0.5):
        # fn=空文本则函数的固定分数=boost
        assert fn in ['gauss', 'exp', 'linear']
        one = {'weight': weight}
        if fn:
            one[fn] = {
                key: {
                    "origin": origin,
                    "scale": scale,
                    "offset": offset,
                    "decay": decay
                }
            }
        self.functions.append(one)

    @classmethod
    def aggs(cls, name__field, query=None, size=100):
        # field文本的末尾记得添加 .keyword
        # 直接返回query数据 而不是Query对象
        # name__field = {name: field_str}                       (类型默认是terms)
        # name__field = {name: {field: field_str, size: int}}   (类型默认是terms)
        # name__field = {name: {field: field_str, size: int, type: 'terms'}}
        # name__field = {name: {'type': 'histogram', 'field': '字段', 'interval': 1}}  数值按照间隔=1进行统计
        # name__field = {name: {'type': 'cardinality', 'field': '字段'}}  统计 桶的数量
        q = {
            'size': 0,
            'aggs': {
                # name: {
                #     'terms': {
                #         'field': field,
                #         'size': 20,
                #     },
                # 'aggs': 子聚合
                # },
            }
        }
        if query:
            if isinstance(query, Query):
                query = query._query
            if isinstance(query, dict):
                if 'query' in query:
                    query = query['query']
            q['query'] = query
        for name, field in name__field.items():
            if isinstance(field, str):
                wrap = {'terms': {'field': field, 'size': size}}
            else:
                agg_type = field.pop('type', 'terms')
                wrap = {agg_type: field}

                if 'aggs' in field:
                    wrap['aggs'] = field.pop('aggs')
                    wrap['size'] = size
            q['aggs'][name] = wrap
        return q

    @classmethod
    def term(cls, key, values, boost=None, boost_change=True, _name=''):
        if isinstance(values, (int, float)):
            q = {"term": {
                key: {
                    "value": values,
                }}}

            if boost is not None or boost_change:
                if boost is None:
                    boost = 1.0
                q['term'][key]['boost'] = boost
        elif isinstance(values, str):
            q = {"term": {
                key: {
                    "value": values,
                }}}
            if boost is not None or boost_change:
                if boost is None:
                    boost = 1.0
                if boost_change:
                    total = len(values)
                    if total:
                        boost /= len(values)  # 根据搜索文本长度归一化
                q['term'][key]['boost'] = boost
        elif len(values) == 1:
            q = {"term": {
                key: {
                    "value": values[0],
                    "boost": boost
                }}}
            if boost is not None or boost_change:
                if boost is None:
                    boost = 1.0
                if boost_change:
                    total = len(values[0])
                    if total:
                        boost /= len(values[0])  # 根据搜索文本长度归一化
                q['term'][key]['boost'] = boost
        else:
            should = [cls.term(key, v, boost_change=boost_change) for v in values]
            if boost is not None or boost_change:
                if boost is None:
                    boost = 1.0
                if boost_change:
                    total = len(values)
                    if total:
                        boost /= len(values)  # 根据搜索文本数量归一化
            q = cls.bool(should=should, boost=boost)
        if _name:
            q['term'][key]['_name'] = _name
        query = Query(q)
        return query

    @classmethod
    def term_filter(cls, key, values, required_matches=None, _name=''):
        # 问题： terms是筛选方法，所有分数都等于1   匹配的项数没有区别
        if isinstance(values, list):
            if len(values) == 1:
                q = {"term": {key: values[0]}}
            else:
                q = {"terms": {key: list(values)}}
        else:
            q = {"term": {key: values}}
        if required_matches is not None:
            q['required_matches'] = required_matches
        if _name:
            if 'term' in q:
                q['term'][key]['_name'] = _name
            else:
                q['terms'][key]['_name'] = _name
        query = Query(q)
        return query

    @classmethod
    def match(cls, key, value, boost=None, boost_change=True, analyzer=None, _name=''):
        q = {"match": {key: {"query": value}}}
        if _name:
            q['match'][key]['_name'] = _name
        if analyzer:
            q['match'][key]['analyzer'] = analyzer
        if boost is not None or boost_change:
            if boost is None:
                boost = 1.0
            if boost_change:
                total = len(value)
                if total:
                    boost /= len(value)  # 根据搜索文本长度归一化
            q['match'][key]['boost'] = boost
        query = Query(q)
        return query

    @classmethod
    def match_phrase(cls, key, value, boost=None, _name=''):
        q = {"match_phrase": {key: {"query": value}}}
        if _name:
            q['match_phrase'][key]['_name'] = _name
        if boost is not None:
            q['match_phrase'][key]['boost'] = boost
        return Query(q)

    @classmethod
    def range(cls, key, start=None, end=None, boost=1.0, _name=''):
        # 示范： cls.range('a', '>3', '<=10')
        q = {
            "range": {
                key: {
                    "boost": boost
                }
            }
        }
        if _name:
            q['range'][key]['_name'] = _name
        if start is not None:
            q['range'][key]['gte'] = start
        if end is not None:
            q['range'][key]['lte'] = end
        query = Query(q)
        return query

    @classmethod
    def nest(cls, path, query):
        q = {
            "nested": {
                "path": path,
                "query": Query.extract_query(query)
            }
        }
        query = Query(q)
        return query

    @classmethod
    def exist(cls, key, _name=''):
        q = {
            "exists": {
                "field": key
            }
        }
        if _name:
            q['exists']['_name'] = _name
        query = Query(q)
        return query

    @classmethod
    def geo_filter(cls, key, location, distance, boost=None):
        # 按地理距离筛选, 符合的分数=1 否则分数=0
        q = {
            "geo_distance": {
                "distance": distance,  # 10000m   = 10000米
                key: location,  # {"lat": 39.504901,"lon": 118.966,},
            }
        }
        if boost:
            q['geo_distance']['boost'] = boost
        query = Query(q)
        return query

    @classmethod
    def bool(cls,
             must: list = None,
             should: list = None,
             must_not: list = None,
             filter: list = None,
             boost: float = None,
             boost_change: bool = True,
             minimum_should_match: int = 0,
             _name: str = '',
             ):
        q = {"bool": {}}
        lengths = []
        if must:
            lengths.append(len(must))
            q['bool']['must'] = [Query.extract_query(t) for t in must]
        if should:
            lengths.append(len(should))
            q['bool']['should'] = [Query.extract_query(t) for t in should]
        if must_not:
            q['bool']['must_not'] = [Query.extract_query(t) for t in must_not]
        if filter:
            q['bool']['filter'] = [Query.extract_query(t) for t in filter]
        if boost is not None or boost_change:
            if boost is None:
                boost = 1.0
            if boost_change:
                total = sum(lengths)
                if total:
                    boost /= total  # 根据查询子句的总数量归一化
            q['bool']['boost'] = boost
        if minimum_should_match:
            q['bool']['minimum_should_match'] = minimum_should_match
        if _name:
            q['bool']['_name'] = _name
        query = BoolQuery(q)
        return query

    @classmethod
    def boost(cls, positive: dict, negative: dict, negative_boost: float = 0.2):
        q = {
            "boosting": {
                "positive": positive,
                "0": negative,
                "negative_boost": negative_boost
            }
        }
        query = Query(q)
        return query


class BoolQuery(Query):
    def __init__(self, _query):
        super().__init__(_query)

    def __call__(self, *args, **kv):
        if any(self._query['bool'].values()):
            fn = super().__call__
        else:
            fn = Query.all.__call__
            # 没有任何条件 则query相当于 all
        return fn(*args, **kv)

    def must(self, query):
        self._query['bool'].setdefault('must', []).append(Query.extract_query(query))

    def should(self, query):
        self._query['bool'].setdefault('should', []).append(Query.extract_query(query))

    def no(self, query):
        self._query['bool'].setdefault('must_not', []).append(Query.extract_query(query))

    def filter(self, query):
        self._query['bool'].setdefault('filter', []).append(Query.extract_query(query))


class EsTool:
    def __init__(self, host):
        self.host = host
        self.headers = {'Content-Type': 'application/json'}

    def all_index(self):
        url = f'{self.host}/_cat/indices?format=json'
        resp = requests.get(url, timeout=12)
        out = resp.json()
        return out

    def explain(self, index, query, doc_id=None):
        if doc_id:
            url = f'{self.host}/{index}/_explain/{doc_id}'
            query = {k: v for k, v in query.items() if k in ['query']}  # 去除 size 等无用的参数
        else:
            url = f'{self.host}/{index}/_doc/_search'
            query = deepcopy(query)
            query['explain'] = True
        resp = requests.post(url, json=query, headers=self.headers, timeout=3)
        resp_obj = resp.json()
        out = resp_obj
        return out

    def waiting_es_is_ok(self, minute=10):
        for i in range(int(minute * 60)):
            try:
                resp = requests.get(self.host, timeout=1)
                txt = resp.text
            except:
                txt = '404'
            if 'You Know, for Search' in txt:
                logs.rotate.warning(f'ES is OK!')
                return
            else:
                logs.rotate.warning(f'ES is not OK. It is Waiting!')
                time.sleep(1)
        raise ValueError(f'{self.host} 无法连结到ES')

    async def async_count(self, index, query=None):
        url = f'{self.host}/{index}/_doc/_count'
        if query is None:
            query = Query.all()
        elif isinstance(query, Query):
            query = query()
        query = {k: v for k, v in query.items() if k in ['query']}
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=query, headers=self.headers, timeout=3)
            resp = resp.json()
            if 'error' in resp:
                logs.rotate.error(f'error={resp}')
            out = resp.get('count', 0)
            return out
        except Exception:
            raise

    def count(self, index, query=None):
        url = f'{self.host}/{index}/_doc/_count'
        if query is None:
            query = Query.all()
        elif isinstance(query, Query):
            query = query()
        query = {k: v for k, v in query.items() if k in ['query']}
        try:
            resp = requests.post(url, json=query, headers=self.headers, timeout=3)
            resp = resp.json()
            if 'error' in resp:
                logs.rotate.error(f'error={resp}')
            out = resp.get('count', 0)
            return out
        except Exception:
            raise

    async def async_save(self, doc, index, doc_id=''):
        # 增 （如果id已存在则替换内容） 如果id和doc都存在则update
        if doc_id:
            url = f'{self.host}/{index}/_doc/{doc_id}/_update'
        else:
            url = f'{self.host}/{index}/_doc/'
        try:
            async with httpx.AsyncClient() as client:
                if doc_id:
                    body = {'doc': doc, 'doc_as_upsert': True}
                    resp = await client.post(url, json=body, headers=self.headers, timeout=3)
                else:
                    resp = await client.post(url, json=doc, headers=self.headers, timeout=3)
            resp_obj = resp.json()
            # 'result': 'created'  创建成功   updated更新成功
            # 'status': 409        已存在了，冲突，创建失败
            logs.rotate.info(f'save_resp={resp_obj}')
            out = resp_obj
        except requests.exceptions.ReadTimeout:
            logs.rotate.error(f'url={url}  body={doc}  超时错误')
            out = {}
        except Exception:
            error = '\n'.join(traceback.format_exception(*sys.exc_info()))
            logs.rotate.error(f'url={url}  body={doc}  {error}')
            out = {}
        return out

    def save(self, doc, index, doc_id=''):
        # 警告： 会全文替换， 缺少的字段会被删除
        # 增 （如果id已存在则替换内容）
        if doc_id:
            url = f'{self.host}/{index}/_doc/{doc_id}'
        else:
            url = f'{self.host}/{index}/_doc/'
        try:
            if doc_id:
                resp = requests.put(url, json=doc, headers=self.headers, timeout=3)
            else:
                resp = requests.post(url, json=doc, headers=self.headers, timeout=3)
            resp_obj = resp.json()
            out = resp_obj
            # id重复错误
            # {'error': {'root_cause': [{'type': 'version_conflict_engine_exception', 'reason': '[a001]: version
            # conflict, document already exists (current version [1])', 'index_uuid': 'BL8rKRXgRkKX3LgKb7MPEg',
            # 'shard': '0', 'index': 'test'}], 'type': 'version_conflict_engine_exception', 'reason': '[a001]: version conflict,
            # document already exists (current version [1])', 'index_uuid': 'BL8rKRXgRkKX3LgKb7MPEg', 'shard': '0', 'index': 'test'}, 'status': 409}
            # 创建成功
            # {'_index': 'test', '_type': '_doc', '_id': 'a002', '_version': 1, 'result': 'created', '_shards': {'total': 2,
            # 'successful': 1, 'failed': 0}, '_seq_no': 1, '_primary_term': 1}

            # {'_index': 'test', '_type': '_doc', '_id': 'nJs2znMBLUO2t0Glmcsb', '_version': 1, 'result': 'created',
            # '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 2, '_primary_term': 1}
        except requests.exceptions.ReadTimeout:
            logs.rotate.error(f'url={url}  body={doc}  超时错误')
            out = {}
        except Exception:
            error = '\n'.join(traceback.format_exception(*sys.exc_info()))
            logs.rotate.error(f'url={url}  body={doc}  {error}')
            out = {}
        return out

    async def async_update_doc(self, doc, index, doc_id, action='update', show_log=True, wait=False, timeout=10):
        # 更新成功返回 True 否则返回False
        assert action in ['update', 'index']
        # logs.rotate.info(f'update_doc={doc}')
        if action == 'update':
            url = f'{self.host}/{index}/_doc/{doc_id}/_{action}'
            body = {'doc': doc}
        else:
            url = f'{self.host}/{index}/_doc/{doc_id}'
            body = doc
        if wait:
            url += '?refresh=wait_for'  # 等待ES存储成功
        try:
            if action == 'update':
                async with httpx.AsyncClient() as client:
                    resp = await client.post(url, json=body, headers=self.headers, timeout=timeout)
            else:
                async with httpx.AsyncClient() as client:
                    resp = await client.put(url, json=body, headers=self.headers, timeout=timeout)
            resp_obj = resp.json()
            if show_log:
                code_caller = inspect.stack()[1]
                code_file = '/'.join(code_caller.filename.split('/')[-3:])
                pre = f'[{code_file} {code_caller.function}:{code_caller.lineno}]'
                logs.rotate.info(f'{pre} update_doc resp_obj={resp_obj}')
            out = resp_obj.get('result') in ['updated', 'noop', 'created']  # noop=更新后未变化，所以没有操作
            # resp原始值
            # 更新成功
            # {'_index': 'test', '_type': '_doc', '_id': 'nJs2znMBLUO2t0Glmcsb', '_version': 2, 'result': 'updated',
            # '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 3, '_primary_term': 1}
            # 不存在
            # {'error': {'root_cause': [{'type': 'document_missing_exception', 'reason': '[_doc][nJs2znMBLUO2t0Glmcsb--]:
            # document missing', 'index_uuid': 'BL8rKRXgRkKX3LgKb7MPEg', 'shard': '0', 'index': 'test'}], 'type': 'document_missing_exception',
            # 'reason': '[_doc][nJs2znMBLUO2t0Glmcsb--]: document missing', 'index_uuid': 'BL8rKRXgRkKX3LgKb7MPEg', 'shard': '0', 'index': 'test'},
            # 'status': 404}
        except requests.exceptions.ReadTimeout:
            logs.rotate.error(f'url={url}  body={body}  超时错误')
            out = None
        except Exception:
            error = '\n'.join(traceback.format_exception(*sys.exc_info()))
            logs.rotate.error(f'url={url}  body={body}  {error}')
            out = None
        return out

    def update_doc(self, doc, index, doc_id, action='update', show_log=True, wait=False, timeout=10):
        # 更新成功返回 True 否则返回False
        assert action in ['update', 'index']
        # logs.rotate.info(f'update_doc={doc}')
        if action == 'update':
            url = f'{self.host}/{index}/_doc/{doc_id}/_{action}'
            body = {'doc': doc}
        else:
            url = f'{self.host}/{index}/_doc/{doc_id}'
            body = doc
        if wait:
            url += '?refresh=wait_for'  # 等待ES存储成功
        try:
            if action == 'update':
                resp = requests.post(url, json=body, headers=self.headers, timeout=timeout)
            else:
                resp = requests.put(url, json=body, headers=self.headers, timeout=timeout)
            resp_obj = resp.json()
            if show_log:
                code_caller = inspect.stack()[1]
                code_file = '/'.join(code_caller.filename.split('/')[-3:])
                pre = f'[{code_file} {code_caller.function}:{code_caller.lineno}]'
                logs.rotate.info(f'{pre} update_doc resp_obj={resp_obj}')
            out = resp_obj.get('result') in ['updated', 'noop', 'created']  # noop=更新后未变化，所以没有操作
            # resp原始值
            # 更新成功
            # {'_index': 'test', '_type': '_doc', '_id': 'nJs2znMBLUO2t0Glmcsb', '_version': 2, 'result': 'updated',
            # '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 3, '_primary_term': 1}
            # 不存在
            # {'error': {'root_cause': [{'type': 'document_missing_exception', 'reason': '[_doc][nJs2znMBLUO2t0Glmcsb--]:
            # document missing', 'index_uuid': 'BL8rKRXgRkKX3LgKb7MPEg', 'shard': '0', 'index': 'test'}], 'type': 'document_missing_exception',
            # 'reason': '[_doc][nJs2znMBLUO2t0Glmcsb--]: document missing', 'index_uuid': 'BL8rKRXgRkKX3LgKb7MPEg', 'shard': '0', 'index': 'test'},
            # 'status': 404}
        except requests.exceptions.ReadTimeout:
            logs.rotate.error(f'url={url}  body={body}  超时错误')
            out = None
        except Exception:
            error = '\n'.join(traceback.format_exception(*sys.exc_info()))
            logs.rotate.error(f'url={url}  body={body}  {error}')
            out = None
        return out

    async def async_read(self, index, doc_id, _source=None):
        """
        读取文件内容返回， 如果不存在则返回值=default
        :param index:
        :param doc_id:
        :param _source:
        :return:
            {'_index': '', '_type': '_doc', '_id': '', '_primary_term': 3, 'found': True, '_source': {}}
            {'_index': '', '_type': '_doc', '_id': '', 'found': False}
        """
        url = f'{self.host}/{index}/_doc/{doc_id}'
        if _source:
            if isinstance(_source, list):
                _source = ','.join(_source)
            url += f'?_source={_source}'
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, headers=self.headers, timeout=3)
            out = resp.json()
            if not out.get('found'):
                logs.rotate.error(f'url={url}  {out}')
                out = {'found': False, 'error': f'not found'}
        except requests.exceptions.ReadTimeout:
            error = f'url={url}  超时错误'
            logs.rotate.error(error)
            out = {'found': False, 'error': error}
        except Exception:
            error = '\n'.join(traceback.format_exception(*sys.exc_info()))
            logs.rotate.error(f'url={url}  {error}')
            out = {'found': False, 'error': error}
        return out

    def read(self, index, doc_id, _source=None):
        """
        读取文件内容返回， 如果不存在则返回值=default
        :param index:
        :param doc_id:
        :param _source:
        :return:
            {'_index': '', '_type': '_doc', '_id': '', '_primary_term': 3, 'found': True, '_source': {}}
            {'_index': '', '_type': '_doc', '_id': '', 'found': False}
        """
        url = f'{self.host}/{index}/_doc/{doc_id}'
        if _source:
            if isinstance(_source, list):
                _source = ','.join(_source)
            url += f'?_source={_source}'
        try:
            resp = requests.get(url, headers=self.headers, timeout=3)
            out = resp.json()
        except requests.exceptions.ReadTimeout:
            error = f'url={url}  超时错误'
            logs.rotate.error(error)
            out = {'found': False, 'error': error}
        except Exception:
            error = '\n'.join(traceback.format_exception(*sys.exc_info()))
            logs.rotate.error(f'url={url}  {error}')
            out = {'found': False, 'error': error}
        return out

    async def async_exist(self, index, doc_id):
        url = f'{self.host}/{index}/_doc/{doc_id}'
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.head(url, headers=self.headers, timeout=3)
            out = resp.status_code == 200
        except requests.exceptions.ReadTimeout:
            logs.rotate.error(f'url={url}  超时错误')
            out = None
        except Exception:
            error = '\n'.join(traceback.format_exception(*sys.exc_info()))
            logs.rotate.error(f'url={url}  {error}')
            out = None
        return out

    def exist(self, index, doc_id):
        url = f'{self.host}/{index}/_doc/{doc_id}'
        try:
            resp = requests.head(url, headers=self.headers, timeout=3)
            out = resp.status_code == 200
        except requests.exceptions.ReadTimeout:
            logs.rotate.error(f'url={url}  超时错误')
            out = None
        except Exception:
            error = '\n'.join(traceback.format_exception(*sys.exc_info()))
            logs.rotate.error(f'url={url}  {error}')
            out = None
        return out

    def index_exist(self, index):
        url = f'{self.host}/{index}'
        try:
            resp = requests.get(url, headers=self.headers, timeout=3)
            out = 'error' not in resp.json()
        except requests.exceptions.ReadTimeout:
            logs.rotate.error(f'url={url}   超时错误')
            out = None
        except Exception:
            error = '\n'.join(traceback.format_exception(*sys.exc_info()))
            logs.rotate.error(f'url={url}  {error}')
            out = None
        return out

    def create_index(self, index):
        if self.index_exist(index):
            return True
        else:
            url = f'{self.host}/{index}'
            resp = requests.put(url)
            out = resp.json()
            return out

    def set_disk(self, low=0.999998, high=0.999999, flood_stage=0.999999):
        # 避免硬盘使用率超过95%时自动进入只读模式
        assert flood_stage >= high
        body = {
            "persistent": {  # persistent表示为永久修改，重启以后也会保存设置   transient表示临时修改，重启以后不会保存设置
                # 这两个是磁盘使用率限制，当磁盘使用率大于低的限制时，如果没有别的node可以存储数据，状态就会变为red
                "cluster.routing.allocation.disk.watermark.low": f"{(low * 100):0.6f}%",  # 默认值 90%
                "cluster.routing.allocation.disk.watermark.high": f"{(high * 100):0.6f}%",  # 默认值 95%

                # 硬盘使用率大于该值， ES会进入只读模式
                "cluster.routing.allocation.disk.watermark.flood_stage": f"{(flood_stage * 100):0.6f}%",  # 默认值95%
                # 这个值要大于等于cluster.routing.allocation.disk.watermark.high，否则设置不成功，这时候只能搜索，不能加了
            }
        }
        print(body)
        url = f'{self.host}/_cluster/settings'
        resp = requests.put(url, json=body, timeout=5)
        out = resp.json()
        return out

    def set_not_read_only(self):
        body = {'index.blocks.read_only_allow_delete': None}
        url = f'{self.host}/_all/_settings'
        resp = requests.put(url, json=body)
        out = resp.json()
        return out

    def set_max_result_window(self, index, num=5000000):
        self.create_index(index)
        url = f'{self.host}/{index}/_settings'
        body = {"index.max_result_window": num}
        resp = requests.put(url, json=body)
        out = resp.json()
        return out

    def set_field_type(self, index, field, dtype):
        assert dtype in ['geo', 'nest']
        self.create_index(index)
        if dtype == 'geo':
            dtype = 'geo_point'
        elif dtype == 'nest':
            dtype = 'nested'
        url = f'{self.host}/{index}/_mapping'
        body = {"properties": {field: {"type": dtype}}}
        resp = requests.put(url, json=body)
        out = resp.json()  # {"acknowledged": true}
        return out

    def put_mapping(self, index, mapping):
        """字段类型概述
            一级分类	二级分类	具体类型
            核心类型	字符串类型  text,  keyword
            整数类型	integer,long,short,byte
            浮点类型	double,float,half_float,scaled_float
            逻辑类型	boolean
            日期类型	date
            范围类型	range
            二进制类型	binary
            复合类型	数组类型	array
            对象类型	object
            嵌套类型	nested
            地理类型	地理坐标类型	geo_point
            地理地图	geo_shape
            特殊类型	IP类型	ip
            范围类型	completion
            令牌计数类型	token_count
            附件类型	attachment
            抽取类型	percolator
        """
        url = f'{self.host}/{index}/_mapping'
        resp = requests.put(url, json=mapping)
        return resp.json()

    async def async_index_exist(self, index):
        url = f'{self.host}/{index}'
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, headers=self.headers, timeout=3)
            out = 'error' not in resp.json()
        except requests.exceptions.ReadTimeout:
            logs.rotate.error(f'url={url}   超时错误')
            out = None
        except Exception:
            error = '\n'.join(traceback.format_exception(*sys.exc_info()))
            logs.rotate.error(f'url={url}  {error}')
            out = None
        return out

    async def async_search(self, index, query):
        url = f'{self.host}/{index}/_doc/_search'
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=query, headers=self.headers, timeout=3)
            out = resp.json()
        except requests.exceptions.ReadTimeout:
            logs.rotate.error(f'url={url}  query={query}  超时错误')
            out = None
        except Exception:
            error = '\n'.join(traceback.format_exception(*sys.exc_info()))
            logs.rotate.error(f'url={url}  query={query}  {error}')
            out = None
        return out

    def search(self, index, query, timeout=20):
        url = f'{self.host}/{index}/_doc/_search'
        try:
            resp = requests.post(url, json=query, headers=self.headers, timeout=timeout)
            out = resp.json()
        except requests.exceptions.ReadTimeout:
            logs.rotate.error(f'url={url}  query={query}  超时错误')
            out = None
        except Exception:
            error = '\n'.join(traceback.format_exception(*sys.exc_info()))
            logs.rotate.error(f'url={url}  query={query}  {error}')
            out = None
        return out

    def agg(self, index, query):
        url = f'{self.host}/{index}/_doc/_search'
        try:
            resp = requests.post(url, json=query, headers=self.headers, timeout=3)
            out = resp.json()
        except requests.exceptions.ReadTimeout:
            logs.rotate.error(f'url={url}  query={query}  超时错误')
            out = None
        except Exception:
            error = '\n'.join(traceback.format_exception(*sys.exc_info()))
            logs.rotate.error(f'url={url}  query={query}  {error}')
            out = None
        return out

    async def async_agg(self, index, query):
        url = f'{self.host}/{index}/_doc/_search'
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=query, headers=self.headers, timeout=3)
            out = resp.json()
        except requests.exceptions.ReadTimeout:
            logs.rotate.error(f'url={url}  query={query}  超时错误')
            out = None
        except Exception:
            error = '\n'.join(traceback.format_exception(*sys.exc_info()))
            logs.rotate.error(f'url={url}  query={query}  {error}')
            out = None
        return out

    def scroll(self, index, query, wait='10m', timeout=20000):
        if isinstance(query, Query):
            query = query()
        if not self.index_exist(index):
            return []
        return ScrollIter(self.host, index, query, wait=wait, timeout=timeout)

    def scroll_batch(self, index, query, wait='10m', timeout=20000):
        if isinstance(query, Query):
            query = query()
        if not self.index_exist(index):
            return []
        return ScrollBatch(es=self, index=index, query=query, wait=wait, timeout=timeout)

    async def async_del_doc(self, index, doc_id):
        url = f'{self.host}/{index}/_doc/{doc_id}'
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.delete(url, headers=self.headers, timeout=3)
            resp_obj = resp.json()
            logs.rotate.info(resp_obj)
            out = True
            if not out:
                logs.rotate.error(f'del resp={resp_obj}')
        except requests.exceptions.ReadTimeout:
            logs.rotate.error(f'del url={url}  超时错误')
            out = None
        except Exception:
            error = '\n'.join(traceback.format_exception(*sys.exc_info()))
            logs.rotate.error(f'del url={url}  {error}')
            out = None
        return out

    def del_doc(self, index, doc_id):
        url = f'{self.host}/{index}/_doc/{doc_id}'
        try:
            resp = requests.delete(url, headers=self.headers, timeout=5)
            resp_obj = resp.json()
            logs.rotate.info(resp_obj)
            out = True
            if not out:
                logs.rotate.error(f'del resp={resp_obj}')
        except requests.exceptions.ReadTimeout:
            logs.rotate.error(f'del url={url}  超时错误')
            out = None
        except Exception:
            error = '\n'.join(traceback.format_exception(*sys.exc_info()))
            logs.rotate.error(f'del url={url}  {error}')
            out = None
        return out

    def del_field(self, index, field, query=None):
        url = f'{self.host}/{index}/_doc/_update_by_query'
        if query is None:
            query = Query.exist(field)()
        elif isinstance(query, Query):
            query = query()
        body = {'query': query['query'], 'script': {
            'source': f'ctx._source.remove("{field}");',
            'lang': 'painless',
        }}
        print(body)
        resp = requests.post(url, headers=self.headers, json=body, timeout=5)
        resp_obj = resp.json()
        return resp_obj

    def del_index(self, index):
        url = f'{self.host}/{index}'
        logs.rotate.info(f'url={url}')
        try:
            resp = requests.delete(url, headers=self.headers, timeout=3)
            logs.rotate.info(f'index={index} resp={resp.text}')
            if resp.status_code == 404:
                return {'ok': False, 'detail': f'index="{index}" 不存在'}
            if resp.status_code == 200 and resp.json().get('acknowledged'):
                return {'ok': True, 'detail': f'index="{index}" 已经删除'}
            return {'ok': False, 'detail': resp.text}
        except Exception as e:
            logs.rotate.error(f'error={e}')
            return {'ok': False, 'detail': '未获取ES的返回数据'}

    async def async_cat_indices(self):
        url = f'{self.host}/_cat/indices?format=json'
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.headers, timeout=3)
            resp_obj = resp.json()
            for index in resp_obj:
                for k, v in list(index.items()):
                    if '.' in k:
                        index[k.replace('.', '_')] = index.pop(k)  # 前端用 .的话会被当做属性引用，所以替换成下划线
            logs.rotate.info(f'resp={resp_obj}')
            return resp_obj

    def get_bulk_txt(self, docs):
        txts = []
        for i, doc in enumerate(docs):
            for k in ['_index', 'opt']:
                if k not in doc:
                    raise ValueError(f'docs[{i}] 缺少key "{k}"')
            opt = doc['opt']
            assert opt in ['create', 'delete', 'update', 'index'], f'opt错误 "{opt}"'
            if opt != 'delete' and '_source' not in doc:
                raise ValueError(f'docs[{i}] 缺少key "_source"')

            line = {opt: {'_index': doc['_index']}}
            if '_id' in doc:
                line[opt]['_id'] = doc['_id']
            txts.append(json.dumps(line) + '\n')
            if opt in ['index', 'create']:
                txts.append(json.dumps(doc['_source']) + '\n')
            elif opt == 'update':
                txts.append(json.dumps({'doc': doc['_source']}) + '\n')
        txt = ''.join(txts)
        return txt

    async def async_save_bulk(self, docs, is_break=True):
        # 存储一个bulk
        # docs = [{_index: '', _id: '', _source: {}, 'opt': 'update'}]
        # opt可取值: update局部更新   index可以创建也可以全量替换   create智能创建   delete删除
        url = f'{self.host}/_bulk'
        if not docs:
            return
        txt = self.get_bulk_txt(docs)
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, data=txt, headers=self.headers, timeout=30)
        resp_obj = resp.json()
        if resp_obj.get('error'):
            all_ok = False
        elif resp_obj.get('errors'):
            all_ok = False
        else:
            all_ok = True
        if not all_ok:
            if 'items' in resp_obj:
                # 筛选掉 操作成功的item
                resp_obj['items'] = [t for t in resp_obj['items'] if any([info.get('status') != 200 for info in t.values()])]
            logs.brief.error(resp_obj)
            if is_break:
                logs.brief.error('exit()')
                exit()
        return all_ok

    def save_bulk(self, docs, is_break=True):
        # 存储一个bulk
        # docs = [{_index: '', _id: '', _source: {}, 'opt': 'update'}]
        # opt可取值: update局部更新   index可以创建也可以全量替换   create智能创建   delete删除
        url = f'{self.host}/_bulk'
        if not docs:
            return
        txt = self.get_bulk_txt(docs)
        resp = requests.post(url, data=txt, headers=self.headers, timeout=30)
        resp_obj = resp.json()
        if resp_obj.get('error'):
            all_ok = False
        elif resp_obj.get('errors'):
            all_ok = False
        else:
            all_ok = True
        if not all_ok:
            if 'items' in resp_obj:
                # 筛选掉 操作成功的item
                resp_obj['items'] = [t for t in resp_obj['items'] if any([info.get('status') != 200 for info in t.values()])]
            logs.brief.error(resp_obj)
            if is_break:
                logs.brief.error('exit()')
                exit()
        return all_ok

    def save_bulk_all(self, docs, size=5000, desc='save_bulk_all', is_break=True):
        # 通过bulk接口把数据存入ES
        # docs = [{_index: '', _id: '', _source: {}, 'opt': 'update'}]
        # opt可取值: update局部更新   index可以创建也可以全量替换   create智能创建   delete删除
        all_is_ok = True
        for i in tqdm(range(0, len(docs), size), desc=desc):
            all_is_ok = all_is_ok and self.save_bulk(docs[i:i + size], is_break=is_break)
        return all_is_ok

    def backup_save(self, zip_path, *indexs):
        # 备份ES， 存储到文件夹中
        zip_path = os.path.abspath(zip_path)
        os.makedirs(os.path.dirname(zip_path), exist_ok=True)
        if os.path.exists(zip_path):
            raise InfoError(f'{zip_path} 文件已存在')
        index__mapping = {}
        for index in indexs:
            index__mapping[index] = self.get_map(index)
        z = ZipTool(zip_path, 'w')
        z.add('index__mapping.pkl', pickle.dumps(index__mapping))
        query = Query.all(size=1000)  # size 不能太大， 避免requests传递data不支持大数据
        for index in indexs:
            for i, batch in enumerate(tqdm(self.scroll_batch(index, query), desc=f'backup_save: {index}')):
                arcname = f'{index}/{i}.pkl'
                content = pickle.dumps(batch)
                z.add(arcname, content)
        logs.rotate.info(f'已完成备份 {zip_path}')

    def backup_load(self, zip_path, opt='index'):
        # 从备份中恢复数据到ES     opt=update局部更新 / index可以创建也可以全量替换
        f = ZipTool(zip_path, 'r')
        index__ok_ids = {}
        errors = []
        index__mapping = pickle.loads(f.read('index__mapping.pkl'))
        for index, mapping in index__mapping.items():
            logs.rotate.info(f'backup_load index={index}')
            if not self.index_exist(index):
                self.create_index(index)
            resp = self.put_mapping(index, mapping[index]['mappings'])
            if not resp.get('acknowledged'):
                logs.rotate.error(f'index({index}) mapping ERROR')
                logs.rotate.error(str(resp))
                raise InfoError('index mapping ERROR')

        for name in tqdm(f.namelist(), desc='backup_load'):
            if name == 'index__mapping.pkl':
                continue
            batch = pickle.loads(f.read(name))
            for doc in batch:
                doc['opt'] = opt
            try:
                self.save_bulk(batch)
                for doc in batch:
                    index__ok_ids.setdefault(doc['_index'], []).append(doc['_id'])
            except:
                errors.append(name)
        logs.rotate.info(f'已恢复备份 {zip_path}  errors~{len(errors)}')
        return index__ok_ids, errors

    def get_agg_list(self, index, field, query=None, size=100):
        # 如果field值是文本，则需要末尾添加 .keyword    如果是整数则不需要添加
        # return  = [{'doc_count': 数量, 'key': '文本内容'}]
        query = query or Query.all()
        q = Query.aggs({'resp': {'field': field, 'size': size}}, query=Query.extract_query(query))
        resp = self.agg(index, q)
        if 'aggregations' in resp and 'resp' in resp['aggregations'] and 'buckets' in resp['aggregations']['resp']:
            return resp['aggregations']['resp']['buckets']
        else:
            raise InfoError(f'resp={resp}')

    async def async_get_agg_list(self, index, field, query=None, size=100):
        # 如果field值是文本，则需要末尾添加 .keyword    如果是整数则不需要添加
        # return  = [{'doc_count': 数量, 'key': '文本内容'}]
        query = query or Query.all()
        q = Query.aggs({'resp': {'field': field, 'size': size}}, query=Query.extract_query(query))
        resp = await self.async_agg(index, q)
        if 'aggregations' in resp and 'resp' in resp['aggregations'] and 'buckets' in resp['aggregations']['resp']:
            return resp['aggregations']['resp']['buckets']
        else:
            raise InfoError(f'resp={resp}')

    def get_agg_count(self, index, field, query=None):
        # 返回 聚类 bulket 数量
        q = {
            'size': 0,
            'aggs': {
                'Key1': {
                    'terms': {
                        'field': field,
                    },
                },
                "count": {
                    "cardinality": {
                        "field": field
                    }
                }
            }
        }
        if query:
            q['query'] = Query.extract_query(query)
        resp = self.agg(index, q)
        return resp['aggregations']['count']['value']

    def get_map(self, index=''):
        if index:
            url = f'{self.host}/{index}/_mapping'
        else:
            url = f'{self.host}/_mapping'
        resp = requests.get(url)
        out = resp.json()
        return out


if __name__ == '__main__':
    es = EsTool('http://127.0.0.1:9200')
    kv = {
        '_fn': 'bool',
        '_param': {'must': [{'_fn': 'term', '_param': {'key': 'key1.keyword', 'values': 'xxxxx'}}]},
        '_call': {'start': 10}
    }
    # x = Query.json_to_query(kv)
    # pprint(x)

    # print(es.set_disk())
    # print(es.set_not_read_only())
    # print(es.all_index())
    data = [
        {'_index': 'test33', '_source': {'value': 1}, 'opt': 'index'},
        {'_index': 'test33', '_source': {'value': 2}, '_id': 'test2', 'opt': 'index'},
    ]
    es.save_bulk(data)

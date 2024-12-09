import os
from fish_tool.log_tool import logs, InfoError
import requests.exceptions as e
import urllib3.exceptions
import socket
import uvicorn
# 便于其他代码导入（不能删除）
from pydantic import BaseModel
from fastapi import FastAPI, Response, APIRouter, Header, Request, HTTPException, Depends, Security, Cookie

# 常用的requests异常
net_excepts = (
    e.ReadTimeout, e.ChunkedEncodingError, e.ConnectionError,
    socket.gaierror,
    urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError
)

# 设置 uvicorn的日志格式
if uvicorn:
    fmt = '[%(levelname)s %(asctime)s %(filename)s %(funcName)s:%(lineno)d] %(message)s'
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["default"]["fmt"] = fmt

app_cache = {}


def get_app(app_name='default'):
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.middleware.gzip import GZipMiddleware
    if app_name not in app_cache:
        # 参数关闭/docs /docs/oauth2-redirect /redoc /openapi.json
        app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
        # 允许跨域 便与测试
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        # 添加gzip压缩中间件
        app.add_middleware(GZipMiddleware, minimum_size=1000)
        app_cache[app_name] = app
    return app_cache[app_name]


def show_router(app):
    for _router in app.router.routes:
        logs.tmp.info(_router.path or _router.path_format)


def deploy(app, port=80):
    uvicorn.run(app, host='0.0.0.0', port=port)


def add_file_url(app, url, path):
    # 添加静态文件的url
    from fastapi.staticfiles import StaticFiles
    if not os.path.isfile(path):
        raise InfoError(f'静态url 文件不存在={path}')
    scope = {'method': 'GET', 'headers': {}}
    folder = os.path.dirname(path)
    name = os.path.basename(path)
    static = StaticFiles(directory=folder)

    @app.get(url)
    async def aifish_manage():
        return await static.get_response(name, scope)

    # 示范： add_file_url(app, '/favicon.ico', 'data/img/icon.jpg')


def add_dir_url(app, url, path):
    # 添加静态文件夹的url
    from fastapi.staticfiles import StaticFiles
    if not os.path.isdir(path):
        raise InfoError(f'静态url 文件夹不存在={path}')
    app.mount(url, StaticFiles(directory=path), name=url)

# 为了方便引用 载入常用对象
from fish_tool.log_tool import logs, InfoError
from fish_tool.config_base import BaseConfig

"""   依赖关系
log_tool
    无
    
sys_tool
    log_tool
register
    log_tool
config_base
    log_tool
    
ai.laboratory
    log_tool
ai.torch_tool
    log_tool
    
db.es_tool
    log_tool
db.sqlite_tool
    log_tool
db.neo_tool
    log_tool
    
net.spider_tool
    log_tool
net.proxy_16yun.py
    log_tool
    
"""

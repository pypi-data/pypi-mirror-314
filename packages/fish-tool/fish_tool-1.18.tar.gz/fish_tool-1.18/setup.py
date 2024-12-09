from setuptools import setup, find_packages

setup(
    name="fish_tool",
    version="1.18",
    author="aifish",
    url="https://gitee.com/laowangzi/fish_tool",
    author_email="ofyu@163.com",
    description="some tool code",
    packages=find_packages(),
    install_requires=[
        'pyyaml>=6.0',
        'tqdm>=4.36.1',
        'requests>=2.22.0',
        'httpx>=0.18.1',
        "fastapi>=0.90.0",
        "uvicorn>=0.20.0",
    ],
    extras_require={
        'AI': [
            "torch>=1.0"
        ],
        'db': [
            "pymysql>=1.0.2"
        ],
    },
    python_requires='>=3.8',
)

"""
build代码
python setup.py sdist

上传到PyPi
(pip install twine)
twine upload dist/*

由于使用了类型注释 typing.Union 最低python版本为3.8

更新内容
1.1 2023.03.22 db/sqlite_tool.py 增加字段功能
1.11 2023年3月27日 db/sqlite_tool.py 增加scroll功能
1.12 2023年7月18日 ai/torch_tool.py 增加load_model(model, path, device=None)
1.13 2023年11月4日 sys_tool.py 增加 stacks_to_txt 调用堆栈文本
1.14 2023年11月4日 sys_tool.py stacks_to_txt stack_num默认值从1改为3
1.15 2023年11月11日 spider_tool.py post get (自动重试、自动打日志的功能)
1.16 2023年12月17日 ai/torch_tool.py ce_loss mask2维自动补充到3维
1.17 2024年12月08日 增加中文的简繁体转换  Etree增加子节点, Etree改为Enode，增加txt属性，去掉了txts函数
1.18 2024年12月08日 修复提取文本的br转成换行
"""

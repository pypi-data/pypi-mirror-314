import argparse
from fish_tool import register
import os
from fish_tool.log_tool import logs

parser = argparse.ArgumentParser(description='AI实验室')

parser.add_argument('config_name', type=str, help='配置名称')
parser.add_argument('--folder', type=str, default='', help='模型存储位置')

parser.add_argument('--start', type=int, default=0, help='训练起始位置（闭区间）')
parser.add_argument('--end', type=int, default=900000000, help='训练结束位置（开区间）')
parser.add_argument('--repeat', type=int, default=1, help='训练数据重复次数')


def root(*path):
    out = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', *path))
    return out


def train(config_name, folder='', start=0, end=900000000, repeat=1):
    # 训练函数（执行训练流程）
    # 注意： 必须先import注册对象所在的模块，才能正常使用register （使用register.walk_import)
    config = register.get(config_name)()
    if folder:
        config.folder = root(folder)
    else:
        config.folder = root(f'data/{config_name}')
    logs.reset(config.folder)
    logs.brief.info(f'name={config_name}   config={config}')
    Learner = register.get(config.learner_name)
    learner = Learner(config)
    learner.train(start=start, end=end, repeat=repeat)


def cmd_train():
    # 通过命令行参数 执行训练函数
    args = parser.parse_args()
    config_name = args.config_name
    folder = args.folder
    train(config_name, folder, start=args.start, end=args.end, repeat=args.repeat)

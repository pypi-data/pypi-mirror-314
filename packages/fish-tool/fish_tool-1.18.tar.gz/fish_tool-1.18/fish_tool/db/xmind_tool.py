import json
import zipfile
from collections import Counter


def read_xmind(path):
    f = zipfile.ZipFile(path, 'r')
    data = json.loads(f.read('content.json'))
    return data


def get_leafs(data, pre=''):
    out = []
    if isinstance(data, list):
        for one in data:
            out.extend(get_leafs(one, pre))
        return out
    if 'rootTopic' in data:
        data = data['rootTopic']
    title = data['title']
    if 'children' in data and 'attached' in data['children']:
        pre = f'{pre}_{title}' if pre else title
        for sub in data['children']['attached']:
            out.extend(get_leafs(sub, pre))
    else:
        title = data['title']
        info = {
            'id': data['id'],
            'title': title,
            'join_title': f'{pre}_{title}' if pre else title
        }
        if 'labels' in data:
            info['labels'] = data['labels']
        if 'children' in data and 'callout' in data['children']:
            info['callout'] = data['children']['callout']
        out.append(info)
    return out


def check_leaf_is_same(path):
    # 检查标签体系的叶子节点的文本是否有重复的
    data = read_xmind(path)
    leafs = get_leafs(data)
    leaf__count = Counter([t['title'] for t in leafs])
    print(f'leaf__count={leaf__count}')
    print('=' * 60)
    for leaf, c in leaf__count.items():
        if c > 1:
            print('EORROR 重复的标签： ', leaf, c)


if __name__ == '__main__':
    check_leaf_is_same(path='C:/Users/fish/Desktop/标签体系/小说标签体系8.xmind')

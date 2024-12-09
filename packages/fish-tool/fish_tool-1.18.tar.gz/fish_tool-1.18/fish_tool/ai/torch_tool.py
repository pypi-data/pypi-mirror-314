import random
import io
import types
import os
import copy
import math
import numpy as np
import sentencepiece
import torch
import torch.nn.parameter
from fish_tool.log_tool import logs, InfoError
from fish_tool.db import zip_tool

device = os.environ.get('CUDA_VISIBLE_DEVICES', '-1')


def list_tensor(*values, dtype=torch.long):
    return [tensor(v, dtype) for v in values]


def tensor(values, dtype=torch.long):
    # 把数组或者字典 转换成 tensor
    if not values:  # 空数组、空字典等等
        return values
    if isinstance(values, (list, np.ndarray)):
        return cuda(torch.tensor(values, dtype=dtype))
    elif isinstance(values, dict):
        return {k: tensor(v) for k, v in values.items()}
    else:
        return values


def count_to_weight(count, base=0.1):
    # 通过 统计数量 计算 损失加权
    max_num = max(count)
    if not max_num:
        return [1 for i in count]
    weight = [max_num / (t + base * max_num) for t in count]
    weight = cuda(torch.tensor(weight, dtype=torch.float))
    return weight


def init_linear(input_linear, seed=1337):
    """初始化全连接层权重
    """
    torch.manual_seed(seed)
    scope = np.sqrt(6.0 / (input_linear.weight.size(0) + input_linear.weight.size(1)))
    torch.nn.init.uniform_(input_linear.weight, -scope, scope)
    # nn.init.uniform(input_linear.bias, -scope, scope)
    if input_linear.bias is not None:
        input_linear.bias.data.zero_()


class WarmupOptim:
    # 带预热机制的优化器
    def __init__(self, params, lr=1e-3, warm_step=10000, warm_num=10, optim=None, **kv):
        optim = optim or torch.optim.SGD
        # warm_step学习率预热提升到100%需要的总步数     warm_num学习率变化的总次数
        if isinstance(params, types.GeneratorType):
            params = list(params)  # 生成器对象转换成数组， 避免第二次调用时报错
        self.optim_cls = optim
        self.params = params
        self.warm_step = warm_step
        self.kv = kv
        self.warm_frequency = warm_step // warm_num
        self.add_lr = lr / (warm_num + 1)
        self.lr = self.add_lr
        self.optim = self.get_optim()
        self.count = 1

    def get_optim(self):
        optimizer = self.optim_cls(self.params, lr=self.lr, **self.kv)
        return optimizer

    def zero_grad(self):
        self.optim.zero_grad()

    def step(self):
        self.optim.step()
        if self.count <= self.warm_step and self.count % self.warm_frequency == 0:
            self.lr += self.add_lr
            logs.tmp.info(f'update lr = {self.lr}')
            self.optim = self.get_optim()
        self.count += 1


class MovingAverage:
    # Exponentially Weighted Moving-Average 指数加权平均 指数加权滑动平均
    def __init__(self, beta=0.95):
        assert 0 < beta < 1
        self._value = None
        self.beta = beta

    @property
    def value(self):
        if self._value is None:
            return 0
        return self._value

    def update(self, value):
        if self._value is None:
            self._value = value
        else:
            new_value = self.beta * self._value + (1 - self.beta) * value
            if math.isnan(new_value):
                logs.tmp.error(f'value={value}  old={self._value}  new={new_value}')
            else:
                self._value = new_value
        return self._value


class SentencePieceVocab:
    def __init__(self, sp_path):
        if not os.path.isfile(sp_path):
            logs.brief.warning(f'sp_path文件不存在： {sp_path}')
        self.sp = sentencepiece.SentencePieceProcessor()
        self.sp.load(sp_path)

    def char_id(self, char):
        return self.sp.PieceToId(char)  # 如果piece不存在则输出是0

    def char(self, char_id):
        return self.sp.IdToPiece(char_id)

    def char_id_bak(self, char):
        pad_id = 6
        #  sp.EncodeAsPieces('萨')->['▁', '萨']   sp.encode_as_ids('阿')->[19, 893]
        this_encode = self.sp.encode_as_ids(char)
        if len(this_encode) >= 1:
            return this_encode[-1]
        else:
            return pad_id


def select_vec_3d(seq_vec, idxs):
    # seq_vec~(bsz, max_seq_len, dim)   idxs~(num)  idxs在dim=1上抽取向量
    # return~(bsz, num, dim)
    bsz, max_seq_len, dim = seq_vec.size()
    idxs = torch.tensor(idxs, dtype=torch.long, device=seq_vec.device)
    idxs = idxs.unsqueeze(0)
    idxs = idxs.unsqueeze(2)
    idxs = idxs.expand(bsz, -1, dim)
    return seq_vec.gather(1, idxs).contiguous()


def get_seq_combination_pair(seq_vec):
    # 输入向量序列 形成两两组合的pair向量序列
    # seq_vec~(bsz, max_seq_len, dim)
    # return: pair_vec~(bsz, join_num, dim)    join_num=max_seq_len*(max_seq_len-1)/2 两两成组
    max_seq_len = seq_vec.size(1)
    small_idxs = []  # (join_num)
    big_idxs = []  # (join_num)
    for j in range(1, max_seq_len):
        for i in range(j):
            small_idxs.append(i)
            big_idxs.append(j)
    left_vec = select_vec_3d(seq_vec, small_idxs)  # (bsz, join_num, dim)
    right_vec = select_vec_3d(seq_vec, big_idxs)  # (bsz, join_num, dim)
    pair_vec = torch.cat([left_vec - right_vec, left_vec * right_vec], dim=-1)  # (bsz, join_num, dim*2)
    return pair_vec


def __cuda(v):
    if torch.cuda.is_available() and hasattr(v, 'cuda'):
        return v.cuda()
    else:
        return v


def recusive__cuda(model):
    if isinstance(model, dict):
        return {k: recusive__cuda(v) for k, v in model.items()}
    elif isinstance(model, (list, tuple, set)):
        return [recusive__cuda(t) for t in model]
    else:
        return __cuda(model)


def cuda(*model):
    # 对数组参数的包装 调用代码省事一点
    if len(model) == 1:
        return recusive__cuda(model[0])
    else:
        return [recusive__cuda(t) for t in model]


def clone_module(module, num, share=False):
    if share:
        m = torch.nn.ModuleList([module for i in range(num)])
    else:
        m = torch.nn.ModuleList([copy.deepcopy(module) for i in range(num)])
    return m


def get_model_param_num(model):
    # 获取模型 参数量
    out = 0
    if isinstance(model, torch.nn.Module):
        out = sum(x.numel() for x in model.parameters())
    elif isinstance(model, torch.nn.parameter.Parameter):
        out = model.numel()
    return out


def get_model_layers_param_num(model):
    # 获取模型每层的参数量
    out = f'{model.__class__}  模型参数总量={get_model_param_num(model)}\n'
    for k, value in model.named_parameters():
        out += f'{k: <70} ---> {get_model_param_num(value)}\n'
    return out


def total_grad(model):
    # 查看一个模型的全部梯度之和
    out = 0
    for k, value in model.named_parameters():
        if isinstance(value, torch.nn.Module):
            out += total_grad(value)
        elif isinstance(value, torch.nn.parameter.Parameter):
            if value.grad is not None:
                out += value.grad.abs().sum()
    return out


def cut_grad(model, max_grad):
    # 对模型进行梯度剪裁 ，避免梯度更新过于剧烈
    torch.nn.utils.clip_grad_value_(model.parameters(), max_grad)


def count_to_lr_weight(counts, base=0.05, device=None):
    big = max(counts)
    add = big * base  # 平滑
    counts_pad = [t + add for t in counts]
    big += add
    weight = [big / t for t in counts_pad]
    weight = torch.tensor(weight, dtype=torch.float, device=device)
    return weight


def save_model(model, path):
    if hasattr(model, 'module'):
        model = getattr(model, 'module')  # torch.nn.parallel.DistributedDataParallel
    path = os.path.abspath(path)
    save_dir = os.path.dirname(path)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    torch.save(model.state_dict(), path)
    return model


def load_cpu_model(model, path):
    # 之后废弃掉
    if isinstance(path, bytes):
        # 如果是二进制 则已经读取了 要包装一下
        path = io.BytesIO(path)
    model_state = torch.load(path, map_location=torch.device('cpu'))
    model.load_state_dict(model_state)
    return model


def load_model(model, path, device=None):
    if isinstance(path, bytes):
        # 如果是二进制 则已经读取了 要包装一下
        path = io.BytesIO(path)
    if device is None:
        device = torch.device('cpu')
    elif isinstance(device, int):
        device = torch.device("cuda", device)
    model_state = torch.load(path, map_location=device)
    model.load_state_dict(model_state)
    return model


def model_save_zip(model, path, name='model.pth'):
    # 把模型存储到zip文件中 注意存储过程很慢
    save_dir = os.path.dirname(os.path.abspath(path))
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    zip = zip_tool.ZipTool(path)
    if zip.is_exist(name):
        raise InfoError(f'模型存储错误 path={path} name={name} 已经存在')
    f = io.BytesIO()
    torch.save(model.state_dict(), f)
    pth = f.getvalue()
    zip.add(name, pth)


def model_load_zip(model, path, name='model.pth'):
    zip = zip_tool.ZipTool(path, 'r')
    pth = zip.read(name)
    model = load_cpu_model(model, pth)
    return model


def __init_model_weights(module, initializer_range=0.02, seed=1337):
    torch.manual_seed(seed)
    if isinstance(module, torch.nn.Linear):
        scope = math.sqrt(6.0 / (module.weight.size(0) + module.weight.size(1)))
        torch.nn.init.uniform_(module.weight, -scope, scope)
        if module.bias is not None:
            module.bias.data.zero_()
    elif isinstance(module, torch.nn.Embedding):
        module.weight.data.normal_(mean=0.0, std=initializer_range)
        if isinstance(module, torch.nn.Linear) and module.bias is not None:
            module.bias.data.zero_()
    elif isinstance(module, torch.nn.LayerNorm):
        module.bias.data.zero_()
        module.weight.data.fill_(1.0)


def init_model_weights(model):
    model.apply(__init_model_weights)


def ce_loss(pred, target, weight=None, mask=None):
    # pred~(bsz, seq_len, cls_num)   target~(bsz, seq_len)   mask~(bsz, seq_len) 对应位置 1=计算loss 0=不计算loss
    # 安全的交叉熵损失, 避免出现NaN的情况
    target = torch.nn.functional.one_hot(target, num_classes=pred.size(-1)).float()  # ~ (bsz, seq_len, cls_num)
    pred = torch.softmax(pred, dim=-1)  # ~ (bsz, seq_len, cls_num)
    pred = pred.clamp(min=1e-20, max=1)
    shape_loss = target * torch.log(pred)  # ~ (bsz, seq_len, cls_num)
    if mask is not None:
        if mask.dim() < shape_loss.dim():
            mask = mask.unsqueeze(2)
        mask = mask.float()
        shape_loss = shape_loss * mask
    shape_loss = shape_loss.sum(dim=-1)  # ~ (bsz, seq_len)
    if weight is not None:
        shape_loss = shape_loss * weight
    loss = -torch.mean(shape_loss)
    return loss


def ce_loss_with_probability(pred, target, weight=None, mask=None):
    # pred~(bsz, seq_len)二分类的概率值   target~(bsz, seq_len)取值只能是0或1
    target = target.float()
    pred_1 = (1 - pred).clamp(min=1e-20, max=1)
    pred = pred.clamp(min=1e-20, max=1)
    if weight is None:
        weight0, weight1 = 1, 1
    else:
        weight0, weight1 = weight
    shape_loss = -(1 - target) * torch.log(pred_1) * weight0 - target * torch.log(pred) * weight1
    loss = torch.mean(shape_loss)
    return loss


def pad_1d(line, max_num, pad=0):
    # line是1维数组， 补全到max_num长度
    out = line + [pad] * (max_num - len(line))
    return out


def pad_batch_seq(batch_seq, pad=0):
    # batch_seq 是2维数组， (batch_size, seq_len)
    max_len = max(len(seq) for seq in batch_seq)
    mask = []
    input_ids = []
    for seq in batch_seq:
        input_ids.append(pad_1d(seq, max_len, pad=pad))
        mask.append([1] * len(seq) + [0] * (max_len - len(seq)))
    return input_ids, mask


def pad_2d(matrix, max_row, max_column, pad=0):
    # matrix是2维数组， 补全到max-row行数， max-column列数
    row = len(matrix)
    if row:
        column = len(matrix[0])
    else:
        # 如果原矩阵是空白矩阵，直接返回pad组成的对应尺寸的矩阵
        return [[pad] * max_column for _ in range(max_row)]
    out = []
    for line in matrix:
        out.append(line + [pad] * (max_column - column))
    out += [[pad] * max_column for _ in range(max_row - row)]
    return out


def frozen(net):
    # 冻结网络的参数
    for param in net.parameters():
        param.requires_grad = False


def unfrozen(net):
    # 解冻网络的参数
    for param in net.parameters():
        param.requires_grad = True


def graph_to_cliques(nodes, edges):
    """
    输入一个无向图（顶点和边），解码出这个图全部的团
    :param nodes: 顶点数组   range(1, 6)
    :param edges: 边数组, 每个边由二元组表示  {(1, 2), (1, 4), (1, 5), (2, 3), (2, 5), (3, 5), (4, 5)}
    :return: 顶点的二维数组，表示每个团    [[1, 2, 5], [1, 4, 5], [2, 3, 5]]
    """
    nodes = sorted(nodes)
    node_relation_nodes = {}
    for a, b in edges:
        node_relation_nodes.setdefault(a, set()).add(b)
        node_relation_nodes.setdefault(b, set()).add(a)

    cliques = []
    looked_nodes = set()
    for node in nodes:
        relation_nodes = node_relation_nodes.get(node, set()) & looked_nodes
        __clique_add_node(cliques, node, relation_nodes)
        looked_nodes.add(node)
    cliques = [sorted(t) for t in cliques]
    cliques.sort()
    return cliques


def __clique_add_node(cliques, node, relation_nodes):
    # 操作 cliques 把节点加入到 已有的团， 或者新建一个团
    if not cliques:  # 如果已创建的团为空
        cliques.append({node})
        # logs.tmp.debug(f'\t创建一个团  已有cliques={cliques}')
        return
    if not relation_nodes:  # 当前节点没有任何边
        cliques.append({node})
        # logs.tmp.debug(f'\t创建一个团  已有cliques={cliques}')
        return
    share_vertexes = set()  # 当前节点加入的团的全部节点
    for i, clique in enumerate(cliques):
        if relation_nodes == clique:
            share_vertexes.update(clique)
            clique.add(node)
            # logs.tmp.debug(f'\t完整加入  已有cliques={cliques}')
        elif clique.issubset(relation_nodes):
            share_vertexes.update(clique)
            clique.add(node)
            # logs.tmp.debug(f'\t共享加入  已有cliques={clique}')
    left_vartexes = relation_nodes - share_vertexes  # 剩下的，没有加入到已有团里的边的节点
    if left_vartexes:
        left_vartexes.add(node)
        cliques.append(left_vartexes)
        # logs.tmp.debug(f'\t共享并创建一个团  已有cliques={cliques}')
    return


def pair_to_objs(ent_pair, ent_num):
    # 根据实体对是否属于同一个实体（边），解码出实体成组（最大团）
    if ent_num == 0:
        return []
    elif ent_num == 1:
        return [[0]]
    nodes = range(ent_num)
    edges = set()
    i = 0
    for big in range(1, ent_num):
        for small in range(big):
            if ent_pair[i] > 0:
                edges.add((small, big))
            i += 1
    cliques = graph_to_cliques(nodes, edges)
    return cliques


def decode_ner_line(tags):
    """
    :param tags: 数字 O=out  1=Begin  2=inner  3=end  4=single
    return: [(start, end)]  index左闭右开
    """
    out = []
    start = None
    for i, tag in enumerate(tags):
        if tag == 0:
            if start is not None:
                out.append((start, i))
                start = None
        elif tag == 1:
            if start is not None:
                out.append((start, i))
            start = i
        elif tag == 2:
            if start is None:
                start = i
        elif tag == 3:
            if start is None:
                start = i
            out.append((start, i + 1))
            start = None
        elif tag == 4:
            if start is not None:
                out.append((start, i))
            start = None
            out.append((i, i + 1))
    if start is not None:
        out.append((start, len(tags)))
    return out


def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


def randn(*size, variance=1.0, clamp=20.0, requires_grad=False):
    # 创建正态分布的张量
    vec = torch.randn(*size, requires_grad=requires_grad)
    vec = vec * variance
    assert clamp > 0
    vec.clamp_(min=-clamp, max=clamp)
    return vec


if __name__ == '__main__':
    # 测试pytorch计算精度不一致问题
    logit = torch.FloatTensor([0.621, 0.4067])
    soft = logit.softmax(-1)
    prob0 = 1 - soft[1]
    print(prob0.tolist(), soft.tolist())
    # (0.5533709526062012, [0.5533708930015564, 0.4466290771961212])

    ce_fn = torch.nn.CrossEntropyLoss()
    gold = torch.LongTensor([[0]])
    pred = torch.FloatTensor([[[0.621, 0.4067]]])
    pred = torch.FloatTensor([[[0.621, 0.6067]]])
    print(f'pred={pred.tolist()}')
    logit = pred.softmax(dim=-1)
    print(f'logit={logit}')
    prob = logit[:, :, 1]
    print(f'prob={prob}')
    print(f'ce_fn={ce_fn(pred.view(-1, 2), gold.view(-1))}')
    print(f'my_ce={ce_loss(pred, gold)}')
    print(f'ce_pr={ce_loss_with_probability(prob, gold)}')

    x = torch.FloatTensor([[0.6860]])
    xx = torch.mean(x)
    logs.tmp.info(f'x={x}  mean={xx}')

    x = torch.FloatTensor([[-0.6860]])
    xx = -torch.mean(x)
    logs.tmp.info(f'x={x}  mean={xx}')

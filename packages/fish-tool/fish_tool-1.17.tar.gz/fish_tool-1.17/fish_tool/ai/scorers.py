import torch
import sklearn.metrics


def get_f1(tp, fp, fn):
    if tp + fn + fp == 0:
        return -1
    if tp + fp == 0:
        precision = 0
    else:
        precision = tp / (tp + fp)
    if tp + fn == 0:
        recall = 0
    else:
        recall = tp / (tp + fn)
    if precision + recall < 0.000001:
        f1 = 0
    else:
        f1 = 2. * ((precision * recall) / (precision + recall))
    return f1


class MultiHotF1Scorer:
    # 计算多标签的F1
    def __init__(self):
        self.pred = []
        self.gold = []
        self.average = 'macro'

    def update(self, pred, gold):
        if isinstance(pred, torch.Tensor):
            pred = pred.long().tolist()
        if isinstance(gold, torch.Tensor):
            gold = gold.long().tolist()

        if pred:
            if not isinstance(pred[0], list):
                pred = [pred]  # 确保pred~~（bsz， doc_num）
                gold = [gold]
            for pred_line, gold_line in zip(pred, gold):
                self.pred.extend(pred_line)
                self.gold.extend(gold_line)

    def f1(self, reset=True):
        value = sklearn.metrics.f1_score(self.gold, self.pred, average=self.average)
        if reset:
            self.pred = []
            self.gold = []
        return value


class MultiLabelF1Scorer:
    # 多标签任务的F1   计算每个类别和总F1
    def __init__(self, labels):
        assert len(labels) > 0
        self.label_num = len(labels)
        self.label__scorer = {label: MultiHotF1Scorer() for label in labels}

    def update(self, label, pred, gold):
        self.label__scorer[label].update(pred, gold)

    def values(self):
        out = {}
        for label, scorer in self.label__scorer.items():
            out[label] = scorer.f1()
        out['f1'] = sum(out.values()) / self.label_num
        return out


class ClassifyF1Scorer:
    # 计算多分类的F1
    def __init__(self, average='macro', labels=None):
        assert average in ['binary', 'micro', 'macro', 'weighted', 'samples'], f'average={average} 不合法的参数值'
        self.pred = []
        self.gold = []
        self.average = average
        self.labels = labels

    def update(self, pred, gold):
        if isinstance(pred, torch.Tensor):
            pred = pred.long().tolist()
        if isinstance(gold, torch.Tensor):
            gold = gold.long().tolist()
        self.pred.extend(pred)
        self.gold.extend(gold)

    def f1(self, reset=True):
        value = sklearn.metrics.f1_score(self.gold, self.pred, average=self.average, labels=self.labels)
        if reset:
            self.pred = []
            self.gold = []
        return value


class SetF1Scorer:
    # 通过预测和golden的集合计算F1
    def __init__(self):
        self.tp, self.fp, self.fn = 0, 0, 0

    def update(self, pred_set, gold_set):
        self.tp += len(pred_set & gold_set)
        self.fp += len(pred_set - gold_set)
        self.fn += len(gold_set - pred_set)

    def f1(self, reset=True):
        f1 = get_f1(self.tp, self.fp, self.fn)
        if reset:
            self.tp, self.fp, self.fn = 0, 0, 0
        return f1

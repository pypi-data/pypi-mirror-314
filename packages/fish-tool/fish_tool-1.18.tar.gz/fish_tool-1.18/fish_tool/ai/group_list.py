class GroupList:
    # 组列表 每个组由有关联的成员组成， 如果两个组的成员有关联则2个组合并成一个组（类似并查集）
    def __init__(self):
        self.item__team = {}  # 每个成员对应的team team={'items': set(), 'key': item}
        self.key_items = set()  # 每个team出一个关键成员， 便于迭代返回全部team

    def __bool__(self):
        if self.item__team:
            return True
        return False

    def __len__(self):
        return len(self.key_items)

    def __iter__(self):
        # 返回全部组的成员集合
        for key in self.key_items:
            yield self.item__team[key]['items']

    def __str__(self):
        txt = ', '.join(str(t) for t in self)
        return txt

    def __call__(self, item):
        # 返回item所属的组的成员集合 如果不存在则返回空集合
        if item in self.item__team:
            return self.item__team[item]['items']
        return set()

    def add(self, *items):
        # 添加相互关联的成员列表
        key_item = items[0]
        items = set(items)
        key__rel_idx_set = {}
        for item in items:
            if item in self.item__team:
                team = self.item__team[item]
                key = team['key']
                if key not in key__rel_idx_set:
                    key__rel_idx_set[key] = team
        if len(key__rel_idx_set) == 0:
            team = {'items': items, 'key': key_item}
            self.key_items.add(key_item)
            for item in items:
                self.item__team[item] = team
        elif len(key__rel_idx_set) == 1:
            teams = list(key__rel_idx_set.values())
            teams[0]['items'].update(items)
            for item in items:
                self.item__team[item] = teams[0]
        else:
            teams = list(key__rel_idx_set.values())
            key_team = teams[0]
            key_team['items'].update(items)
            for item in items:
                self.item__team[item] = key_team
            for team in teams[1:]:
                key_team['items'].update(team['items'])
                for item in team['items']:
                    self.item__team[item] = key_team
                self.key_items.remove(team['key'])

__author__ = 'traveloka'


class PriorityQueue(object):
    def __init__(self):
        self.datas = list()

    def put(self, data, priority):
        pair = (data, priority)
        self.datas.append(pair)
        self.datas.sort(cmp=lambda x, y: x[1] - y[1])

    def deque(self):
        if len(self.datas) == 0:
            return None
        else:
            return self.datas.pop(0)[0]

    def size(self):
        return len(self.datas)

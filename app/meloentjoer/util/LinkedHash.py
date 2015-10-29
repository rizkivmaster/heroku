__author__ = 'traveloka'


class LinkedHash(list):
    def __hash__(self):
        return '.'.join(self).__hash__()
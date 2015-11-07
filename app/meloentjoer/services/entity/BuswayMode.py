from TransportationMode import TransportationMode


class BuswayMode(TransportationMode):

    def __init__(self):
        super(BuswayMode, self).__init__()
        self.corridor = None

    def __str__(self):
        parent_str = super(BuswayMode, self).__str__()
        return '{0},{1}'.format(parent_str, self.corridor)

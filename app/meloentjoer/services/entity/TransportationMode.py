# TODO separate TransportationMode from GeneralMode such that WalkMode does not belong to TransportationMode
class TransportationMode(object):
    def __init__(self):
        self.name = None
        self.price = None
        self.eta = None
        self.destination = None
        self.origin = None
        self.heading_to = None
        self.heading_from = None

    def cost(self):
        return self.eta

    def __str__(self):
        return '{0},{1},{2},{3},{4}'.format(self.origin, self.name, self.destination, self.price, self.eta)

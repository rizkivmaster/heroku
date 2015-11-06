class BusState(object):
    def __init__(self):
        self.name = None
        self.last_station = None
        self.last_time_stop = None
        self.previous_station = None
        self.previous_time_stop = None
        self.stop_list = []
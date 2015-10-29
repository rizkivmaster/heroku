class BusState:
    def __init__(self):
        self.last_station = None
        self.last_time_stop = None
        self.previous_station = None
        self.previous_time_stop = None
        self.stop_list = []
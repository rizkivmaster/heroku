class BusTrackData(object):
    def __init__(self, name=None, latitude=None, longitude=None, speed=None):
        """
        :type name:str
        :type latitude:float
        :type longitude:float
        :type speed:float
        :param name:str
        :param latitude:
        :param longitude:
        :param speed:
        :return:
        """
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.speed = speed

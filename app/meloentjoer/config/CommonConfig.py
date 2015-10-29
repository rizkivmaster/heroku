__author__ = 'traveloka'


class CommonConfig(object):

    def __init__(self, config):
        """
        :type config: dict
        :param config:
        :return:
        """
        self.host_name = config['HOST_URL']

    def get_host_name(self):
        return self.host_name

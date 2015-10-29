__author__ = 'traveloka'


class PostgresConfig(object):
    def __init__(self, config):
        """
        :type config: dict
        :param config:
        :return:
        """
        self.database_url = config['DATABASE_URL']

    def get_database_url(self):
        return self.database_url

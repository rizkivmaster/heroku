import json
import os


class GeneralConfig(object):
    def __init__(self):
        config_path = './meloentjoer/config'
        if 'MELOENTJOER_ENV' not in os.environ:
            env_type = 'TEST'
        else:
            env_type = os.environ['MELOENTJOER_ENV']
        if env_type == 'TEST':
            config_path = '/var/meloentjoer/config/config-{0}.json'.format(env_type)
        config_file = open(config_path, 'r').read()
        config_json = json.loads(config_file)
        self.database_url = config_json['DATABASE_URL']
        self.host_name = config_json['HOST_URL']
        self.mapping_threshold = 0.0025452082429566771

    def get_database_url(self):
        return self.database_url

    def get_host_name(self):
        return self.host_name

    def get_mapping_threshold(self):
        return self.mapping_threshold

    def get_geo_refresh_period(self):
        """
        :rtype int
        :return:
        """
        return 10

    def get_autocomplete_refresh_period(self):
        """
        :rtype int
        :return:
        """
        return 10

    def get_default_eta(self):
        """
        :rtype int
        :return:
        """
        return 60

    def get_default_price(self):
        """
        :rtype int
        :return:
        """
        return 0

    def get_thread_size(self):
        """
        :rtype int
        :return:
        """
        return 32
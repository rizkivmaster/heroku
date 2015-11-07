import json
import os

config_path = './meloentjoer/config'
if 'MELOENTJOER_ENV' not in os.environ:
    env_type = 'TEST'
else:
    env_type = os.environ['MELOENTJOER_ENV']
if env_type == 'TEST':
    config_path = '/var/meloentjoer/config/config-{0}.json'.format(env_type)
config_file = open(config_path, 'r').read()
config_json = json.loads(config_file)


def get_database_url():
    """
    :rtype
    :return:
    """
    database_url = config_json['DATABASE_URL']
    return database_url


def get_host_url():
    host_name = config_json['HOST_URL']
    return host_name


def get_mapping_threshold():
    mapping_threshold = 0.0025452082429566771
    return mapping_threshold


def get_geo_refresh_period():
    """
    :rtype int
    :return:
    """
    return 10


def get_autocomplete_refresh_period():
    """
    :rtype int
    :return:
    """
    return 2


def get_default_eta():
    """
    :rtype int
    :return:
    """
    return 60


def get_default_price():
    """
    :rtype int
    :return:
    """
    return 0


def get_thread_size():
    """
    :rtype int
    :return:
    """
    return 32


def get_eta_refresh_period():
    """
    :rtype int
    :return:
    """
    return 2

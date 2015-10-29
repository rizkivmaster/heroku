from app.meloentjoer.config.CommonConfig import CommonConfig

__author__ = 'traveloka'

from PostgresConfig import PostgresConfig
import os
import json

config_path = './meloentjoer/config'
if 'MELOENTJOER_ENV' not in os.environ:
    env_type = 'TEST'
else:
    env_type = os.environ['MELOENTJOER_ENV']

if env_type == 'TEST':
    config_path = '/var/meloentjoer/config/config-{0}.json'.format(env_type)

config_file = open(config_path, 'r').read()
config_json = json.loads(config_file)

postgres_config = PostgresConfig(config_json)
common_config = CommonConfig(config_json)

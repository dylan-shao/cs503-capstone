import os
import yaml
from pystatsd import Client

STATDS_HOST = None
STATDS_PORT = None

config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
with open(config_file_path, 'r') as config_file:
    # Load YAML config file
    config = yaml.load(config_file)

    STATDS_HOST = config['statsd']['host']
    STATDS_PORT = config['statsd']['port']

metrics_client = Client(STATDS_HOST, STATDS_PORT)

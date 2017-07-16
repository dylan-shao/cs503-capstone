import os
import yaml
from pymongo import MongoClient

MONGODB_HOST = None
MONGODB_PORT = None
DB_NAME = None

config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
with open(config_file_path, 'r') as config_file:
    # Load YAML config file
    config = yaml.load(config_file)

    MONGODB_HOST = config['mongodb']['host']
    MONGODB_PORT = config['mongodb']['port']
    DB_NAME = config['mongodb']['db_name']

client = MongoClient('%s:%s' % (MONGODB_HOST, MONGODB_PORT))

def get_db(db_name=DB_NAME):
    db = client[db_name]
    return db

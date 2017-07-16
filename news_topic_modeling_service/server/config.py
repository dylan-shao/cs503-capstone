import os
import yaml

SERVICE_HOST = None
SERVICE_PORT = None

config_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.yaml')
with open(config_file_path, 'r') as config_file:
    # Load YAML config file
    config = yaml.load(config_file)

    # Extract what we need
    SERVICE_HOST = config['news_topic_modeling_service']['host']
    SERVICE_PORT = config['news_topic_modeling_service']['port']

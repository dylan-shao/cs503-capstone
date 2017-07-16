import os
import yaml
import pyjsonrpc

SERVICE_HOST = None
SERVICE_PORT = None

config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
with open(config_file_path, 'r') as config_file:
    # Load YAML config file
    config = yaml.load(config_file)

    SERVICE_HOST = config['news_topic_modeling_service']['host']
    SERVICE_PORT = config['news_topic_modeling_service']['port']

SERVICE_URL = 'http://{host}:{port}/'.format(host=SERVICE_HOST, port=SERVICE_PORT)

client = pyjsonrpc.HttpClient(url=SERVICE_URL)

def classify(text):
    topic = client.call('classify', text)
    print "Topic: %s" % str(topic)
    return topic

import os
import yaml

SERVICE_HOST = None
SERVICE_PORT = None

REDIS_HOST = None
REDIS_PORT = None

NEWS_TABLE_NAME = None
CLICK_LOGS_TABLE_NAME = None

CLICK_LOGS_TASK_QUEUE_NAME = None
CLICK_LOGS_TASK_QUEUE_URL = None

NEWS_LIMIT = None
NEWS_LIST_BATCH_SIZE = None
USER_NEWS_TIMEOUT_IN_SECONDS = None

NEWS_CLASSES = None

LOG_FILE_PATH = None

config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
with open(config_file_path, 'r') as config_file:
    # Load YAML config file
    config = yaml.load(config_file)

    # Extract what we need
    SERVICE_HOST = config['backend_service']['host']
    SERVICE_PORT = config['backend_service']['port']

    REDIS_HOST = config['redis']['host']
    REDIS_PORT = config['redis']['port']

    NEWS_TABLE_NAME = config['mongodb']['news_table_name']
    CLICK_LOGS_TABLE_NAME = config['mongodb']['click_logs_table_name']

    CLICK_LOGS_TASK_QUEUE_NAME = config['message_queue']['click_logs_task_queue_name']
    CLICK_LOGS_TASK_QUEUE_URL = config['message_queue']['click_logs_task_queue_url']

    NEWS_LIMIT = config['backend_service']['news_limit']
    NEWS_LIST_BATCH_SIZE = config['backend_service']['news_list_batch_size']
    USER_NEWS_TIMEOUT_IN_SECONDS = config['backend_service']['user_news_timeout_in_seconds']

    NEWS_CLASSES = config['news']['classes']

    LOG_FILE_PATH = config['backend_service']['log_file_path']

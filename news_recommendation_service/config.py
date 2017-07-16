import os
import yaml

SERVICE_HOST = None
SERVICE_PORT = None

PREFERENCE_MODEL_TABLE_NAME = None
NEWS_TABLE_NAME = None
NUMBER_OF_CLASSES = None
NEWS_CLASSES = None

CLICK_LOGS_TASK_QUEUE_NAME = None
CLICK_LOGS_TASK_QUEUE_URL = None

CLICK_LOGS_PROCESSOR_CONFIG = {}

config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
with open(config_file_path, 'r') as config_file:
    # Load YAML config file
    config = yaml.load(config_file)

    # Extract what we need
    SERVICE_HOST = config['news_recommendation_service']['host']
    SERVICE_PORT = config['news_recommendation_service']['port']

    PREFERENCE_MODEL_TABLE_NAME = config['mongodb']['preference_model_table_name']
    NEWS_TABLE_NAME = config['mongodb']['news_table_name']
    
    NUMBER_OF_CLASSES = config['news']['number_of_classes']
    NEWS_CLASSES = config['news']['classes']

    CLICK_LOGS_TASK_QUEUE_NAME = config['message_queue']['click_logs_task_queue_name']
    CLICK_LOGS_TASK_QUEUE_URL = config['message_queue']['click_logs_task_queue_url']

    CLICK_LOGS_PROCESSOR_CONFIG['alpha'] = config['news_recommendation_service']['click_logs_processor']['alpha']
    CLICK_LOGS_PROCESSOR_CONFIG['sleep_time_in_seconds'] = config['news_recommendation_service']['click_logs_processor']['sleep_time_in_seconds']
    CLICK_LOGS_PROCESSOR_CONFIG['log_file_path'] = config['news_recommendation_service']['click_logs_processor']['log_file_path']

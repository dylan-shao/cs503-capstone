import os
import yaml

NEWS_SOURCES = None

REDIS_HOST = None
REDIS_PORT = None

NEWS_MONITOR_CONFIG = {}
NEWS_FETCHER_CONFIG = {}
NEWS_DEDUPER_CONFIG = {}

NEWS_TABLE_NAME = None

SCRAPE_NEWS_TASK_QUEUE_NAME = None
SCRAPE_NEWS_TASK_QUEUE_URL = None

DEDUPE_NEWS_TASK_QUEUE_NAME = None
DEDUPE_NEWS_TASK_QUEUE_URL = None

config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
with open(config_file_path, 'r') as config_file:
    # Load YAML config file
    config = yaml.load(config_file)

    # Extract what we need
    REDIS_HOST = config['redis']['host']
    REDIS_PORT = config['redis']['port']

    NEWS_MONITOR_CONFIG['news_sources'] = config['news_pipeline']['news_monitor']['news_sources']
    NEWS_MONITOR_CONFIG['sleep_time_in_seconds'] = config['news_pipeline']['news_monitor']['sleep_time_in_seconds']
    NEWS_MONITOR_CONFIG['news_timeout_in_seconds'] = config['news_pipeline']['news_monitor']['news_timeout_in_seconds']
    NEWS_MONITOR_CONFIG['log_file_path'] = config['news_pipeline']['news_monitor']['log_file_path']

    NEWS_FETCHER_CONFIG['sleep_time_in_seconds'] = config['news_pipeline']['news_fetcher']['sleep_time_in_seconds']
    NEWS_FETCHER_CONFIG['log_file_path'] = config['news_pipeline']['news_fetcher']['log_file_path']

    NEWS_DEDUPER_CONFIG['sleep_time_in_seconds'] = config['news_pipeline']['news_deduper']['sleep_time_in_seconds']
    NEWS_DEDUPER_CONFIG['same_news_similarity_threshold'] = config['news_pipeline']['news_deduper']['same_news_similarity_threshold']
    NEWS_DEDUPER_CONFIG['log_file_path'] = config['news_pipeline']['news_deduper']['log_file_path']

    NEWS_TABLE_NAME = config['mongodb']['news_table_name']

    SCRAPE_NEWS_TASK_QUEUE_NAME = config['message_queue']['scrape_news_task_queue_name']
    SCRAPE_NEWS_TASK_QUEUE_URL = config['message_queue']['scrape_news_task_queue_url']

    DEDUPE_NEWS_TASK_QUEUE_NAME = config['message_queue']['dedupe_news_task_queue_name']
    DEDUPE_NEWS_TASK_QUEUE_URL = config['message_queue']['dedupe_news_task_queue_url']

import sys
import os
import hashlib
import redis
import datetime

# Import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import news_api_client

from cloudamqp_client import CloudAMQPClient
from metrics_client import metrics_client
import logging_service

from config import NEWS_MONITOR_CONFIG
from config import REDIS_HOST, REDIS_PORT
from config import SCRAPE_NEWS_TASK_QUEUE_NAME, SCRAPE_NEWS_TASK_QUEUE_URL

NEWS_SOURCES = NEWS_MONITOR_CONFIG['news_sources']
NEWS_TIME_OUT_IN_SECONDS = NEWS_MONITOR_CONFIG['news_timeout_in_seconds']
SLEEP_TIME_IN_SECONDS = NEWS_MONITOR_CONFIG['sleep_time_in_seconds']

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
logger = logging_service.get_logger(log_file_path=NEWS_MONITOR_CONFIG['log_file_path'])

while True:
    news_list = news_api_client.get_news_from_sources(NEWS_SOURCES)
    num_of_new_news = 0

    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

        if redis_client.get(news_digest) is None:
            num_of_new_news = num_of_new_news + 1
            news['digest'] = news_digest

            # If 'publishedAt' is None, set it to current UTC time
            if news['publishedAt'] is None:
                # Make the time in format YYYY-MM_DDTHH:MM:SS in UTC
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

            redis_client.set(news_digest, news)
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

            cloudAMQP_client.send_message(news)
            metrics_client.increment('coconut_news.news_pipeline.news_monitor')

    logger.info('News monitor Fetched %d news.' % num_of_new_news)
    print 'Fetched %d news.' % num_of_new_news

    cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

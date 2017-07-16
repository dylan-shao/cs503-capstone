import os
import sys
import datetime
from newspaper import Article

# Import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper

from cloudamqp_client import CloudAMQPClient
import logging_service

from config import SCRAPE_NEWS_TASK_QUEUE_NAME, SCRAPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME, DEDUPE_NEWS_TASK_QUEUE_URL
from config import NEWS_FETCHER_CONFIG

SLEEP_TIME_IN_SECONDS = NEWS_FETCHER_CONFIG['sleep_time_in_seconds']

scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
logger = logging_service.get_logger(log_file_path=NEWS_FETCHER_CONFIG['log_file_path'])

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print 'message is broken'
        return

    task = msg
    text = None

    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text
    dedupe_news_queue_client.send_message(task)


while True:
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.get_message()

        if msg is not None:
            # Parse and process the task
            try:
                start_time = datetime.datetime.now()

                handle_message(msg)

                end_time = datetime.datetime.now()
                # Measure the time of the operation in milliseconds
                operation_time_in_milliseconds = int((end_time - start_time).total_seconds() * 1000)
                
                # Send the metrics
                metrics_client.timing('coconut_news.news_pipeline.news_fetcher',
                                      operation_time_in_milliseconds)
                metrics_client.increment('coconut_news.news_pipeline.news_fetcher')
            except Exception as e:
                logger.exception('News fetcher handle_message exception')
                print e
                pass

        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)

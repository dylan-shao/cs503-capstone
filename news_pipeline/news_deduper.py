import os
import sys
import datetime

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

# Import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_topic_modeling_service_client

from cloudamqp_client import CloudAMQPClient
from metrics_client import metrics_client
import logging_service

from config import DEDUPE_NEWS_TASK_QUEUE_NAME, DEDUPE_NEWS_TASK_QUEUE_URL
from config import NEWS_TABLE_NAME
from config import NEWS_DEDUPER_CONFIG

SLEEP_TIME_IN_SECONDS = NEWS_DEDUPER_CONFIG['sleep_time_in_seconds']
SAME_NEWS_SIMILARITY_THRESHOLD = NEWS_DEDUPER_CONFIG['same_news_similarity_threshold']

cloudAMQP_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
logger = logging_service.get_logger(log_file_path=NEWS_DEDUPER_CONFIG['log_file_path'])

def handle_message(msg):
    if msg is None or not isinstance(msg, dict) :
        return
    task = msg
    text = task['text'].encode('utf-8')
    if text is None:
        return

    # Get all recent news based on publishedAt
    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year,
                                               published_at.month,
                                               published_at.day,
                                               0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    db = mongodb_client.get_db()
    same_day_news_list = list(db[NEWS_TABLE_NAME].find(
        {
            'publishedAt': {
                '$gte': published_at_day_begin,
                '$lt': published_at_day_end
            }
        }
    ))

    if same_day_news_list is not None and len(same_day_news_list) > 0:
        documents = [news['text'].encode('utf-8') for news in same_day_news_list]
        documents.insert(0, text)

        # Calculate similarity matrix
        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T
        rows, _ = pairwise_sim.shape
        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                print "Duplicated news. Ignore"
                return

    task['publishedAt'] = parser.parse(task['publishedAt'])

    # Classify news
    title = task['title']
    if title is not None:
        topic = news_topic_modeling_service_client.classify(title)
        task['class'] = topic
    
    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)

while True:
    if cloudAMQP_client is not None:
        msg = cloudAMQP_client.get_message()
        if msg is not None:
            # Parse and process the task
            try:
                start_time = datetime.datetime.now()

                handle_message(msg)

                end_time = datetime.datetime.now()
                # Measure the time of the operation in milliseconds
                operation_time_in_milliseconds = int((end_time - start_time).total_seconds() * 1000)
                
                # Send the metrics
                metrics_client.timing('coconut_news.news_pipeline.news_deduper',
                                      operation_time_in_milliseconds)
                metrics_client.increment('coconut_news.news_pipeline.news_deduper')
            except Exception as e:
                logger.exception('News deduper handle_message exception')
                print e
                pass

        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
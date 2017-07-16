import json
import os
import pickle
import random
import redis
import sys

from bson.json_util import dumps
from datetime import datetime

# Import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_recommendation_service_client
from cloudamqp_client import CloudAMQPClient
from metrics_client import metrics_client
from config import REDIS_HOST, REDIS_PORT, NEWS_TABLE_NAME, CLICK_LOGS_TASK_QUEUE_NAME, CLICK_LOGS_TASK_QUEUE_URL
from config import NEWS_LIMIT, NEWS_LIST_BATCH_SIZE, USER_NEWS_TIMEOUT_IN_SECONDS, NEWS_CLASSES, CLICK_LOGS_TABLE_NAME

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)
cloudAMQP_client = CloudAMQPClient(CLICK_LOGS_TASK_QUEUE_URL, CLICK_LOGS_TASK_QUEUE_NAME)


def get_news_summaries_for_user(user_id, page_num):
    page_num = int(page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    start_time = datetime.now()

    # The final list of news to be returned.
    sliced_news = []

    if redis_client.get(user_id) is not None:
        news_digests = pickle.loads(redis_client.get(user_id))

        # If begin_index is out of range, this will return empty list.
        # If end_index is out of range (begin_index is within the range), this
        # will return all remaining news ids.
        sliced_news_digests = news_digests[begin_index:end_index]
        print sliced_news_digests
        db = mongodb_client.get_db()
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digests}}))
    else:
        db = mongodb_client.get_db()
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        total_news_digests = map(lambda x:x['digest'], total_news)

        redis_client.set(user_id, pickle.dumps(total_news_digests))
        redis_client.expire(user_id, USER_NEWS_TIMEOUT_IN_SECONDS)

        sliced_news = total_news[begin_index:end_index]

    # Get preference for the user
    preference = news_recommendation_service_client.getPreferenceForUser(user_id)

    result_news = []
    if preference is not None and len(preference) > 0:
        topPreference = preference[0]

        # Init the preference to news dict.
        preference_news_dict = {}
        for news_class in NEWS_CLASSES:
            preference_news_dict[news_class] = []

        remaining_news = []
        for news in sliced_news:
            if 'class' not in news:
                remaining_news.append(news)
                continue

            news_class = news['class']
            news_list = preference_news_dict[news_class]
            news_list.append(news)
        
        
        for p in preference:
            news_list = preference_news_dict[p]
            result_news.extend(news_list)
        if len(remaining_news) > 0:
            result_news.extend(remaining_news)
    else:
        result_news = sliced_news

    end_time = datetime.now()
    # Measure the time of the operation in milliseconds
    operation_time_in_milliseconds = int((end_time - start_time).total_seconds() * 1000)

    # Send the metrics
    metrics_client.timing('coconut_news.backend_service.get_news_summaries_for_user',
                          operation_time_in_milliseconds)
    metrics_client.increment('coconut_news.backend_service.get_news_summaries_for_user')

    return json.loads(dumps(result_news))

def log_news_click_for_user(user_id, news_id):
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': datetime.utcnow()}

    start_time = datetime.now()

    db = mongodb_client.get_db()
    db[CLICK_LOGS_TABLE_NAME].insert(message)

    # Send log task to machine learning service for prediction
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': str(datetime.utcnow())}
    cloudAMQP_client.send_message(message)

    end_time = datetime.now()
    # Measure the time of the operation in milliseconds
    operation_time_in_milliseconds = int((end_time - start_time).total_seconds() * 1000)

    # Send the metrics
    metrics_client.increment('coconut_news.backend_service.log_news_click_for_user')
    metrics_client.timing('coconut_news.backend_service.log_news_click_for_user',
                          operation_time_in_milliseconds)
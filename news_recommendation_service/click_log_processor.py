# -*- coding: utf-8 -*-

'''
Time decay model:

If selected:
p = (1-α)p + α

If not:
p = (1-α)p

Where p is the selection probability, and α is the degree of weight decrease.
The result of this is that the nth most recent selection will have a weight of
(1-α)^n. Using a coefficient value of 0.05 as an example, the 10th most recent
selection would only have half the weight of the most recent. Increasing epsilon
would bias towards more recent results more.
'''

import os
import sys

# Import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudamqp_client import CloudAMQPClient
from metrics_client import metrics_client
import logging_service
from config import PREFERENCE_MODEL_TABLE_NAME, NEWS_TABLE_NAME
from config import NUMBER_OF_CLASSES, NEWS_CLASSES
from config import CLICK_LOGS_TASK_QUEUE_NAME, CLICK_LOGS_TASK_QUEUE_URL
from config import CLICK_LOGS_PROCESSOR_CONFIG

INITIAL_P = 1.0 / NUMBER_OF_CLASSES
ALPHA = CLICK_LOGS_PROCESSOR_CONFIG['alpha']
SLEEP_TIME_IN_SECONDS = CLICK_LOGS_PROCESSOR_CONFIG['sleep_time_in_seconds']

cloudAMQP_client = CloudAMQPClient(CLICK_LOGS_TASK_QUEUE_URL, CLICK_LOGS_TASK_QUEUE_NAME)
logger = logging_service.get_logger(log_file_path=CLICK_LOGS_PROCESSOR_CONFIG['log_file_path'])

def handle_message(msg):
    if msg is None or not isinstance(msg, dict) :
        return

    if ('userId' not in msg
        or 'newsId' not in msg
        or 'timestamp' not in msg):
        return

    userId = msg['userId']
    newsId = msg['newsId']

    # Update user's preference
    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': userId})

    # If model not exists, create a new one
    if model is None:
        print 'Creating preference model for new user: %s' % userId
        new_model = {'userId' : userId}
        preference = {}
        for i in NEWS_CLASSES:
            preference[i] = float(INITIAL_P)
        new_model['preference'] = preference
        model = new_model

    print 'Updating preference model for new user: %s' % userId

    # Update model using time decaying method
    news = db[NEWS_TABLE_NAME].find_one({'digest': newsId})
    if (news is None
        or 'class' not in news
        or news['class'] not in NEWS_CLASSES):
        # print news is None
        # print 'class' not in news
        # print news['class'] not in NEWS_CLASSES
        print 'Skipping processing...'
        return

    click_class = news['class']

    # Update the clicked one.
    old_p = model['preference'][click_class]
    model['preference'][click_class] = float((1 - ALPHA) * old_p + ALPHA)

    # Update not clicked classes.
    for i, prob in model['preference'].iteritems():
        if not i == click_class:
            model['preference'][i] = float((1 - ALPHA) * model['preference'][i])

    db[PREFERENCE_MODEL_TABLE_NAME].replace_one({ 'userId': userId }, model, upsert=True)

def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.get_message()
            if msg is not None:
                # Parse and process the task
                try:
                    handle_message(msg)

                    metrics_client.increment('coconut_news.news_recommendation_service.click_log_processor')
                except Exception as e:
                    logger.exception('click_log_processor handle_message exception')
                    print e
                    pass
            # Remove this if this becomes a bottleneck.
            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ ==  '__main__':
    run()

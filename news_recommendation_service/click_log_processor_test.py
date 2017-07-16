import os
import sys
from datetime import datetime
from sets import Set
import click_log_processor

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

from config import PREFERENCE_MODEL_TABLE_NAME, NEWS_TABLE_NAME
from config import NUMBER_OF_CLASSES

# Make sure the MongoDB is up before running following tests.
def test_basic():
    db = mongodb_client.get_db()
    db[PREFERENCE_MODEL_TABLE_NAME].delete_many({ 'userId': 'test_user' })

    test_news_id = 'test_news'
    test_news = {
        'digest': test_news_id,
        'class': 'Technology'
    }
    db[NEWS_TABLE_NAME].replace_one({ 'digest': test_news_id }, test_news, upsert=True)

    msg = {
        'userId': 'test_user',
        'newsId': test_news_id,
        'timestamp': str(datetime.utcnow())
    }

    click_log_processor.handle_message(msg)

    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({ 'userId':'test_user' })
    assert model is not None
    assert len(model['preference']) == NUMBER_OF_CLASSES

    print 'test_basic passed!'

    db[NEWS_TABLE_NAME].delete_many({ 'digest': test_news_id })

if __name__ == '__main__':
    test_basic()

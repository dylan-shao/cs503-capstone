from metrics_client import metrics_client

def test_basic():
    metrics_client.increment('coconut_news.python.metrics_client_test')

if __name__ == '__main__':
    test_basic()

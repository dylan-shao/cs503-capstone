import mongodb_client as client

def test_basic():
    db = client.get_db()
    print db.news.count()

if __name__ == '__main__':
    test_basic()

import os
import random
import requests
from lxml import html

GET_CNN_NEWS_XPATH = "//p[@class='zn-body__paragraph speakable']//text() | //div[@class='zn-body__paragraph speakable']//text() | //div[@class='zn-body__paragraph']//text()"

USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []

with open(USER_AGENTS_FILE, 'rb') as user_agents_file:
    for user_agent in user_agents_file.readlines():
        if user_agent:
            USER_AGENTS.append(user_agent.strip()[1:-1])

def get_headers():
    user_agent = random.choice(USER_AGENTS)  # Select a random user agent
    headers = {
        'Connection' : 'close',
        'User-Agent' : user_agent
    }

def extract_news(news_url):
    session_requests = requests.session()
    response = session_requests.get(news_url, headers=get_headers())

    news = {}

    try:
        tree = html.fromstring(response.content)
        news = tree.xpath(GET_CNN_NEWS_XPATH)
        news = ''.join(news)
    except Exception:
        return {}

    return news

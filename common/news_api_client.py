import os
import yaml
import requests
from json import loads

NEWS_API_KEY = None
NEWS_API_ENDPOINT = None
ARTICALS_API = None
SORT_BY_TOP = None

config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
with open(config_file_path, 'r') as config_file:
    # Load YAML config file
    config = yaml.load(config_file)

    NEWS_API_KEY = config['news_api']['key']
    NEWS_API_ENDPOINT = config['news_api']['endpoint']
    ARTICALS_API = config['news_api']['articals_api_name']
    SORT_BY_TOP = config['news_api']['sort_by_top']

BCC = 'bbc'
CNN = 'cnn'
DEFAULT_SOURCES = [CNN]

def build_url(end_point=NEWS_API_ENDPOINT, api_name=ARTICALS_API):
    return end_point + api_name

def get_news_from_sources(sources=[DEFAULT_SOURCES], sort_by=SORT_BY_TOP):
    articles = []
    for source in sources:
        payload = {
            'apiKey': NEWS_API_KEY,
            'source': source,
            'sortBy': sort_by
        }
        response = requests.get(build_url(), params=payload)
        res_json = loads(response.content)

        # Extract news from response
        if (res_json is not None and
            res_json['status'] == 'ok' and
            res_json['source'] is not None):
            # Populate news source in each article
            for news in res_json['articles']:
                news['source'] = res_json['source']

            articles.extend(res_json['articles'])

    return articles

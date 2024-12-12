import json
import os

from src.where2charge.recommender import Recommender
from src import util


def is_json(data):
    try:
        json.loads(data)
        return True
    except ValueError:
        return False


def test_recommendation_json(config_address='src/config.yaml'):
    os.system('pwd')
    start_location = {'lat': 47.6072982, 'lng': -122.33711}
    GPT_API_KEY = util.read_config(config_address)['OpenAI_API_KEY']
    GOOGLE_API_KEY = util.read_config(config_address)['GOOGLE_API_KEY']
    recommender = Recommender(GOOGLE_API_KEY, GPT_API_KEY)
    suggestions = recommender.get_suggestions(start_location['lat'], start_location['lng'], 2)
    assert is_json(suggestions)



import json
import requests
import logging
from cipher.core.actions import SpeechAction


def main(**kwargs):
    if 'slots' not in kwargs or len(kwargs['slots']) < 1:
        return False
    response = requests.get('https://fr.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext=1&titles=' + kwargs['slots'][0]['rawValue'] + '&exintro&exlimit=1&exsentences=1')
    content = json.loads(response.content.decode('utf-8'))
    extract = ''
    try:
        pages = content['query']['pages']
        for page in pages.values():
            extract = page['extract']
    except Exception:
        logging.error("not found")
    SpeechAction(extract).execute()
    return True

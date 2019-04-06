import json
import requests
from cipher.core.action_manager import speech

def main(**kwargs):
    if 'flags' not in kwargs or len(kwargs['flags']) < 1:
        return

    response = requests.get("https://fr.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext=1&titles="+kwargs['flags'][0]+"&exintro&exlimit=1&exsentences=1")
    content=json.loads(response.content)
    extract=""
    try:
        pages=content['query']['pages']
        for page in pages.values():
            extract=page['extract']
    except Exception:
        print("not found")
    speech(extract)
    return kwargs
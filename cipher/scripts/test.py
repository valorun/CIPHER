import json
import requests
from cipher.core.action_manager import speech

def main(**kwargs):
    if 'flags' not in kwargs or len(kwargs['flags']) < 1:
        return

    speech(kwargs['flags'][0])
    return kwargs
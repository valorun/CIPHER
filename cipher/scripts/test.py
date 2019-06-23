import json
import requests
from cipher.core.actions import speech

def main(**kwargs):
    if 'flags' not in kwargs or len(kwargs['flags']) < 1:
        return
    if 'slots' not in kwargs or len(kwargs['slots']) < 1:
        return

    speech(kwargs['flags'][0])
    speech(kwargs['slots'][0])
    return kwargs
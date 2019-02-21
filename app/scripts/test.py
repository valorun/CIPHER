import json
import requests
from app.core.action_manager import speech

def main(**kwargs):
    if('flags' not in kwargs or kwargs['flags'].length < 1):
        return

    speech(kwargs['flags'][0])
    return kwargs
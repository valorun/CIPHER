import datetime
from cipher.core.actions import SpeechAction


def main(**kwargs):
    now = datetime.datetime.now()
    SpeechAction("Il est " + str(now.hour) + " heure " + str(now.minute)).execute(**kargs)
    return True

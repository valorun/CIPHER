import datetime
from cipher.core.actions import speech

def main(**kwargs):
    now = datetime.datetime.now()
    speech("Il est " + str(now.hour) + " heure " + str(now.minute))
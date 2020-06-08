import datetime
from cipher.core.actions import SpeechAction, CUSTOM_ACTIONS

class GetTimeAction(SpeechAction):
    display_name = 'Heure'

    @staticmethod
    def get_parameters():
        return []

    @staticmethod
    def check_parameters():
        return True, None
        
    @staticmethod
    def execute():
        now = datetime.datetime.now()
        SpeechAction.execute("Il est " + str(now.hour) + " heure " + str(now.minute))

CUSTOM_ACTIONS['time'] = GetTimeAction
from cipher.core.actions import SpeechAction, CUSTOM_ACTIONS
from cipher.model import config

class GetNameAction(SpeechAction):
    display_name = 'Nom du robot'

    @staticmethod
    def get_parameters():
        return []

    @staticmethod
    def check_parameters():
        return True, None

    @staticmethod
    def execute():
        SpeechAction.execute("Je m'appelle " + config.get_robot_name())

CUSTOM_ACTIONS['name'] = GetNameAction
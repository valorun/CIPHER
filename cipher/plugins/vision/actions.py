from cipher.core.actions import SpeechAction, CUSTOM_ACTIONS
from cipher import mqtt


class DetectObjectsAction(SpeechAction):
    display_name = 'Détecter les objets'

    @staticmethod
    def get_parameters():
        return []

    @staticmethod
    def check_parameters():
        return True, None

    @staticmethod
    def execute():
        mqtt.publish('client/vision/detect_objects')

CUSTOM_ACTIONS['camera_detect'] = DetectObjectsAction
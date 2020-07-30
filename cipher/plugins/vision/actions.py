from cipher.core.actions import SpeechAction, CUSTOM_ACTIONS
from cipher.core.camera import camera
from .object_detection import list_objects


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
        camera_is_opened = camera.is_opened()
        if not camera_is_opened:
            camera.open()
        result = list_objects(camera.get_frame())
        result = ','.join(result)
        SpeechAction.execute(result)
        if not camera_is_opened:
            camera.release()

CUSTOM_ACTIONS['camera_detect'] = DetectObjectsAction
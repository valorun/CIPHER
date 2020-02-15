from cipher.core.actions import SpeechAction
from cipher.model import config


def main(**kwargs):
    SpeechAction("Je m'appelle " + config.get_robot_name()).execute()

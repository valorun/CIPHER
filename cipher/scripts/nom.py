from cipher.core.actions import speech
from cipher.model import config

def main(**kwargs):
    speech("Je m'appelle " + config.getRobotName())
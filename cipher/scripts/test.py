from cipher.core.actions import SpeechAction


def main(**kwargs):
    if 'intenName' not in kwargs:
        return

    SpeechAction(kwargs['slots'][0]).execute()

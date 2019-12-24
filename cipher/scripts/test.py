from cipher.core.actions import SpeechAction


def main(**kwargs):
    if 'slots' not in kwargs or len(kwargs['slots']) < 1:
        return

    SpeechAction(kwargs['slots'][0]).execute()

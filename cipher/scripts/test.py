from cipher.core.actions import speech

def main(**kwargs):
    if 'slots' not in kwargs or len(kwargs['slots']) < 1:
        return

    speech(kwargs['slots'][0])
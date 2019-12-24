from cipher.core.actions import ServoAction


def main(**kwargs):
    ServoAction('test', 1200, 25).execute()

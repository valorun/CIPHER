from cipher.core.actions import CUSTOM_ACTIONS

from cipher.plugins.hearing.intent_action import IntentAction, IntentSequenceParameter, INTENT_ACTIONS

class GetNameIntentAction(IntentAction):
    display_name = 'Nom du robot'

    @staticmethod
    def get_parameters():
        return [IntentSequenceParameter('wave', 'Séquence de salutation', 'Exemple: wave_seq')]

    @staticmethod
    def check_parameters(wave_seq: str):
        if not get_parameters()[0].value_is_valid(wave_seq):
            return False, "This sequence does not exists."
        return True, None


    @staticmethod
    def execute(wave_seq: str):
        valid, message = GetNameIntentAction.check_parameters(wave_seq)
        if not valid:
            core.log.warning(message)
            return
        CUSTOM_ACTIONS.get('name').execute()

INTENT_ACTIONS['name'] = GetNameActGetNameIntentActionion
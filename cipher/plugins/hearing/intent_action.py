from typing import List, Tuple

from cipher.core.action_parameters import ActionParameter
from cipher.core.actions import Action

class IntentSequenceParameter(ActionParameter):
    type = 'Sequence'
    def __init__(self, name, display_name, hint = None):
        ActionParameter.__init__(self, name, display_name, hint)

    def value_is_valid(self, value):
        if isinstance(value, str):
            seq = DbSequence.query.filter_by(id=value, enabled=True).first()
            if seq is not None:
                return True
        return False

    def get_type(self):
        return IntentSequenceParameter.type

# class IntentActionParameter(ActionParameter):
#     type = 'Action'
#     def __init__(self, name, display_name, hint = None):
#         ActionParameter.__init__(self, name, display_name, hint)

#     def value_is_valid(self, value):
#         return value in DEFAULT_ACTIONS or value in CUSTOM_ACTIONS

#     def get_type(self):
#         return IntentActionParameter.type



class IntentAction(Action):
    """
    Action trigerred when an intent is detected.
    """
    display_name = ''

    @staticmethod
    def execute():
        """
        Execute the action with some parameters.
        """
        pass

    @staticmethod
    def check_parameters() -> Tuple[bool, str]:
        """
        Check the given parameters to ensure they are suitable for the method execute.
        Return False and a message if the parameters are incorrect, True otherwise.
        """
        return True, None

    @staticmethod
    def get_parameters() -> List[ActionParameter]:
        """
        Get all the parameters needed in order to execute the action.
        This method is used to dynamically display the different form to set up the execution.
        """
        return []

INTENT_ACTIONS = {}
import logging
import json
from cipher.core.actions import *
from cipher.core.sequence import Sequence, Node, Transition
from cipher.model import db, Sequence as DbSequence


# vérif que le parcours partant du noeud de départ soit bien sans orphelins, et qu'il n'y ait pas de boucles
class SequenceReader:
    """
    Classe reading sequences.
    """
    def __init__(self):
        self.current_sequence = None

    def get_sequence_from_json(self, json_list: list):
        """
        Create a sequence object from JSON.
        """
        if json_list is None:
            return []

        return Sequence([self._get_transition_from_json(t) for t in json_list])

    def _get_action_from_json(self, data: dict):
        """
        Create a action node object from JSON.
        """
        if 'name' not in data:
            logging.info(str(data))
            raise ValueError('Invalid JSON Action format')
        action_name = data['name']
        action_parameters = data['parameters']
        action = Action.get_from_name(action_name)
        
        return Node(action, action_parameters, [self._get_transition_from_json(t) for t in data['transitions']])

    def _get_transition_from_json(self, data: dict):
        """
        Create a transition object from JSON.
        """
        if 'target' not in data or 'time' not in data:
            raise ValueError('Invalid JSON Action format')
        transition_target = self._get_action_from_json(data['target'])
        transition_time = data['time']
        return Transition(transition_target, transition_time)

    def read_sequence(self, data: list, **kwargs):
        """
        Launch the sequence execution from a JSON object.
        """
        # wait for the current sequence to be completed to launch a new one
        if self.current_sequence is not None and self.current_sequence.is_in_execution():
            logging.warning("Cannot execute sequence, another one is already running.")
            return

        seq = self.get_sequence_from_json(data)
        self.current_sequence = seq
        seq.execute(**kwargs)

    def launch_sequence(self, name: str, **kwargs):
        """
        Searches for the sequence in the database from its name, and then launches it.
        """
        if name is None or name == '':
            return
        seq = DbSequence.query.filter_by(id=name, enabled=True).first()
        if seq is not None:
            seq_data = seq.value
            logging.info("Executing sequence " + name)
            self.read_sequence(json.loads(seq_data), **kwargs)
            return True
        else:
            return False


sequence_reader = SequenceReader()

import json
import re
from cipher.core.actions import *
from cipher.core.sequence import Sequence, Node, Transition
from cipher.model import db, Sequence as DbSequence
from . import core


# vérif que le parcours partant du noeud de départ soit bien sans orphelins, et qu'il n'y ait pas de boucles
class SequenceReader:
    """
    Classe reading sequences.
    """
    def __init__(self):
        self.current_sequence = None

    def get_sequence_from_json(self, json_list: list, **kwargs):
        """
        Create a sequence object from JSON.
        """
        if json_list is None:
            return []

        return Sequence([self._get_transition_from_json(t, **kwargs) for t in json_list])

    def _parse_slot_parameters(self, parameters: dict, slots: dict):
        """
        Parse parameters related to slots.
        If a pattern corresponding to '${slot_name:fallback}' appears, value is replaced. 
        """
        for p in parameters.keys():
            if not isinstance(parameters[p], str):
                continue
            raw_potential_slots = re.findall('\${([^}]+)}', parameters[p])

            for s in raw_potential_slots:
                # Split the parameter string after ':'. 
                # First part correspond to slot name, second one to fallback value.
                potential_slot = s.split(':', 1)
                # Replace matched slots by their values.
                if potential_slot[0] in slots:
                    value = slots[potential_slot[0]]['value']
                    while type(value) is dict:
                        value = value['value']
                    parameters[p] = parameters[p].replace('${' + s + '}', value)
                # Unmatched slots use their default value.
                else:
                    fallback = potential_slot[1] if len(potential_slot) > 1 else ''
                    parameters[p] = parameters[p].replace('${' + s + '}', fallback)
        return parameters

    def _get_action_from_json(self, data: dict, **kwargs):
        """
        Create a action node object from JSON.
        """
        if 'name' not in data:
            core.log.info(str(data))
            raise ValueError('Invalid JSON Action format')
        action_name = data['name']
        if 'slots' in kwargs:
            kwargs['slots'] = {s['slotName']:s for s in kwargs['slots']}
        else:
            kwargs['slots'] = {}
        action_parameters = self._parse_slot_parameters(data['parameters'], kwargs['slots'])
        action = Action.get_from_name(action_name)
        return Node(action, action_parameters, [self._get_transition_from_json(t, **kwargs) for t in data['transitions']])

    def _get_transition_from_json(self, data: dict, **kwargs):
        """
        Create a transition object from JSON.
        """
        if 'target' not in data or 'time' not in data:
            raise ValueError('Invalid JSON Action format')
        transition_target = self._get_action_from_json(data['target'], **kwargs)
        transition_time = data['time']
        return Transition(transition_target, transition_time)

    def read_sequence(self, data: list, **kwargs):
        """
        Launch the sequence execution from a JSON object.
        """
        # wait for the current sequence to be completed to launch a new one
        if self.current_sequence is not None and self.current_sequence.is_in_execution():
            core.log.warning("Cannot execute sequence, another one is already running.")
            return

        seq = self.get_sequence_from_json(data, **kwargs)
        self.current_sequence = seq
        seq.execute()

    def launch_sequence(self, name: str, **kwargs):
        """
        Searches for the sequence in the database from its name, and then launches it.
        """
        if name is None or name == '':
            return
        seq = DbSequence.query.filter_by(id=name, enabled=True).first()
        if seq is not None:
            seq_data = seq.value
            core.log.info("Executing sequence %s", name)
            self.read_sequence(json.loads(seq_data), **kwargs)
            return True
        else:
            return False

class DictObj:
    def __init__(self, in_dict:dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
                setattr(self, key, [DictObj(x) if isinstance(x, dict) else x for x in val])
            else:
                setattr(self, key, DictObj(val) if isinstance(val, dict) else val)
                
sequence_reader = SequenceReader()

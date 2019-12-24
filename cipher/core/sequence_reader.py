import logging
import json
from cipher.core.actions import *
from cipher.core.sequence import Sequence, Node, PauseAction
from cipher.model import db, Sequence as DbSequence


# vérif que le parcours partant du noeud de départ soit bien sans orphelins
class SequenceReader:
    """
    Classe reading sequences.
    """
    def __init__(self):
        self.currentSequence = None

    def getSequenceFromJson(self, jsonList: list):
        """
        Create a sequence object from JSON.
        """
        if jsonList is None:
            return []

        return Sequence([self._getActionFromJson(n) for n in jsonList])

    def _getActionFromJson(self, json: dict):
        """
        Create a action node object from JSON.
        """
        actionType = json['type']
        if actionType == 'pause':
            action = PauseAction(json['time'])
        elif actionType == 'speech':
            action = SpeechAction(json['speech'])
        elif actionType == 'relay':
            action = RelayAction(json['relay'], json['state'])
        elif actionType == 'script':
            action = ScriptAction(json['script'])
        elif actionType == 'sound':
            action = SoundAction(json['sound'])
        elif actionType == 'motion':
            action = MotionAction(json['direction'], json['speed'])
        elif actionType == 'servo':
            action = ServoAction(json['servo'], json['position'], json['speed'])
        elif actionType == 'servoSequence':  # COMPATIBILITY REASON
            action = ServoSequenceAction(json['sequence'])
        # elif actionType == 'condition':
            # if 'flags' not in kwargs or json['flag'] not in kwargs['flags']:
                # if there is no flag, or the specified flag is missing, stop the execution
                # return False
        return Node(action, [self._getActionFromJson(c) for c in json['children']])

    def readSequence(self, json: list, **kwargs):
        """
        Launch the sequence execution from a JSON object.
        """
        # wait for the current sequence to be completed to launch a new one
        if self.currentSequence is not None and self.currentSequence.inExecution():
            logging.warning("Cannot execute sequence, another one is already running.")
            return

        seq = self.getSequenceFromJson(json)
        self.currentSequence = seq
        seq.execute(**kwargs)

    def launchSequence(self, name: str, **kwargs):
        """
        Searches for the sequence in the database from its name, and then launches it.
        """
        if name is None or name == '':
            return
        seq = DbSequence.query.filter_by(id=name).first()
        if seq is not None and seq.enabled:
            seq_data = seq.value
            logging.info("Executing sequence " + name)
            self.readSequence(json.loads(seq_data), **kwargs)


sequence_reader = SequenceReader()

import logging
import json
from cipher.core.sequence import Sequence
from cipher.model import db
from cipher.model import Sequence as DbSequence

class SequenceReader:
	"""
	Classe reading sequences.
	"""
	def __init__(self):
		self.currentSequence = None

	def getSequenceFromJson(self, json):
		"""
		Create a sequence object from JSON.
		"""
		nodes = json[0]
		edges = json[1]
		return Sequence(nodes, edges)

	def readSequence(self, json, **kwargs):
		"""
		Launch the sequence execution from a JSON object.
		"""
		#wait for the current sequence to be completed to launch a new one
		if self.currentSequence is not None and not self.currentSequence.inExecution():
			return
		
		seq = self.getSequenceFromJson(json)
		self.currentSequence = seq
		seq.execute('start', **kwargs)

	def launchSequence(self, name, **kwargs):
		"""
		Searches for the sequence in the database from its name, and then launches it.
		"""
		if name is None or name == '':
			return
		seq = DbSequence.query.filter_by(id=name).first()
		if seq is not None and seq.enabled:
			seq_data = seq.value
			logging.info('Executing sequence ' + name)
			self.readSequence(json.loads(seq_data), **kwargs)

sequence_reader = SequenceReader()

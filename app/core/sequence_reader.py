import logging
import json
from flask_socketio import SocketIO
from app import socketio
from app.model import db, Sequence
from .action_manager import speech, relay, motion, servo, sound, script

class SequenceReader:
	"""
	Classe reading sequences and executing actions.
	"""
	def __init__(self):
		#number of actions in progress, to wait before executing another sequence.
		self.threads = 0

	def _executeSequence(self, startNode, nodes, edges, **kwargs):
		"""
		Launch the sequence execution, place each new branch in another thread.
		"""
		self.threads+=1
		result = self.executeAction(self._getNodeActionData(startNode, nodes), **kwargs)
		if result == False:
			# if conditions aren't achieved, or the code is incorrect
			return
		for c in self._getChildren(startNode, edges):
			socketio.start_background_task(self._executeSequence, c, nodes, edges, **kwargs)
		self.threads-=1

	def executeAction(self, actionData, **kwargs):
		"""
		Execute an action based on an action data, for exemple 'sleep:100ms'.
		"""
		if(actionData == None):
			return True
		
		action=actionData["type"]

		if(action == "pause"):
			#if it's a pause, the executed script is paused
			socketio.sleep( int(actionData["time"])/1000 )
		elif(action == "speech"):
			speech(actionData["speech"])
		elif(action == "relay"):
			relay(actionData["relay"], actionData["relay"])
		elif(action == "script"):
			script(actionData["script"], **kwargs)
		elif(action=="sound"):
			sound(actionData["sound"])
		elif(action=="motion"):
			motion(actionData["left"], actionData["right"])
		elif(action=="servo"):
			servo(actionData["sequence"])
		#elif(action=="if"):
		#	val1 = option.split("=")[0]
		#	val2 = option.split("==")[0]
		#	val
		return True

	def _getChildren(self, id, edges):
		"""
		Return the list of the child nodes.
		"""
		children=[]
		for e in edges:
			if(e["from"]==id):
				children.append(e["to"])
		return children

	def _getNodeActionData(self, id, nodes):
		"""
		Return the action of the node with the given id.
		"""
		for n in nodes:
			if(n["id"]==id):
				if("action" in n):
					return n["action"]
		return None

	def readSequence(self, json, **kwargs):
		"""
		Launch the sequence execution from a JSON object.
		"""
		if(self.threads>0): #wait for the current sequence to be completed to launch a new one
			return
		nodes=json[0]
		edges=json[1]
		self._executeSequence("start", nodes, edges, **kwargs)

	def launchSequence(self, name, **kwargs):
		"""
		Searches for the sequence in the database from its name, and then launches it.
		"""
		if(name == None or name == ""):
			return
		seq = Sequence.query.filter_by(id=name).first()
		if(seq!=None and seq.enabled):
			seq_data = seq.value
			logging.info('Executing sequence '+name)
			self.readSequence(json.loads(seq_data), **kwargs)
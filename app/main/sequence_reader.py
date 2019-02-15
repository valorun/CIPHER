#!/usr/bin/python
# coding: utf-8

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

	def _executeSequence(self, startNode, nodes, edges, args=None):
		"""
		Launch the sequence execution, place each new branch in another thread.
		"""
		self.threads+=1
		self.executeAction(self._getNodeLabel(startNode, nodes), args)
		for c in self._getChildren(startNode, edges):
			socketio.start_background_task(self._executeSequence, c, nodes, edges, args)
		self.threads-=1

	def executeAction(self, label, args=None):
		"""
		Execute an action based on a label, for exemple 'sleep:100ms'.
		"""
		if(len(label.split(":", 1))<2):
			return
		action=label.split(":", 1)[0]
		option=label.split(":", 1)[1]

		if(action=="pause"):
			#if it's a pause, the executed script is paused
			socketio.sleep( int(option.split("ms")[0])/1000 )
		elif(action=="speech"):
			#if it'a a speech, return it directly to the client
			speech_str=option.split('"')[0]
			speech(speech_str)
		elif(action=="relay"):
			#if it's a relay, first look for the associated pin, restore the request
			rel_label = option.rsplit(',',1)[0]
			rel_state=""
			#if the state is specified (0 or 1)
			if(len(option.rsplit(',',1))>1):
				rel_state=option.rsplit(',',1)[1]
			relay(rel_label, rel_state)
		elif(action=="script"):
			#if it's a script, import the requested script and execute its start method
			script(option, args)
		elif(action=="sound"):
			#if it's a sound, execute the requested sound
			sound(option)
		elif(action=="motion"):
			#if it is a motion command, activate the motors with the specified speed
			m1Speed = option.split(",")[0]
			m2Speed = option.split(",")[1]
			motion(m1Speed, m2Speed)
		elif(action=="servo"):
			#if it is a servo sequence, launch the one with the specified index
			servo(option)
		logging.info("Sending "+action+" to rasperries.")
		logging.info(label)

	def _getChildren(self, id, edges):
		"""
		Return the list of the child nodes.
		"""
		children=[]
		for e in edges:
			if(e["from"]==id):
				children.append(e["to"])
		return children

	def _getNodeLabel(self, id, nodes):
		"""
		Return the label of the node with the given id.
		"""
		for n in nodes:
			if(n["id"]==id):
				return n["label"]

	def readSequence(self, json, args=None):
		"""
		Launch the sequence execution from a JSON object.
		"""
		if(self.threads>0): #wait for the current sequence to be completed to launch a new one
			return
		nodes=json[0]
		edges=json[1]
		self._executeSequence("start", nodes, edges, args)

	def launchSequence(self, name, args=None):
		"""
		Searches for the sequence in the database from its name, and then launches it.
		"""
		if(name == None or name == ""):
			return
		seq = Sequence.query.filter_by(id=name).first()
		if(seq!=None and seq.enabled):
			seq_data = seq.value
			logging.info('Executing sequence '+name)
			self.readSequence(json.loads(seq_data))
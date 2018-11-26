#!/usr/bin/python
# coding: utf-8

import logging
import time
import json
import importlib.util
import os
from os.path import join
from flask import current_app
from flask_socketio import SocketIO, emit
from .. import socketio
from app.constants import SCRIPTS_LOCATION, SOUNDS_LOCATION
from app.model import db, Relay, Sequence, chatbot, config
from app.chatbot.entity_adapter import ENTITY_PATTERN

class SequenceReader:
	"""
	Classe reading sequences and executing actions.
	"""
	def __init__(self):
		#number of actions in progress, to wait before executing another sequence.
		self.threads = 0

	def _executeSequence(self, app, startNode, nodes, edges, args=None):
		"""
		Launch the sequence execution, place each new branch in another thread.
		"""
		self.threads+=1
		self.executeAction(app, self._getNodeLabel(startNode, nodes), args)
		for c in self._getChildren(startNode, edges):
			socketio.start_background_task(self._executeSequence, app, c, nodes, edges, args)
		self.threads-=1

	def executeAction(self, app, label, args=None):
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
			speech=option.split('"')[0]
			if args != None:
				speech=speech.replace(ENTITY_PATTERN, args[0])
			socketio.emit("response", speech, namespace="/client")
		elif(action=="relay"):
			#if it's a relay, first look for the associated pin, restore the request
			rel_label = option.rsplit(',',1)[0]
			rel_state=""
			#if the state is specified (0 or 1)
			if(len(option.rsplit(',',1))>1):
				rel_state=option.rsplit(',',1)[1]
			with app.app_context():
				db_rel = Relay.query.filter_by(label=rel_label).first()
				if(not db_rel.enabled):
					return
				pin = db_rel.pin
				parity = db_rel.parity
				raspi_id = db_rel.raspi_id

				#if the relay is paired
				if(parity!=""):
					#recover all the peer relays
					peers_rel = Relay.query.filter(Relay.parity==parity, Relay.label!=rel_label)
					peers=[]
					for peer in peers_rel:
						peers.append(peer.pin)

					socketio.emit("activate_paired_relay", (pin, rel_state, peers, raspi_id), namespace="/relay", broadcast=True)

				else:
					socketio.emit("activate_relay", (pin, rel_state, raspi_id), namespace="/relay")
		elif(action=="script"):
			#if it's a script, import the requested script and execute its start method
			spec = importlib.util.spec_from_file_location("script", os.path.join(SCRIPTS_LOCATION, option))
			script = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(script)
			socketio.emit("response", script.start(args), namespace="/client")
		elif(action=="sound"):
			#if it's a sound, execute the requested sound
			if config.getAudioOnServer:
				os.system("sudo pkill mplayer")
				os.system("mplayer "+join(SOUNDS_LOCATION,option).replace(" ", "\\ "))
				logging.info("Playing sound \'" + join(SOUNDS_LOCATION,option) + "\' on server")			
			else:
				socketio.emit("play_sound", option, namespace="/client")
		else:
			#sends the command to the raspberries
			logging.info("Sending "+action+" to rasperries.")
			socketio.emit("command", option, namespace="/"+action)
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

	def readSequence(self, app, json, args=None):
		"""
		Launch the sequence execution from a JSON object.
		"""
		if(self.threads>0): #wait for the current sequence to be completed to launch a new one
			return
		nodes=json[0]
		edges=json[1]
		self._executeSequence(app, "start", nodes, edges, args)


sequence_reader = SequenceReader()


@socketio.on('speech_detected', namespace='/client')
def speech_detected(transcript):
	"""
	Function called when a sentence is detected on the client.
	"""
	logging.info("Received data: " + transcript)
	response = chatbot.getResponse(transcript)
	response_text = response.text

	if(len(response_text.split("]"))>1):
		seq_name=response_text.split("[")[1].split("]")[0]
		seq = Sequence.query.filter_by(id=seq_name).first()
		response_text = response_text.split("]")[1]
		#if a sequence exists and is activated, launch it
		if(seq!=None and seq.enabled):
			seq_data = seq.value
			logging.info('Executing sequence: '+seq_name)
			entities=None
			if hasattr(response, 'entities'): #if entities are detected, we will pass them to the sequence
				entities=response.entities
				logging.info("Detected entities: "+str(entities))
			sequence_reader.readSequence(current_app._get_current_object(), json.loads(seq_data), entities)
	emit("response", response_text)


@socketio.on('play_sequence', namespace='/client')
def play_sequence(seq_name):
	"""
	Function called when the client want to execute a sequence.
	"""
	seq = Sequence.query.filter_by(id=seq_name).first()
	if(seq!=None and seq.enabled):
		seq_data = seq.value
		logging.info('Executing sequence '+seq_name)
		sequence_reader.readSequence(current_app._get_current_object(), json.loads(seq_data))

@socketio.on('command', namespace='/client')
def command(label):
	"""
	Function called when the client want to execute a simple command.
	"""
	logging.info("Received command: "+label)
	sequence_reader.executeAction(current_app._get_current_object(), label)

#!/usr/bin/python
# coding: utf-8

import logging
import json
from flask_socketio import SocketIO, emit
from .action_manager import ActionManager
from .sequence_reader import SequenceReader
from .. import socketio
from app.model import Sequence, chatbot

action_manager = ActionManager()
sequence_reader = SequenceReader(action_manager)

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
			sequence_reader.readSequence(json.loads(seq_data), entities)
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
		sequence_reader.readSequence(json.loads(seq_data))

@socketio.on('command', namespace='/client')
def command(label):
	"""
	Function called when the client want to execute a simple command.
	"""
	logging.info("Received command: "+label)
	sequence_reader.executeAction(label)
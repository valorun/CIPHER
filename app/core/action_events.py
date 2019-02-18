import logging
import json
from flask_socketio import SocketIO, emit
from .sequence_reader import SequenceReader
from app import socketio, mqtt
from app.model import Sequence

sequence_reader = SequenceReader()

@socketio.on('play_sequence', namespace='/client')
def play_sequence(seq_name):
	"""
	Function called when the client want to execute a sequence.
	"""
	logging.info("Client triggered sequence: \'" + seq_name + "\'")
	sequence_reader.launchSequence(seq_name)

@socketio.on('command', namespace='/client')
def command(label):
	"""
	Function called when the client want to execute a simple command.
	"""
	logging.info("Client sent command: " + label)
	sequence_reader.executeAction(label)
import logging
import json
from flask_socketio import SocketIO, emit
from .sequence_reader import SequenceReader
from .action_manager import relay, sound, motion
from app import socketio, mqtt
from app.model import Sequence

sequence_reader = SequenceReader()

@socketio.on('play_sequence', namespace='/client')
def play_sequence(seq_name, flags):
	"""
	Function called when the client want to execute a sequence.
	"""
	logging.debug("Client triggered sequence: \'" + seq_name + "\'")
	sequence_reader.launchSequence(seq_name, flags=flags)

@socketio.on('activate_relay', namespace='/client')
def activate_relay(label):
	"""
	Function called when the client want to activate a relay.
	"""
	logging.debug("Client triggered sequence: \'" + label + "\'")
	relay(label)

@socketio.on('play_sound', namespace='/client')
def play_sound_event(sound_name):
	"""
	Function called when the client want to play a sound.
	"""
	logging.debug("Client triggered sound: \'" + sound_name + "\'")
	sound(sound_name)

@socketio.on('move', namespace='/client')
def move(left, right):
	"""
	Function called when the client want to move the robot with the 2 motors.
	"""
	logging.debug("Client motion: " + left + ", " + right)
	motion(int(left), int(right))
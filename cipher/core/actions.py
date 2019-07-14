import logging
import json
import importlib.util
from subprocess import Popen
from os.path import join, exists
from flask_socketio import SocketIO, emit
from flask_mqtt import Mqtt
from cipher import socketio, mqtt
from cipher.constants import SCRIPTS_LOCATION, SOUNDS_LOCATION
from cipher.model import db, Servo, Relay, config

current_sound = None

def speech(speech:str):
	"""
	Speak on the client from the client or from the raspberry, according to the parameter
	"""
	if speech is None:
		return
	logging.info("Pronouncing '" + speech + "'")
	socketio.emit('response', speech, namespace='/client')

def relay(label:str, state=None):
	"""
	Activate the relay with the specified label
	"""
	if state != 1 and state != 0:
		state = ''
	with db.app.app_context():
		db_rel = Relay.query.filter_by(label=label).first()
		if db_rel is None or not db_rel.enabled:
			logging.warning("Unknown relay '" + label + "'.")
			return
		pin = db_rel.pin
		parity = db_rel.parity
		raspi_id = db_rel.raspi_id

		logging.info("Activating relay '" + label + "'")

		#if the relay is paired
		if parity!='':
			#recover all the peer relays
			peers_rel = Relay.query.filter(Relay.parity==parity, Relay.label!=label)
			peers=[]
			for peer in peers_rel:
				peers.append(peer.pin)
			#activate the relay on the corresponding raspberry
			mqtt.publish('raspi/' + raspi_id + '/relay/activate', json.dumps({'gpio':pin, 'state':state, 'peers':peers}))

		else:
			mqtt.publish('raspi/' + raspi_id + '/relay/activate', json.dumps({'gpio':pin, 'state':state, 'peers':None}))

def motion(direction:str, speed:int):
	"""
	Activate the motors with the specified speed
	"""
	if speed < 0 or speed > 100:
		return
	if config.getMotionRaspiId() is None:
		return
		
	logging.info("Moving with values " + direction + ", " + str(speed))
	mqtt.publish('raspi/' + config.getMotionRaspiId() + '/motion', json.dumps({'direction':direction, 'speed':speed}))
	
def servo(label:str, position:int, speed:int):
	"""
	Launch a servo motor to a position at a specified speed
	"""
	if speed < 0 or speed > 100:
		logging.warning("Out of range speed " + str(speed) + " for servo '" + label + "'.")
		return
	with db.app.app_context():
		db_servo = Servo.query.filter_by(label=label).first()
		if db_servo is None or not db_servo.enabled:
			logging.warning("Unknown or disabled servo '" + label + "'.")
			return
		if position < db_servo.min_pulse_width or position > db_servo.max_pulse_width:
			logging.warning("Out of range position " + str(position) + " for servo '" + label + "'.")
			return

		pin = db_servo.pin
		raspi_id = db_servo.raspi_id
		logging.info("Moving servo '" + label + "' to " + str(position) + " at speed " + str(speed))
		mqtt.publish('raspi/' + raspi_id + '/servo/set_position', json.dumps({'gpio':pin, 'position':position, 'speed':speed}))

def servo_sequence(index:int):
	"""
	COMPATIBILITY REASON
	Launch a servo sequence, specific to maestro card
	"""
	with db.app.app_context():
		db_servo = Servo.query.distinct(Servo.raspi_id).first()
		if db_servo is None:
			logging.warning("No default servo raspi set.")
			return
		raspi_id = db_servo.raspi_id
		logging.info("Executing servo sequence '" + str(index) + "'")
		mqtt.publish('raspi/' + raspi_id + '/servo/sequence', json.dumps({'index':index}))

def sound(sound_name:str):
	"""
	Execute the requested sound from the 'sounds' directory
	"""
	if not exists(join(SOUNDS_LOCATION, sound_name)):
		logging.warning("Cannot load sound '" + sound_name + "'")
		return

	if config.getAudioOnServer():
		logging.info("Playing sound '" + join(SOUNDS_LOCATION, sound_name) + "\' on server")
		if current_sound is None or current_sound.poll() is None: # if no sound is played or the current sound ended
			curent_sound = Popen(['mplayer', join(SOUNDS_LOCATION, sound_name)])	
		else:
			curent_sound.terminate()
	else:
		logging.info("Playing sound '" + sound_name + "' on client")			
		socketio.emit('play_sound', sound_name, namespace='/client')

def script(script_name:str, **kwargs):
	"""
	Import the requested script from the 'scripts' directory and execute its 'main' method
	"""
	if not exists(join(SCRIPTS_LOCATION, script_name)):
		logging.warning("Cannot load script '" + script_name + "'")
		return
	spec = importlib.util.spec_from_file_location('script', join(SCRIPTS_LOCATION, script_name))
	script = importlib.util.module_from_spec(spec)
	logging.info("Executing script '" + script_name + "'")			
	spec.loader.exec_module(script)
	result = script.main(**kwargs)
	if result is not None and type(result) == dict:
		return result

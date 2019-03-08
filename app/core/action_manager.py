import logging
import json
import importlib.util
from subprocess import Popen
from os.path import join, exists
from flask_socketio import SocketIO, emit
from flask_mqtt import Mqtt
from app import socketio, mqtt
from app.constants import SCRIPTS_LOCATION, SOUNDS_LOCATION
from app.model import db, Relay, config

current_sound = None
def speech(speech:str):
	"""
	Speak on the client from the client or from the raspberry, according to the parameter
	"""
	if(speech == None):
		return
	logging.info("Pronouncing \'" + speech + "\'")
	socketio.emit("response", speech, namespace="/client")

def relay(rel_label:str, rel_state=None):
	"""
	Activate the relay with the specified label
	"""
	if rel_state != 1 and rel_state != 0:
		rel_state=""
	with db.app.app_context():
		db_rel = Relay.query.filter_by(label=rel_label).first()
		if(not db_rel.enabled):
				return
		pin = db_rel.pin
		parity = db_rel.parity
		raspi_id = db_rel.raspi_id

		logging.info("Activating relay \'" + rel_label + "\'")

		#if the relay is paired
		if(parity!=""):
			#recover all the peer relays
			peers_rel = Relay.query.filter(Relay.parity==parity, Relay.label!=rel_label)
			peers=[]
			for peer in peers_rel:
				peers.append(peer.pin)
			#activate the relay on the corresponding raspberry
			mqtt.publish('raspi/'+raspi_id+'/relay/activate', json.dumps({'gpio':pin, 'state':rel_state, 'peers':peers}))
			#socketio.emit("activate_paired_relay", (pin, rel_state, peers, raspi_id), namespace="/relay", broadcast=True)

		else:
			mqtt.publish('raspi/'+raspi_id+'/relay/activate', json.dumps({'gpio':pin, 'state':rel_state, 'peers':None}))
			#socketio.emit("activate_relay", (pin, rel_state, raspi_id), namespace="/relay")

def motion(direction:str, speed:int):
	"""
	Activate the motors with the specified speed
	"""
	if config.getMotionRaspiId() == None:
		return
	logging.info("Moving with values " + direction + ", " + str(speed))
	mqtt.publish('raspi/'+config.getMotionRaspiId()+'/motion', json.dumps({'direction':direction, 'speed':speed}))
	
def servo(index:int):
	"""
	Launch a servomotor sequence with the given id
	"""
	if config.getServoRaspiId() == None:
		return
	logging.info("Executing servo sequence \'" + index + "\'")
	mqtt.publish('raspi/'+config.getServoRaspiId()+'/servo', json.dumps({'index':index}))

def sound(sound_name:str):
	"""
	Execute the requested sound from the 'sounds' directory
	"""
	if not exists(join(SOUNDS_LOCATION, sound_name)):
		logging.error("Cannot load sound \'" + sound_name + "\'")
		return

	if config.getAudioOnServer():
		logging.info("Playing sound \'" + join(SOUNDS_LOCATION, sound_name) + "\' on server")
		if current_sound == None or current_sound.poll() == None: # if no sound is played or the current sound ended
			curent_sound = Popen(['mplayer', join(SOUNDS_LOCATION, sound_name).replace(" ", "\\ ")])	
		else:
			curent_sound.terminate()
	else:
		logging.info("Playing sound \'" + sound_name + "\' on client")			
		socketio.emit("play_sound", sound_name, namespace="/client")

def script(script_name:str, **kwargs):
	"""
	Import the requested script from the 'scripts' directory and execute its 'main' method
	"""
	if not exists(join(SCRIPTS_LOCATION, script_name)):
		logging.error("Cannot load script \'" + script_name + "\'")
		return
	spec = importlib.util.spec_from_file_location("script", join(SCRIPTS_LOCATION, script_name))
	script = importlib.util.module_from_spec(spec)
	logging.info("Executing script \'" + script_name + "\'")			
	spec.loader.exec_module(script)
	result = script.main(**kwargs)
	if(result != None and type(result) == dict):
		return result

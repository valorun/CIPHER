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


class Action:
    def __init__(self):
        pass

    def execute(self, **kwargs):
        pass


class SpeechAction(Action):
    """
    Speak on the client from the client or from the raspberry,
    according to the parameter
    """
    def __init__(self, text: str):
        self.text = text

    def execute(self, **kwargs):
        if self.text is None:
            return
        logging.info("Pronouncing '" + self.text + "'")
        socketio.emit('response', self.text, namespace='/client')


class RelayAction(Action):
    """
    Activate the relay with the specified label
    """
    relay_states = {}

    def __init__(self, label: str, state: int = None):
        self.label = label
        self.state = state

    def execute(self, **kwargs):
        if self.state != 1 and self.state != 0:
            self.state = ''
        with db.app.app_context():
            db_rel = Relay.query.filter_by(label=self.label).first()
            if db_rel is None or not db_rel.enabled:
                logging.warning("Unknown relay '" + self.label + "'.")
                return
            pin = db_rel.pin
            parity = db_rel.parity
            raspi_id = db_rel.raspi_id

            logging.info("Activating relay '" + self.label + "'")

            # if the relay is paired
            if parity != '':
                # recover all the pair relays
                pairs_rel = Relay.query.filter(Relay.parity == parity, Relay.label != self.label)
                # check if the pairs relays aren't activated
                if all([pair.label not in RelayAction.relay_states or RelayAction.relay_states[pair.label] == 0 for pair in pairs_rel]):
                    # activate the relay on the corresponding raspberry
                    mqtt.publish('raspi/' + raspi_id + '/relay/activate', json.dumps({'gpio': pin, 'state': self.state}))
                else:
                    logging.warning("Cannot activate relay '" + self.label + "', pair already activated")

            else:
                mqtt.publish('raspi/' + raspi_id + '/relay/activate', json.dumps({'gpio': pin, 'state': self.state}))


class MotionAction(Action):
    """
    Activate the motors with the specified speed
    """
    def __init__(self, direction: str, speed: int):
        self.direction = direction
        self.speed = speed

    def execute(self, **kwargs):
        if self.speed < 0 or self.speed > 100:
            return
        if config.get_motion_raspi_id() is None:
            return

        logging.info("Moving with values " + self.direction + ", " + str(self.speed))
        mqtt.publish('raspi/' + config.get_motion_raspi_id() + '/motion', json.dumps({'direction': self.direction, 'speed': self.speed}))


class ServoAction(Action):
    """
    Launch a servo motor to a position at a specified speed
    """
    def __init__(self, label: str, position: int, speed: int):
        self.label = label
        self.position = position
        self.speed = speed

    def execute(self, **kwargs):
        if self.speed < 0 or self.speed > 100:
            logging.warning("Out of range speed " + str(self.speed) + " for servo '" + self.label + "'.")
            return
        with db.app.app_context():
            db_servo = Servo.query.filter_by(label=self.label).first()
            if db_servo is None or not db_servo.enabled:
                logging.warning("Unknown or disabled servo '" + self.label + "'.")
                return
            if self.position < db_servo.min_pulse_width or self.position > db_servo.max_pulse_width:
                logging.warning("Out of range position " + str(self.position) + " for servo '" + self.label + "'.")
                return

            pin = db_servo.pin
            raspi_id = db_servo.raspi_id
            logging.info("Moving servo '" + self.label + "' to " + str(self.position) + " at speed " + str(self.speed))
            mqtt.publish('raspi/' + raspi_id + '/servo/set_position', json.dumps({'gpio': pin, 'position': self.position, 'speed': self.speed}))


class ServoSequenceAction(Action):
    """
    COMPATIBILITY REASON
    Launch a servo sequence, specific to maestro card
    """
    def __init__(self, index: int):
        self.index = index

    def execute(self, **kwargs):
        with db.app.app_context():
            db_servo = Servo.query.distinct(Servo.raspi_id).first()
            if db_servo is None:
                logging.warning("No default servo raspi set.")
                return
            raspi_id = db_servo.raspi_id
            logging.info("Executing servo sequence '" + str(self.index) + "'")
            mqtt.publish('raspi/' + raspi_id + '/servo/sequence', json.dumps({'index': self.index}))


class SoundAction(Action):
    """
    Execute the requested sound from the 'sounds' directory
    """
    curent_sound = None

    def __init__(self, sound_name: str):
        self.sound_name = sound_name

    def execute(self, **kwargs):
        if not exists(join(SOUNDS_LOCATION, self.sound_name)):
            logging.warning("Cannot load sound '" + self.sound_name + "'")
            return

        if config.getAudioOnServer():
            logging.info("Playing sound '" + join(SOUNDS_LOCATION, self.sound_name) + "\' on server")
            if SoundAction.curent_sound is None or SoundAction.curent_sound.poll() is None:  # if no sound is played or the current sound ended
                curent_sound = Popen(['mplayer', join(SOUNDS_LOCATION, self.sound_name)])
            else:
                curent_sound.terminate()
        else:
            logging.info("Playing sound '" + self.sound_name + "' on client")
            socketio.emit('play_sound', self.sound_name, namespace='/client')


class ScriptAction():
    """
    Import the requested script from the 'scripts' directory and execute its 'main' method
    """
    def __init__(self, script_name: str):
        self.script_name = script_name

    def execute(self, **kwargs):
        if not exists(join(SCRIPTS_LOCATION, self.script_name)):
            logging.warning("Cannot load script '" + self.script_name + "'")
            return
        spec = importlib.util.spec_from_file_location('script', join(SCRIPTS_LOCATION, self.script_name))
        script = importlib.util.module_from_spec(spec)
        logging.info("Executing script '" + self.script_name + "'")
        spec.loader.exec_module(script)
        result = script.main(**kwargs)
        if result is not None and type(result) == dict:
            return result

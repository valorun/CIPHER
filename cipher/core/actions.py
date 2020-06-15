import logging
import json
import importlib.util
from typing import List
from subprocess import Popen
from os.path import join, exists
from flask_socketio import SocketIO, emit
from flask_mqtt import Mqtt
from cipher import socketio, mqtt
from cipher.model import db, Servo, Relay, resources
from cipher.config import core_config
from cipher.core.action_parameters import *

class Action:
    display_name = ''

    @staticmethod
    def execute():
        """
        Execute the action with some parameters.
        """
        pass

    @staticmethod
    def check_parameters() -> (bool, str):
        """
        Check the given parameters to ensure they are suitable for the method execute.
        Return False and a message if the parameters are incorrect, True otherwise.
        """
        return True, None

    @staticmethod
    def get_parameters() -> List[ActionParameter]:
        """
        Get all the parameters needed in order to execute the action.
        This method is used to dynamically display the different form to set up the execution.
        """
        return []

    @staticmethod
    def get_from_name(name: str) -> 'Action':
        if name in DEFAULT_ACTIONS:
            action_class = DEFAULT_ACTIONS[name]
        elif name in CUSTOM_ACTIONS:
            action_class = CUSTOM_ACTIONS[name]
        else:
            raise ValueError('Unknown action \'' + name + '\'')
        return action_class


class SpeechAction(Action):
    """
    Speak on the client from the client or from the raspberry,
    according to the parameter
    """
    display_name = 'Parole'
    @staticmethod
    def check_parameters(text: str):
        if not isinstance(text, str):
            return False, "The text must be a string."
        return True, None

    @staticmethod
    def get_parameters():
        return [StringParameter('text', 'Texte', 'Exemple: bonjour, je suis un robot')]

    @staticmethod
    def execute(text: str):
        valid, message = SpeechAction.check_parameters(text)
        if not valid:
            logging.warning(message)
            return

        logging.info("Pronouncing '" + text + "'")
        socketio.emit('response', text, namespace='/client')

class RelayAction(Action):
    """
    Activate the relay with the specified label
    """
    display_name = 'Relai'
    relay_states = {}

    @staticmethod
    def check_parameters(label: str, state: int = None):
        if not isinstance(label, str):
            return False, "The label must be a string."
        with db.app.app_context():
            db_rel = Relay.query.filter_by(label=label, enabled=True).first()
            if db_rel is None:
                return False, "Unknown or disabled relay '" + label + "'."
        return True, None

    @staticmethod
    def get_parameters():
        with db.app.app_context():
            return [StringParameter('label', 'Label', '', {r.label : r.label for r in Relay.query.filter_by(enabled=True).all()}),
                    BooleanParameter('state', 'On/Off')]

    @staticmethod
    def execute(label: str, state: int = None):
        if state != 1 and state != 0:
            state = ''
        
        valid, message = RelayAction.check_parameters(label)
        if not valid:
            logging.warning(message)
            return

        logging.info("Activating relay '" + label + "'")

        with db.app.app_context():
            db_rel = Relay.query.filter_by(label=label, enabled=True).first()
            pin = db_rel.pin
            parity = db_rel.parity
            raspi_id = db_rel.raspi_id

            # if the relay is paired
            if parity != '':
                # recover all the pair relays
                pairs_rel = Relay.query.filter(Relay.parity == parity, Relay.label != label)
                # check if the pairs relays aren't activated
                if all([pair.label not in RelayAction.relay_states or RelayAction.relay_states[pair.label] == 0 for pair in pairs_rel]):
                    # activate the relay on the corresponding raspberry
                    mqtt.publish('raspi/' + raspi_id + '/relay/activate', json.dumps({'gpio': pin, 'state': state}))
                else:
                    logging.warning("Cannot activate relay '" + label + "', pair already activated")

            else:
                mqtt.publish('raspi/' + raspi_id + '/relay/activate', json.dumps({'gpio': pin, 'state': state}))
    

class MotionAction(Action):
    """
    Activate the motors with the specified speed
    """
    display_name = 'Déplacement'

    @staticmethod
    def check_parameters(direction: str, speed: int):
        if speed < 0 or speed > 100:
            return False, "Speed must be a number between 0 and 100."
        if core_config.get_motion_raspi_id() is None:
            return False, "No raspberry has been designated for motion."
        if not core_config.get_enable_motion():
            return False, "Motions are disbled."
        return True, None

    @staticmethod
    def get_parameters():
        return [StringParameter('direction', 'Direction', '', 
                    { 'forwards': 'Avant', 'backwards': 'Arrière', 'left': 'Gauche', 'right': 'Droite'}),
                IntegerParameter('speed', 'Vitesse', '', 0, 100)]

    @staticmethod
    def execute(direction: str, speed: int):
        valid, message = MotionAction.check_parameters(direction, speed)
        if not valid:
            logging.warning(message)
            return

        logging.info("Moving with values " + direction + ", " + str(speed))
        mqtt.publish('raspi/' + core_config.get_motion_raspi_id() + '/motion', json.dumps({'direction': direction, 'speed': speed}))

class ServoAction(Action):
    """
    Launch a servo motor to a position at a specified speed
    """
    display_name = 'Servomoteur'

    @staticmethod
    def check_parameters(label: str, position: int, speed: int):
        if not isinstance(label, str):
            return False, "The relay label must be a string."
        if not isinstance(position, int):
            return False, "The position must be an integer."
        if not isinstance(speed, int) or speed < 0 or speed > 100:
            return False, "Speed must be a number between 0 and 100."
        with db.app.app_context():
            db_servo = Servo.query.filter_by(label=label, enabled=True).first()
            if db_servo is None:
                return False, "Unknown or disabled servo '" + label + "'."
            if position < db_servo.min_pulse_width or position > db_servo.max_pulse_width:
                return False, "Out of range position " + str(position) + " for servo '" + label + "'. The value must be between " + str(db_servo.min_pulse_width) + " and " + str(db_servo.max_pulse_width) + "."
        return True, None

    @staticmethod
    def get_parameters():
        with db.app.app_context():
            return [StringParameter('label', 'Label', '', { s.label : s.label for s in Servo.query.filter_by(enabled=True).all() }),
                    IntegerParameter('position', 'Position'),
                    IntegerParameter('speed', 'Vitesse', '', 0, 100)]
    
    @staticmethod
    def execute(label: str, position: int, speed: int):
        valid, message = ServoAction.check_parameters(label, position, speed)
        if not valid:
            logging.warning(message)
            return

        with db.app.app_context():
            db_servo = Servo.query.filter_by(label=label).first()

            pin = db_servo.pin
            raspi_id = db_servo.raspi_id
            logging.info("Moving servo '" + label + "' to " + str(position) + " at speed " + str(speed))
            mqtt.publish('raspi/' + raspi_id + '/servo/set_position', json.dumps({'gpio': pin, 'position': position, 'speed': speed}))

class ServoSequenceAction(Action):
    """
    COMPATIBILITY REASON
    Launch a servo sequence, specific to maestro card
    """
    display_name = 'Séquence servomoteurs (COMPATIBILITE)'

    @staticmethod
    def check_parameters(index: int):
        if not isinstance(index, int):
            return False, "The index must be a valid number."
        return True, None

    @staticmethod
    def get_parameters():
        return [IntegerParameter('index', 'Index', '', 0, 100)]

    @staticmethod
    def execute(index: int):
        valid, message = ServoSequenceAction.check_parameters(index)
        if not valid:
            logging.warning(message)
            return
        with db.app.app_context():
            db_servo = Servo.query.distinct(Servo.raspi_id).first()
            if db_servo is None:
                logging.warning("No default servo raspi set.")
                return
            raspi_id = db_servo.raspi_id
            logging.info("Executing servo sequence '" + str(index) + "'")
            mqtt.publish('raspi/' + raspi_id + '/servo/sequence', json.dumps({'index': index}))

class SoundAction(Action):
    """
    Execute the requested sound from the 'sounds' directory
    """
    display_name = 'Son'
    current_sound = None

    @staticmethod
    def check_parameters(name: str):
        if not isinstance(name, str):
            return False, "The name must be a string."
        if not resources.sound_exists(name):
            return False, "Cannot load sound '" + name + "'"
        return True, None

    @staticmethod
    def get_parameters():
        return [StringParameter('name', 'Nom', '', {s : s for s in resources.get_sounds()})]

    @staticmethod
    def execute(name: str):
        valid, message = SoundAction.check_parameters(name)
        if not valid:
            logging.warning(message)
            return

        if not core_config.get_audio_on_server():
            if SoundAction.current_sound is None or SoundAction.current_sound.poll() is not None:  # if no sound is played or the current sound ended
                logging.info("Playing sound '" + resources.get_sound_path(name) + "\' on server")
                SoundAction.current_sound = Popen(['mplayer', resources.get_sound_path(name)])
            else:
                SoundAction.current_sound.terminate()
        else:
            logging.info("Playing sound '" + name + "' on client")
            socketio.emit('play_sound', name, namespace='/client')

DEFAULT_ACTIONS = {'relay': RelayAction, 'sound': SoundAction, 'speech': SpeechAction, 'servo': ServoAction, 'servoSequence': ServoSequenceAction, 'motion': MotionAction}
CUSTOM_ACTIONS = {}
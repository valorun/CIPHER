import logging
import json
from flask_socketio import SocketIO, emit
from flask_mqtt import Mqtt
from .sequence_reader import sequence_reader
from .actions import RelayAction, SoundAction, MotionAction
from cipher import socketio, mqtt
from cipher.model import Relay


@socketio.on('play_sequence', namespace='/client')
def play_sequence(seq_name: str):
    """
    Function called when the client want to execute a sequence.
    """
    logging.debug("Client triggered sequence: '" + seq_name + "'")
    sequence_reader.launch_sequence(seq_name)


@socketio.on('activate_relay', namespace='/client')
def activate_relay(label: str):
    """
    Function called when the client want to activate a relay.
    """
    logging.debug("Client triggered relay: '" + label + "'")
    RelayAction(label).execute()


@socketio.on('play_sound', namespace='/client')
def play_sound_event(sound_name: str):
    """
    Function called when the client want to play a sound.
    """
    logging.debug("Client triggered sound: '" + sound_name + "'")
    SoundAction(sound_name).execute()


@socketio.on('move', namespace='/client')
def move(direction: str, speed: int):
    """
    Function called when the client want to move the robot with the 2 motors.
    """
    logging.debug("Client triggered motion: " + direction + ", " + str(speed))
    MotionAction(direction, int(speed)).execute()


@socketio.on('get_relays_state', namespace='/client')
def get_relays_state():
    global RelayAction
    emit('receive_relays_state', [{'relay': l, 'state': RelayAction.relay_states[l]} for l in RelayAction.relay_states], namespace='/client', broadcast=False)


@mqtt.on_topic('server/update_relays_state')
def update_relays_state(client, userdata, msg):
    """
    Update the state of the relays on the client side at the request of a raspberry.
    """
    global RelayAction
    logging.info("Updating relay status")
    relays_list = []  # relays to update
    data = json.loads(msg.payload.decode('utf-8'))
    # for each specified relay ...
    for rel in data['relays']:
        raspi_id = rel['raspi_id']
        pin = rel['gpio']
        state = rel['state']
        # retrieve the missing information: the label corresponding to the pin
        for db_rel in Relay.query.filter_by(pin=pin, raspi_id=raspi_id):
            label = db_rel.label
            relays_list.append({'relay': label, 'state': state})
        # update the local state dictionnary
        RelayAction.relay_states[label] = state
    # finally send the list of the relays to update on the clients
    socketio.emit('receive_relays_state', relays_list, namespace="/client", broadcast=True)

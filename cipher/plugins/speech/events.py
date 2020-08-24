import json
from . import speech
from .model import Intent
from flask_socketio import SocketIO, emit
from cipher import socketio, mqtt
from cipher.core.sequence_reader import sequence_reader

@speech.startup()
def on_startup():
    """
    Function called when the server connects to the broker.
    """
    mqtt.subscribe('speech/#')

@mqtt.on_topic('speech/intent/#')
def handle_intents(client, userdata, message):
    intent = message.topic
    speech.log.info(intent)
    speech.log.info("Received intent '" + intent + "'")
    db_intent = Intent.query.filter_by(intent=intent).first()

    if(db_intent is not None):
        if db_intent.sequence is not None:
            sequence_reader.launch_sequence(db_intent.sequence.id, **intent)

@socketio.on('start_speech_recognition', namespace='/client')
def start_speech_recognition():
    speech.log.info("Started speech recognition")
    mqtt.publish('speech/start')

@socketio.on('stop_speech_recognition', namespace='/client')
def stop_speech_recognition():
    speech.log.info("Stopped speech recognition")
    mqtt.publish('speech/stop')
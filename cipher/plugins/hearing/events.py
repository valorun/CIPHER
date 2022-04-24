import json
from . import hearing
from .model import Intent
from flask_socketio import SocketIO, emit
from cipher import socketio, mqtt
from cipher.core.sequence_reader import sequence_reader

@mqtt.on_topic('server/hearing/intent/#')
def handle_intents(client, userdata, message):
    intent = message.topic
    hearing.log.info(intent)
    hearing.log.info("Received intent '" + intent + "'")
    db_intent = Intent.query.filter_by(intent=intent).first()

    if db_intent is not None:
        if db_intent.sequence is not None:
            sequence_reader.launch_sequence(db_intent.sequence.id, **intent)

@socketio.on('start_speech_recognition', namespace='/client')
def start_speech_recognition():
    hearing.log.info("Started speech recognition")
    mqtt.publish('client/hearing/start')

@socketio.on('stop_speech_recognition', namespace='/client')
def stop_speech_recognition():
    hearing.log.info("Stopped speech recognition")
    mqtt.publish('client/hearing/stop')
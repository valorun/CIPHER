import json
from . import hearing
from .model import Intent, chat_queue
from flask_socketio import SocketIO, emit
from datetime import datetime as dt
from cipher import socketio, mqtt
from cipher.core.sequence_reader import sequence_reader

@hearing.startup()
def on_startup():
    """
    Function called when the server connects to the broker.
    """
    mqtt.subscribe('client/speech/speak')

@mqtt.on_topic('client/speech/speak')
def on_speak(client, userdata, message):
    """
    Function called when the robot needs to speak.
    """
    msg_obj = {'message': json.loads(message.payload.decode('utf-8'))['text'], 'source': 'robot', 'time': dt.now().strftime('%H:%M')}
    chat_queue.append(msg_obj)
    socketio.emit('chat', msg_obj, namespace='/client', broadcast=True)


@mqtt.on_topic('server/hearing/intent/#')
def handle_intents(client, userdata, message):
    global chat_queue
    payload = json.loads(message.payload.decode('utf-8'))
    intent = payload['intent']['intentName']
    hearing.log.info("Received intent '" + intent + "'")
    db_intent = Intent.query.filter_by(intent=intent).first()

    if db_intent is not None:
        if db_intent.sequence_id is not None:
            sequence_reader.launch_sequence(db_intent.sequence_id, **payload)
    
    msg_obj = {'message': payload['input'], 'source': 'user', 'time':  dt.now().strftime('%H:%M')}
    chat_queue.append(msg_obj)
    socketio.emit('chat', msg_obj, namespace='/client', broadcast=True)


@socketio.on('start_speech_recognition', namespace='/client')
def start_speech_recognition():
    hearing.log.info("Started speech recognition")
    mqtt.publish('client/hearing/start')

@socketio.on('stop_speech_recognition', namespace='/client')
def stop_speech_recognition():
    hearing.log.info("Stopped speech recognition")
    mqtt.publish('client/hearing/stop')
    
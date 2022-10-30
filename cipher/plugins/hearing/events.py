import json
from . import hearing
from .model import chat_queue
from flask_socketio import SocketIO, emit
from datetime import datetime as dt
from cipher import socketio, mqtt
from cipher.core.triggers import execute_trigger, registered_triggers

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

@mqtt.on_topic('server/hearing/register')
def register_intents(client, userdata, message):
    global registered_triggers
    data = json.loads(message.payload.decode('utf-8'))
    for intent in data:
        registered_triggers.add('intent_' + intent)


@mqtt.on_topic('server/hearing/intent/#')
def handle_intents(client, userdata, message):
    global chat_queue
    payload = json.loads(message.payload.decode('utf-8'))
    intent = payload['intent']['intentName']
    hearing.log.info("Received intent '" + intent + "'")
    hearing.log.debug(str(payload))
    execute_trigger(intent, **payload)
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
    
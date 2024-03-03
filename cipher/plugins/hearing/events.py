import json
from . import hearing
from .model import chat_queue
from .config import llm_config
from flask_socketio import SocketIO, emit
from datetime import datetime as dt
from cipher import socketio, mqtt
from cipher.core.sequence_reader import sequence_reader
from cipher.core.actions import SpeechAction

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



@mqtt.on_topic('server/hearing/transcription')
def handle_intents(client, userdata, message):
    global chat_queue
    message = message.payload.decode('utf-8')
    # TODO call LLM
    # use llm_config

    action = payload['action']
    hearing.log.info(f"Received actions '{action['name']}'")
    hearing.log.debug(str(payload))
    if action['name'] == 'speak':
        if 'text' in action['parameters']:
            SpeechAction.execute(action['parameters']['text'])
        else:
            hearing.log.error("No text in the action parameters")
    else:
        sequence_reader.launch_sequence(action['name'], **action['parameters'])
    msg_obj = {'message': message, 'source': 'user', 'time':  dt.now().strftime('%H:%M')}
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
    

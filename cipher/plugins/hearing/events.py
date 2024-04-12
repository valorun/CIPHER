import json
from datetime import datetime as dt

import requests

from cipher import mqtt, socketio
from cipher.core.actions import SpeechAction
from cipher.core.sequence_reader import sequence_reader
from cipher.model import Sequence, db

from . import hearing
from .config import llm_config
from .model import chat_queue


@hearing.startup()
def on_startup():
    """
    Function called when the server connects to the broker.
    """
    mqtt.subscribe("client/speech/speak")


@mqtt.on_topic("client/speech/speak")
def on_speak(client, userdata, message):
    """
    Function called when the robot needs to speak.
    """
    msg_obj = {
        "message": json.loads(message.payload.decode("utf-8"))["text"],
        "source": "robot",
        "time": dt.now().strftime("%H:%M"),
    }
    chat_queue.append(msg_obj)
    socketio.emit("chat", msg_obj, namespace="/client", broadcast=True)


@mqtt.on_topic("server/hearing/transcription")
def handle_transcription(client, userdata, message):
    global chat_queue
    user_message = message.payload.decode("utf-8")

    # Pass available actions to the LLM
    with db.app.app_context():
        sequences = Sequence.query.all()
    available_actions = [
        {"name": sequence.id, "description": sequence.description, "parameters": {}}
        for sequence in sequences
    ]
    available_actions.append(
        {
            "name": "speak",
            "description": "Prononce une phrase",
            "parameters": {"text": "string"},
        }
    )

    # Call LLM endpoint
    llm_payload = {
        "history": list(chat_queue),
        "message": user_message,
        "available_actions": available_actions,
    }
    print(llm_payload)
    llm_response = requests.post(
        llm_config.get_llm_server_inference_url(), json=llm_payload
    ).json()

    msg_obj = {
        "content": user_message,
        "role": "user",
        "time": dt.now().strftime("%H:%M"),
    }
    chat_queue.append(msg_obj)
    socketio.emit("chat", msg_obj, namespace="/client", broadcast=True)

    action = llm_response["action"]
    hearing.log.info(f"Received actions '{action['name']}'")
    hearing.log.debug(str(llm_response))
    if action["name"] == "speak":
        if "text" in action["parameters"]:
            SpeechAction.execute(action["parameters"]["text"])
        else:
            hearing.log.error("No text in the action parameters")
    else:
        sequence_reader.launch_sequence(action["name"], **action["parameters"])
    msg_obj = {
        "content": action,
        "role": "assistant",
        "time": dt.now().strftime("%H:%M"),
    }
    chat_queue.append(msg_obj)
    socketio.emit("chat", msg_obj, namespace="/client", broadcast=True)


@socketio.on("enable_speech_recognition", namespace="/client")
def enable_speech_recognition():
    hearing.log.info("Enabled speech recognition")
    mqtt.publish("client/hearing/start")


@socketio.on("disable_speech_recognition", namespace="/client")
def disable_speech_recognition():
    hearing.log.info("Disabled speech recognition")
    mqtt.publish("client/hearing/stop")

@socketio.on("trigger_speech_recognition", namespace="/client")
def trigger_speech_recognition():
    hearing.log.info("Triggered recording")
    mqtt.publish("client/hearing/trigger")

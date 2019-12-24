import logging
from .model import Intent
import json
from cipher import mqtt
from cipher.core.sequence_reader import sequence_reader
from cipher.core.actions import ScriptAction

@mqtt.on_topic('hermes/intent/#')
def handle_intents(client, userdata, message):
    intent = message.payload.decode('utf-8')
    try:
        intent = json.loads(intent)
    except Exception:
        return
    intentName = intent['intent']['intentName']
    logging.info("Received intent '" + intentName + "' with slots '" + str(intent['slots']) + "'")
    dbIntent = Intent.query.filter_by(intent=intentName).first()
    kwargs = {}
    kwargs['slots'] = intent['slots']
    if(dbIntent is not None):
        if dbIntent.sequence is not None:
            sequence_reader.launchSequence(dbIntent.sequence.id, **kwargs)
        elif dbIntent.script_name is not None:
            ScriptAction(dbIntent.script_name).execute(**kwargs)

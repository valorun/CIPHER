from .model import Intent
from . import speech
import json
from cipher import mqtt
from cipher.core.sequence_reader import sequence_reader

@mqtt.on_topic('speech/intent/#')
def handle_intents(client, userdata, message):
    intent = message.payload.decode('utf-8')
    try:
        intent = json.loads(intent)
    except Exception:
        return
    intent_name = intent['intentName']
    speech.log.info("Received intent '%s'", intent_name)
    db_intent = Intent.query.filter_by(intent=intent_name).first()

    if(db_intent is not None):
        if db_intent.sequence is not None:
            sequence_reader.launch_sequence(db_intent.sequence.id, **intent)


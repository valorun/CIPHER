import logging
from app.model import db, Intent
import json
from app import mqtt
from app.core.action_events import sequence_reader
from app.core.action_manager import speech

@mqtt.on_topic('hermes/intent/#')
def handle_intents(client, userdata, message):
    intent = message.payload.decode('utf-8').rsplit('/',1)[1]
    db_intent = Intent.query.filter_by(intent=intent).first()
    slots = {}
    if(db_intent != None):
        speech(db_intent.response)
        sequence_reader.launchSequence(db_intent.sequence, **slots)


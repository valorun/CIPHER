import logging
from cipher.model import db, Intent, Sequence
import json
from cipher import mqtt
from cipher.core.sequence_reader import sequence_reader
from cipher.core.actions import speech

@mqtt.on_topic('hermes/intent/#')
def handle_intents(client, userdata, message):
	intent = message.payload.decode('utf-8')
	try:
		intent = json.loads(intent)
	except Exception:
		return
	intentName = intent['intent']['intentName']
	logging.info('Received intent \'' + intentName + '\' with slots \'' + str(intent['slots']) + '\'')
	db_intent = Intent.query.filter_by(intent=intentName).first()
	kwargs = {}
	kwargs['flags'] = [intentName]
	kwargs['slots'] = intent['slots']
	if(db_intent != None):
		speech(db_intent.response)
		sequence_reader.launchSequence(db_intent.sequence.id, **kwargs)

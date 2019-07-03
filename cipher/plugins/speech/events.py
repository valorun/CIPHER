import logging
from cipher.model import db, Intent, Sequence
import json
from cipher import mqtt
from cipher.core.sequence_reader import sequence_reader
from cipher.core.actions import script

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
	kwargs['slots'] = intent['slots']
	if(db_intent is not None):
		if db_intent.sequence is not None:
			sequence_reader.launchSequence(db_intent.sequence.id, **kwargs)
		elif db_intent.script_name is not None:
			script(db_intent.script_name, **kwargs)

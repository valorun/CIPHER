import requests
import json
import uuid
from . import speech
from .config import voice_config
from cipher import mqtt
from cipher.model import resources
from cipher.core.actions import SoundAction

last_temp_sound = None
@speech.startup()
def on_startup():
    """
    Function called when the server connects to the broker.
    """
    mqtt.subscribe('client/speech/speak')

@mqtt.on_topic('client/speech/speak')
def on_speak(client, userdata, msg):
    """
    Function called when the robot needs to speak.
    """
    global last_temp_sound
    if voice_config.get_voice() is None:
        speech.log.debug("Trying to speak but, no voice is set")
        return
    data = json.loads(msg.payload.decode('utf-8'))
    text = data['text']
    url = 'http://' + voice_config.SERVER_ADDRESS + ':' + str(voice_config.SERVER_PORT) + '/process?INPUT_TYPE=TEXT&OUTPUT_TYPE=AUDIO&AUDIO=WAVE_FILE&LOCALE=fr&INPUT_TEXT=' + text
    url += '&VOICE=' + voice_config.get_voice()
    for effect_name, effect in voice_config.effects.items():
        url += '&effect_' + effect_name + '_selected=' + ('on' if effect.is_enabled() else 'off')
        url += '&effect_' + effect_name + '_parameters=' + effect.param_name + ':' + str(effect.get()) + ';'
    r = requests.get(url)
    if last_temp_sound is not None:
        resources.delete_sound(last_temp_sound)
    temp_sound = '.' + str(uuid.uuid4().hex) + '.wav'
    resources.write_sound(temp_sound, r.content)
    SoundAction.execute(temp_sound)
    last_temp_sound = temp_sound
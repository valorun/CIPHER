import requests
from flask import Flask, session, request, jsonify
from . import speech
from .config import voice_config
from cipher.security import login_required


@speech.route('/speech')
@login_required
def speech_page():
    voices = fetch_voices()
    return speech.render_page('speech.html', voice_config=voice_config, voices=voices)

@speech.route('/save_voice', methods=['POST'])
@login_required
def save_voice():
    voice_name = request.json.get('voice_name')
    effects = request.json.get('effects')
    for e in effects:
        voice_config.effects[e['name']].set(e['value']).enable(e['enabled'])
    
    voices = fetch_voices()
    if voice_name in voices:
        voice_config.set_voice(voice_name)
    return jsonify("La voix a été sauvegardée avec succès."), 200


def fetch_voices():
    voices = requests.get('http://' + voice_config.SERVER_ADDRESS + ':' + str(voice_config.SERVER_PORT) + '/voices')
    voices = [v.split(' ')[0] for v in voices.text.split('\n')]
    voices = [v for v in voices if v is not None and v != '']
    return voices
import os
import glob
from flask import Flask, session, request, jsonify
from . import speech
from .config import voice_config, VOICES_DIR
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
    voices = fetch_voices()
    if voice_name in voices:
        voice_config.set_voice(voice_name)
    return jsonify("La voix a été sauvegardée avec succès."), 200

def fetch_voices():
    # A voice is valid if both .npy and .txt exist
    voices = []
    for npy_file in glob.glob(os.path.join(VOICES_DIR, '*.npy')):
        base_name = os.path.basename(npy_file)[:-4] # remove .npy
        txt_file = os.path.join(VOICES_DIR, base_name + '.txt')
        if os.path.exists(txt_file):
            voices.append(base_name)
    return sorted(voices)

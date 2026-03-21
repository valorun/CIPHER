import json
import re
import threading
from flask import Flask, session, request, jsonify
from . import hearing
from .model import chat_queue
from cipher.security import login_required
from cipher import mqtt

@hearing.route("/hearing")
@login_required
def hearing_page():
    return hearing.render_page("hearing.html", chat_records=list(chat_queue))

@hearing.route("/text_input", methods=["POST"])
@login_required
def text_input():
    """
    Inject a transcription directly into the hearing system.
    """
    transcript = request.json.get("transcript")
    if not transcript:
        return jsonify("Transcription manquante."), 400
    
    hearing.log.info("Processing manual text input: '%s'", transcript)
    mqtt.publish("server/hearing/transcription", transcript)
    return jsonify("Transcription traitée."), 200

@hearing.route("/reset_chat", methods=["POST"])
@login_required
def reset_chat():
    """
    Clear the chat history.
    """
    chat_queue.clear()
    from cipher import socketio
    socketio.emit("clear_chat", namespace="/client")
    return jsonify("Historique effacé."), 200

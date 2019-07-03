import logging
import json
import re
from flask import Flask, session, request, redirect
from . import speech
from cipher.model import Sequence, Intent, db, resources
from cipher.security import login_required

@speech.route('/speech')
@login_required
def speech_page():
    sequences=Sequence.query.all()
    scripts=resources.getScripts()
    intents=Intent.query.all()
    return speech.render_page('speech.html', sequences=sequences, scripts=scripts, intents=intents)

@speech.route('/save_intent', methods=['POST'])
@login_required
def save_intent():
    """
    Save an intent in the database.
    """
    intent = request.form.get('intent')
    script_name = request.form.get('script_name')
    seq_id = request.form.get('sequence_id')
    if not intent or ' ' in intent:
        return 'Un nom d\'intention ne doit pas être vide ou contenir d\'espace.', 400
    if ' ' in script_name:
        return 'Un nom de script ne doit pas contenir d\'espace.', 400
    if Intent.query.filter_by(intent=intent).first() is not None:
	    return 'Une intention portant le même nom existe déjà.', 400
    if script_name and script_name not in resources.getScripts():
        return 'Le script spécifié n\'existe pas.', 400
    logging.info('Saving intent \'' + intent + '\'')
    db_intent = Intent(intent=intent, script_name=script_name, sequence_id=seq_id, enabled=True)
    db.session.merge(db_intent)
    db.session.commit()
    return speech.render_page('speech.html')

@speech.route('/enable_intent', methods=['POST'])
@login_required
def enable_intent():
    intent = request.form.get('intent')
    value = json.loads(request.form.get('value'))
    if not intent or ' ' in intent:
        return 'Une intention ne doit pas être vide ou contenir d\'espace.', 400
    logging.info('Updating intent \'' + intent + '\'')
    db_intent = Intent.query.filter_by(intent=intent).first()
    db_intent.enabled = value
    db.session.commit()
    return speech.render_page('speech.html')

@speech.route('/delete_intent', methods=['POST'])
@login_required
def delete_intent():
    intent = request.form.get('intent')
    if not intent or ' ' in intent:
        return 'Une intention ne doit pas être vide ou contenir d\'espace.', 400
    logging.info('Deleting intent \'' + intent + '\'')
    db_intent = Intent.query.filter_by(intent=intent).first()
    db.session.delete(db_intent)
    db.session.commit()
    return speech.render_page('speech.html')
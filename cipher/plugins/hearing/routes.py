import json
import re
import threading
from flask import Flask, session, request, jsonify
from . import hearing
from .model import Intent
from cipher.model import Sequence, db, resources
from cipher.security import login_required

@hearing.route('/hearing')
@login_required
def hearing_page():
    sequences = Sequence.query.all()
    intents = Intent.query.all()
    return hearing.render_page('hearing.html', sequences=sequences, intents=intents)


@hearing.route('/save_intent', methods=['POST'])
@login_required
def save_intent():
    """
    Save an intent in the database.
    """
    intent = request.json.get('intent')
    script_name = request.json.get('script_name')
    seq_id = request.json.get('sequence_id')
    if not intent or ' ' in intent:
        return jsonify("Un nom d'intention ne doit pas être vide ou contenir d'espace."), 400
    if ' ' in script_name:
        return jsonify("Un nom de script ne doit pas contenir d'espace."), 400
    if Intent.query.filter_by(intent=intent).first() is not None:
        return jsonify("Une intention portant le même nom existe déjà."), 400
    hearing.log.info("Saving intent '%s'", intent)
    db_intent = Intent(intent=intent, sequence_id=seq_id, enabled=True)
    db.session.merge(db_intent)
    db.session.commit()
    return jsonify("L'intention '" + intent + "' a été sauvegardée avec succès."), 200


@hearing.route('/enable_intent', methods=['POST'])
@login_required
def enable_intent():
    intent = request.json.get('intent')
    value = request.json.get('value')
    if not intent or ' ' in intent:
        return jsonify("Une intention ne doit pas être vide ou contenir d'espace."), 400
    hearing.log.info("Updating intent '" + intent + "'")
    db_intent = Intent.query.filter_by(intent=intent).first()
    db_intent.enabled = value
    db.session.commit()
    return jsonify("L'état de l'intention '" + intent + "' a été modifié."), 200


@hearing.route('/delete_intent', methods=['POST'])
@login_required
def delete_intent():
    intent = request.json.get('intent')
    if not intent or ' ' in intent:
        return jsonify("Une intention ne doit pas être vide ou contenir d'espace."), 400
    hearing.log.info("Deleting intent '" + intent + "'")
    db_intent = Intent.query.filter_by(intent=intent).first()
    db.session.delete(db_intent)
    db.session.commit()
    return jsonify("L'intention '" + intent + "' a été supprimée avec succès."), 200

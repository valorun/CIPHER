import logging
from flask import Flask, session, request, redirect, jsonify
import json
from . import sequences
from cipher.model import Sequence, Servo, Relay, db
from cipher.security import login_required
from cipher.model import resources
from cipher.core.sequence_reader import sequence_reader

@sequences.route('/sequences')
@login_required
def sequences_page():
    relays=Relay.query.all()
    sequences_list=Sequence.query.all()
    servos=Servo.query.all()
    sounds=resources.getSounds()
    scripts=resources.getScripts()
    return sequences.render_page('sequences.html', sequences=sequences_list, servos=servos, relays=relays, sounds=sounds, scripts=scripts)

@sequences.route('/save_sequence', methods=['POST'])
@login_required
def save_sequence():
    """
    Save a sequence in the database.
    """
    seq_name = request.json.get('seq_name')
    seq_data = request.json.get('seq_data')
    if not seq_name or ' ' in seq_name:
        return jsonify("Un nom de séquence ne doit pas être vide ou contenir d'espace."), 400
    if seq_data is None:
        return jsonify("La séquence est vide."), 400
    if Sequence.query.filter_by(id=seq_name).first() is not None:
	    return jsonify("Une sequence portant le même nom existe déjà."), 400
    sequence = sequence_reader.getSequenceFromJson(seq_data)
    if sequence is not None and not sequence.isValid():
        return jsonify("La séquence n'est pas valide."), 400
    logging.info("Saving sequence '" + seq_name + "'")
    db_sequence = Sequence(id=seq_name, value=json.dumps(seq_data), enabled=True)
    db.session.merge(db_sequence)
    db.session.commit()
    return redirect('/sequences')

@sequences.route('/enable_sequence', methods=['POST'])
@login_required
def enable_sequence():
    """
    Enable or disable a equence stored in the database.
    """
    seq_name = request.json.get('seq_name')
    value = request.json.get('value')
    if not seq_name or ' ' in seq_name:
        return jsonify("Un nom de séquence ne doit pas être vide ou contenir d'espace."), 400
    logging.info("Updating '" + seq_name + "'")
    db_seq = Sequence.query.filter_by(id=seq_name).first()
    if db_seq is None:
        return jsonify("La séquence est inconnue."), 400
    db_seq.enabled = value
    db.session.commit()
    return redirect('/sequences')

@sequences.route('/delete_sequence', methods=['POST'])
@login_required
def delete_sequence():
    """
    Delete a sequence stored in the database.
    """
    seq_name = request.json.get('seq_name')
    if not seq_name or ' ' in seq_name:
        return jsonify("Un nom de séquence ne doit pas être vide ou contenir d'espace."), 400
    logging.info("Deleting " + seq_name + "'")
    db_seq = Sequence.query.filter_by(id=seq_name).first()
    if db_seq is None:
        return jsonify("La séquence est inconnue."), 400
    db.session.delete(db_seq)
    db.session.commit()
    return redirect('/sequences')

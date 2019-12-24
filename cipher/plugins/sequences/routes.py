import logging
from flask import Flask, session, request, jsonify
import json
from . import sequences
from cipher.model import Sequence, Servo, Relay, db
from cipher.security import login_required
from cipher.model import resources
from cipher.core.sequence_reader import sequence_reader


@sequences.route('/sequences')
@login_required
def sequences_page():
    relays = Relay.query.all()
    sequences_list = Sequence.query.all()
    servos = Servo.query.all()
    sounds = resources.getSounds()
    scripts = resources.getScripts()
    return sequences.render_page('sequences.html', sequences=sequences_list, servos=servos, relays=relays, sounds=sounds, scripts=scripts)


@sequences.route('/save_sequence', methods=['POST'])
@login_required
def save_sequence():
    """
    Save a sequence in the database.
    """
    seqName = request.json.get('seq_name')
    seqData = request.json.get('seq_data')
    if not seqName or ' ' in seqName:
        return jsonify("Un nom de séquence ne doit pas être vide ou contenir d'espace."), 400
    if seqData is None:
        return jsonify("La séquence est vide."), 400
    if Sequence.query.filter_by(id=seqName).first() is not None:
        return jsonify("Une sequence portant le même nom existe déjà."), 400
    sequence = sequence_reader.getSequenceFromJson(seqData)
    if sequence is None:
        return jsonify("La séquence n'est pas valide."), 400
    logging.info("Saving sequence '" + seqName + "'")
    dbSequence = Sequence(id=seqName, value=json.dumps(seqData), enabled=True)
    db.session.merge(dbSequence)
    db.session.commit()
    return jsonify("La séquence '" + seqName + "' a été sauvegardée avec succès."), 200


@sequences.route('/enable_sequence', methods=['POST'])
@login_required
def enable_sequence():
    """
    Enable or disable a equence stored in the database.
    """
    seqName = request.json.get('seq_name')
    value = request.json.get('value')
    if not seqName or ' ' in seqName:
        return jsonify("Un nom de séquence ne doit pas être vide ou contenir d'espace."), 400
    logging.info("Updating '" + seqName + "'")
    dbSeq = Sequence.query.filter_by(id=seqName).first()
    if dbSeq is None:
        return jsonify("La séquence est inconnue."), 400
    dbSeq.enabled = value
    db.session.commit()
    return jsonify("L'état de la séquence '" + seqName + "' a été modifié."), 200


@sequences.route('/delete_sequence', methods=['POST'])
@login_required
def delete_sequence():
    """
    Delete a sequence stored in the database.
    """
    seqName = request.json.get('seq_name')
    if not seqName or ' ' in seqName:
        return jsonify("Un nom de séquence ne doit pas être vide ou contenir d'espace."), 400
    logging.info("Deleting " + seqName + "'")
    dbSeq = Sequence.query.filter_by(id=seqName).first()
    if dbSeq is None:
        return jsonify("La séquence est inconnue."), 400
    db.session.delete(dbSeq)
    db.session.commit()
    return jsonify("La séquence '" + seqName + "' a été supprimée avec succès."), 200

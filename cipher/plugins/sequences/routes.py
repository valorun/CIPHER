from flask import Flask, session, request, jsonify
import json
from . import sequences
from cipher.model import Sequence, db, resources
from cipher.security import login_required
from cipher.core.sequence_reader import sequence_reader
from cipher.core.actions import CUSTOM_ACTIONS, DEFAULT_ACTIONS

@sequences.route('/sequences')
@login_required
def sequences_page():
    sequences_list = Sequence.query.all()
    actions = {}
    actions.update(DEFAULT_ACTIONS)
    actions.update(CUSTOM_ACTIONS)
    return sequences.render_page('sequences.html', sequences=sequences_list, actions=actions)


@sequences.route('/save_sequence', methods=['POST'])
@login_required
def save_sequence():
    """
    Save a sequence in the database.
    """
    seq_name = request.json.get('seq_name')
    seq_data = request.json.get('seq_data')
    seq_overwrite = request.json.get('seq_overwrite')
    if not seq_name or ' ' in seq_name:
        return jsonify("Un nom de séquence ne doit pas être vide ou contenir d'espace."), 400
    if seq_data is None:
        return jsonify("La séquence est vide."), 400
    if Sequence.query.filter_by(id=seq_name).first() is not None and not seq_overwrite:
        return jsonify("Une séquence portant le même nom existe déjà."), 409
    sequence = sequence_reader.get_sequence_from_json(seq_data)
    if sequence is None:
        return jsonify("La séquence n'est pas valide."), 400
    sequences.log.info("Saving sequence '" + seq_name + "'")
    db_sequence = Sequence(id=seq_name, value=json.dumps(seq_data), enabled=True)
    db.session.merge(db_sequence)
    db.session.commit()
    return jsonify("La séquence '" + seq_name + "' a été sauvegardée avec succès."), 200


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
    sequences.log.info("Updating '" + seq_name + "'")
    db_seq = Sequence.query.filter_by(id=seq_name).first()
    if db_seq is None:
        return jsonify("La séquence est inconnue."), 400
    db_seq.enabled = value
    db.session.commit()
    return jsonify("L'état de la séquence '" + seq_name + "' a été modifié."), 200


@sequences.route('/delete_sequence', methods=['POST'])
@login_required
def delete_sequence():
    """
    Delete a sequence stored in the database.
    """
    seq_name = request.json.get('seq_name')
    if not seq_name or ' ' in seq_name:
        return jsonify("Un nom de séquence ne doit pas être vide ou contenir d'espace."), 400
    sequences.log.info("Deleting " + seq_name + "'")
    db_seq = Sequence.query.filter_by(id=seq_name).first()
    if db_seq is None:
        return jsonify("La séquence est inconnue."), 400
    db.session.delete(db_seq)
    db.session.commit()
    return jsonify("La séquence '" + seq_name + "' a été supprimée avec succès."), 200


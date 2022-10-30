from flask import Flask, session, request, jsonify
import json
from . import sequences
from cipher.model import Sequence, db, resources, Trigger
from cipher.security import login_required
from cipher.core.sequence_reader import sequence_reader
from cipher.core.actions import CUSTOM_ACTIONS, DEFAULT_ACTIONS
from cipher.core.triggers import registered_triggers

@sequences.route('/sequences')
@login_required
def sequences_page():
    sequences_list = Sequence.query.all()
    triggers_list = Trigger.query.all()
    actions = {}
    actions.update(DEFAULT_ACTIONS)
    actions.update(CUSTOM_ACTIONS)
    return sequences.render_page('sequences.html', sequences=sequences_list, actions=actions, registered_triggers=registered_triggers, triggers=triggers_list)


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



### Triggers ###
@sequences.route('/save_trigger', methods=['POST'])
@login_required
def save_trigger():
    """
    Save a trigger in the database.
    """
    trigger = request.json.get('trigger_name')
    seq_id = request.json.get('sequence_id')
    overwrite = request.json.get('overwrite')
    if not trigger or ' ' in trigger:
        return jsonify("Un nom de déclencheur ne doit pas être vide ou contenir d'espace."), 400
    if not seq_id or ' ' in seq_id:
        return jsonify("Un nom de séquence ne doit pas être vide ou contenir d'espace."), 400
    if Trigger.query.filter_by(trigger_name=trigger, sequence_id=seq_id).first() is not None and not overwrite:
        return jsonify("Un déclencheur portant le même nom existe déjà."), 409
    sequences.log.info(f"Saving trigger '{trigger} - {seq_id}'")
    db_trigger = Trigger(trigger_name=trigger, sequence_id=seq_id, enabled=True)
    db.session.merge(db_trigger)
    db.session.commit()
    return jsonify(f"Le déclencheur '{trigger}' associé à la séquence '{seq_id}' a été sauvegardée avec succès."), 200


@sequences.route('/enable_trigger', methods=['POST'])
@login_required
def enable_trigger():
    trigger = request.json.get('trigger_name')
    seq_id = request.json.get('sequence_id')
    value = request.json.get('value')
    if not trigger or ' ' in trigger:
        return jsonify("Un déclencheur ne doit pas être vide ou contenir d'espace."), 400
    if not seq_id or ' ' in seq_id:
        return jsonify("Un nom de séquence ne doit pas être vide ou contenir d'espace."), 400
    sequences.log.info(f"Updating trigger '{trigger} - {seq_id}'")
    db_trigger = Trigger.query.filter_by(trigger_name=trigger, sequence_id=seq_id).first()
    db_trigger.enabled = value
    db.session.commit()
    return jsonify(f"L'état du déclencheur '{trigger}' associé à la séquence '{seq_id}' a été modifié."), 200


@sequences.route('/delete_trigger', methods=['POST'])
@login_required
def delete_trigger():
    trigger = request.json.get('trigger_name')
    seq_id = request.json.get('sequence_id')
    if not trigger or ' ' in trigger:
        return jsonify("Un déclencheur ne doit pas être vide ou contenir d'espace."), 400
    if not seq_id or ' ' in seq_id:
        return jsonify("Un nom de séquence ne doit pas être vide ou contenir d'espace."), 400
    sequences.log.info(f"Deleting trigger '{trigger} - {seq_id}'")
    db_trigger = Trigger.query.filter_by(trigger_name=trigger, sequence_id=seq_id).first()
    db.session.delete(db_trigger)
    db.session.commit()
    return jsonify(f"Le déclencheur '{trigger}' associé à la séquence '{seq_id}' a été supprimé avec succès."), 200
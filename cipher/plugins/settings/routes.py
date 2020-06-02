import logging
import json
from flask import Flask, flash, request, session, jsonify
from . import settings
from cipher.model import db, Relay, Servo
from cipher.config import core_config
from cipher.security import login_required


@settings.route('/settings')
@login_required
def settings_page():
    relays = Relay.query.all()
    servos = Servo.query.all()
    camera_url = core_config.get_camera_url() or ''
    audio_on_server = core_config.get_audio_on_server()
    motion_raspi_id = core_config.get_motion_raspi_id() or ''
    enable_motion = core_config.get_enable_motion()
    return settings.render_page('settings.html', relays=relays, servos=servos, camera_url=camera_url, audio_on_server=audio_on_server, motion_raspi_id=motion_raspi_id, enable_motion=enable_motion)


@settings.route('/save_relay', methods=['POST'])
@login_required
def save_relay():
    rel_label = request.json.get('rel_label')
    rel_pin = request.json.get('rel_pin')
    rel_parity = request.json.get('rel_parity')
    raspi_id = request.json.get('raspi_id')
    if not rel_label or ' ' in rel_label:
        return jsonify("Un label de relai ne doit pas être vide ou contenir d'espace."), 400
    if not rel_pin or ' ' in rel_pin:
        return jsonify("Un pin ne doit pas être vide ou contenir d'espace."), 400
    if ' ' in rel_parity:
        return jsonify("Une parité ne doit pas contenir d'espace."), 400
    if not raspi_id or ' ' in raspi_id:
        return jsonify("Un id de raspberry ne doit pas être vide ou contenir d'espace."), 400
    if Relay.query.filter_by(label=rel_label).first() is not None:
        return jsonify("Un relai portant le même label existe déjà."), 400
    logging.info("Saving relay " + rel_label)
    db_relay = Relay(label=rel_label, pin=rel_pin, enabled=True, parity=rel_parity, raspi_id=raspi_id)
    db.session.add(db_relay)
    db.session.commit()
    return jsonify("Le relai '" + rel_label + "' a été sauvegardé avec succès."), 200


@settings.route('/enable_relay', methods=['POST'])
@login_required
def enable_relay():
    rel_label = request.json.get('rel_label')
    value = request.json.get('value')
    if not rel_label or ' ' in rel_label:
        return jsonify("Un label de relai ne doit pas être vide ou contenir d'espace."), 400
    logging.info("Updating relay " + rel_label)
    db_rel = Relay.query.filter_by(label=rel_label).first()
    if db_rel is None:
        return jsonify("Le relai est inconnu."), 400
    db_rel.enabled = value
    db.session.commit()
    return jsonify("L'état du relai '" + rel_label + "' a été modifié."), 200


@settings.route('/delete_relay', methods=['POST'])
@login_required
def delete_relay():
    rel_label = request.json.get("rel_label")
    if not rel_label or ' ' in rel_label:
        return jsonify("Un label de relai ne doit pas être vide ou contenir d'espace."), 400
    logging.info("Deleting relay " + rel_label)
    db_rel = Relay.query.filter_by(label=rel_label).first()
    if db_rel is None:
        return jsonify("Le relai est inconnu."), 400
    db.session.delete(db_rel)
    db.session.commit()
    return jsonify("Le relai '" + rel_label + "' a été supprimé avec succès."), 200


@settings.route('/save_servo', methods=['POST'])
@login_required
def save_servo():
    servo_label = request.json.get('servo_label')
    servo_pin = request.json.get('servo_pin')
    raspi_id = request.json.get('raspi_id')
    servo_min_pulse_width = int(request.json.get('min_pulse_width'))
    servo_max_pulse_width = int(request.json.get('max_pulse_width'))
    servo_def_pulse_width = int(request.json.get('def_pulse_width'))

    if not servo_label or ' ' in servo_label:
        return jsonify("Un label de servo moteur ne doit pas être vide ou contenir d'espace."), 400
    if not servo_pin or ' ' in servo_pin:
        return jsonify("Un pin ne doit pas être vide ou contenir d'espace."), 400
    if not servo_min_pulse_width:
        return jsonify("La largeur d'impulsion minimale n'est pas valide."), 400
    if not servo_max_pulse_width:
        return jsonify("La largeur d'impulsion maximale n'est pas valide."), 400
    if not servo_def_pulse_width:
        return jsonify("La largeur d'impulsion par défaut n'est pas valide."), 400
    if servo_min_pulse_width > servo_max_pulse_width:
        return jsonify("La largeur d'impulsion minimum doit être inférieure à la largeur d'impulsion maximum"), 400
    if servo_def_pulse_width < servo_min_pulse_width or servo_def_pulse_width > servo_max_pulse_width:
        return jsonify("La largeur d'impulsion par défaut doit être comprise entre son minimum et son maximum."), 400
    if not raspi_id or ' ' in raspi_id:
        return jsonify("Un id de raspberry ne doit pas être vide ou contenir d'espace."), 400
    if Servo.query.filter_by(label=servo_label).first() is not None:
        return jsonify("Un servomoteur portant le même label existe déjà."), 400
    logging.info("Saving servo '" + servo_label + "'")
    db_servo = Servo(label=servo_label, pin=servo_pin, enabled=True, min_pulse_width=servo_min_pulse_width, max_pulse_width=servo_max_pulse_width, def_pulse_width=servo_def_pulse_width, raspi_id=raspi_id)
    db.session.add(db_servo)
    db.session.commit()
    return jsonify("Le servo moteur '" + servo_label + "' a été sauvegardé avec succès."), 200


@settings.route('/enable_servo', methods=['POST'])
@login_required
def enable_servo():
    servo_label = request.json.get('servo_label')
    value = request.json.get('value')
    if not servo_label or ' ' in servo_label:
        return jsonify("Un label de servomoteur ne doit pas être vide ou contenir d'espace."), 400
    logging.info("Updating servo " + servo_label)
    db_servo = Servo.query.filter_by(label=servo_label).first()
    if db_servo is None:
        return jsonify("Le servomoteur est inconnu."), 400
    db_servo.enabled = value
    db.session.commit()
    return jsonify("L'état du servo moteur '" + servo_label + "' a été modifié."), 200


@settings.route('/delete_servo', methods=['POST'])
@login_required
def delete_servo():
    servo_label = request.json.get('servo_label')
    if not servo_label or ' ' in servo_label:
        return jsonify("Un label de servomoteur ne doit pas être vide ou contenir d'espace."), 400
    logging.info("Deleting servo " + servo_label)
    db_servo = Servo.query.filter_by(label=servo_label).first()
    if db_servo is None:
        return jsonify("Le servomoteur est inconnu."), 400
    db.session.delete(db_servo)
    db.session.commit()
    return jsonify("Le servo moteur '" + servo_label + "' a été supprimé avec succès."), 200


@settings.route('/update_camera_url', methods=['POST'])
@login_required
def update_camera_url():
    url = request.json.get('camera_url')
    if url and ' ' in url:  # if the string is empty, update is accepted
        return jsonify("L'url ne doit pas contenir d'espace."), 400
    logging.info("Updating camera URL: " + url)
    core_config.set_camera_url(url)
    return jsonify("L'URL de la caméra a été mis à jour."), 200


@settings.route('/update_audio_source', methods=['POST'])
@login_required
def update_audio_source():
    value = request.json.get('value')
    logging.info("Updating audio source: " + str(value))
    core_config.set_audio_on_server(value)
    if value:
        response = "Le son sur le serveur a été activé."
    else:
        response = "Le son sur le serveur a été désactivé."
    return jsonify(response), 200


@settings.route('/get_audio_source', methods=['POST'])
@login_required
def get_audio_mode():
    return jsonify(core_config.get_audio_on_server())


@settings.route('/update_motion_raspi_id', methods=['POST'])
@login_required
def update_motion_raspi_id():
    id = request.json.get('raspi_id')
    logging.info("Updating motion raspi id: " + id)
    core_config.set_motion_raspi_id(id)
    return jsonify("L\'id du raspberry chargé des déplacements a été mis à jour."), 200

@settings.route('/update_enable_motion', methods=['POST'])
@login_required
def update_enable_motion():
    value = request.json.get('value')
    logging.info("Updating enable motion: " + str(value))
    core_config.set_audio_on_server(value)
    if value:
        response = "Les déplacement ont été activés."
    else:
        response = "Les déplacements ont été désactivés."
    return jsonify(response), 200

@settings.route('/update_robot_name', methods=['POST'])
@login_required
def update_robot_name():
    name = request.json.get('robot_name')
    logging.info("Updating robot name: " + name)
    core_config.set_robot_name(name)
    return jsonify("Le nom du robot a été mis à jour."), 200

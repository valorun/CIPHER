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
    label = request.json.get('label')
    pin = request.json.get('pin')
    parity = request.json.get('parity')
    raspi_id = request.json.get('raspi_id')
    if not label or ' ' in label:
        return jsonify("Un label de relai ne doit pas être vide ou contenir d'espace."), 400
    if not pin or ' ' in pin:
        return jsonify("Un pin ne doit pas être vide ou contenir d'espace."), 400
    if ' ' in parity:
        return jsonify("Une parité ne doit pas contenir d'espace."), 400
    if not raspi_id or ' ' in raspi_id:
        return jsonify("Un id de raspberry ne doit pas être vide ou contenir d'espace."), 400
    if Relay.query.filter_by(label=label).first() is not None:
        return jsonify("Un relai portant le même label existe déjà."), 400
    settings.log.info("Saving relay " + label)
    db_relay = Relay(label=label, pin=pin, enabled=True, parity=parity, raspi_id=raspi_id)
    db.session.add(db_relay)
    db.session.commit()
    return jsonify("Le relai '" + label + "' a été sauvegardé avec succès."), 200


@settings.route('/update_relay', methods=['POST'])
@login_required
def update_relay():
    label = request.json.get('label')

    if not label or ' ' in label:
        return jsonify("Le label de relai ne doit pas être vide ou contenir d'espace."), 400
    db_relay = Relay.query.filter_by(label=label).first()
    if db_relay is None:
        return jsonify("Le relai est inconnu."), 400
    
    new_label = request.json.get('new_label') or label
    pin = request.json.get('pin') or db_relay.pin
    parity = request.json.get('parity')
    if parity is None:
        parity = db_relay.parity
    raspi_id = request.json.get('raspi_id') or db_relay.raspi_id

    if ' ' in new_label:
        return jsonify("Le nouveau label de relai ne doit pas être vide ou contenir d'espace."), 400
    db_relay.label = new_label
    if ' ' in pin:
        return jsonify("Un pin ne doit pas être vide ou contenir d'espace."), 400
    db_relay.pin = pin
    if ' ' in parity:
        return jsonify("Une parité ne doit pas contenir d'espace."), 400
    db_relay.parity = parity
    if ' ' in raspi_id:
        return jsonify("Un id de raspberry ne doit pas être vide ou contenir d'espace."), 400
    db_relay.raspi_id = raspi_id

    db.session.commit()
    return jsonify("Le relai '" + label + "' a été mis à jour avec succès."), 200


@settings.route('/enable_relay', methods=['POST'])
@login_required
def enable_relay():
    label = request.json.get('label')
    value = request.json.get('value')
    if not label or ' ' in label:
        return jsonify("Un label de relai ne doit pas être vide ou contenir d'espace."), 400
    settings.log.info("Updating relay " + label)
    db_rel = Relay.query.filter_by(label=label).first()
    if db_rel is None:
        return jsonify("Le relai est inconnu."), 400
    db_rel.enabled = value
    db.session.commit()
    return jsonify("L'état du relai '" + label + "' a été modifié avec succès."), 200


@settings.route('/delete_relay', methods=['POST'])
@login_required
def delete_relay():
    label = request.json.get("label")
    if not label or ' ' in label:
        return jsonify("Un label de relai ne doit pas être vide ou contenir d'espace."), 400
    settings.log.info("Deleting relay " + label)
    db_rel = Relay.query.filter_by(label=label).first()
    if db_rel is None:
        return jsonify("Le relai est inconnu."), 400
    db.session.delete(db_rel)
    db.session.commit()
    return jsonify("Le relai '" + label + "' a été supprimé avec succès."), 200


@settings.route('/save_servo', methods=['POST'])
@login_required
def save_servo():
    label = request.json.get('label')
    pin = request.json.get('pin')
    raspi_id = request.json.get('raspi_id')
    min_pulse_width = int(request.json.get('min_pulse_width'))
    max_pulse_width = int(request.json.get('max_pulse_width'))
    def_pulse_width = int(request.json.get('def_pulse_width'))

    if not label or ' ' in label:
        return jsonify("Un label de servo moteur ne doit pas être vide ou contenir d'espace."), 400
    if not pin or ' ' in pin:
        return jsonify("Un pin ne doit pas être vide ou contenir d'espace."), 400
    if not min_pulse_width:
        return jsonify("La largeur d'impulsion minimale n'est pas valide."), 400
    if not max_pulse_width:
        return jsonify("La largeur d'impulsion maximale n'est pas valide."), 400
    if not def_pulse_width:
        return jsonify("La largeur d'impulsion par défaut n'est pas valide."), 400
    if min_pulse_width > max_pulse_width:
        return jsonify("La largeur d'impulsion minimum doit être inférieure à la largeur d'impulsion maximum"), 400
    if def_pulse_width < min_pulse_width or def_pulse_width > max_pulse_width:
        return jsonify("La largeur d'impulsion par défaut doit être comprise entre son minimum et son maximum."), 400
    if not raspi_id or ' ' in raspi_id:
        return jsonify("Un id de raspberry ne doit pas être vide ou contenir d'espace."), 400
    if Servo.query.filter_by(label=label).first() is not None:
        return jsonify("Un servomoteur portant le même label existe déjà."), 400
    settings.log.info("Saving servo '%s'", label)
    db_servo = Servo(label=label, pin=pin, enabled=True, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width, def_pulse_width=def_pulse_width, raspi_id=raspi_id)
    db.session.add(db_servo)
    db.session.commit()
    return jsonify("Le servo moteur '" + label + "' a été sauvegardé avec succès."), 200

@settings.route('/update_servo', methods=['POST'])
@login_required
def update_servo():
    label = request.json.get('label')

    if not label or ' ' in label:
        return jsonify("Le label de servo moteur ne doit pas être vide ou contenir d'espace."), 400

    db_servo = Servo.query.filter_by(label=label).first()
    if db_servo is None:
        return jsonify("Le servomoteur est inconnu."), 400

    new_label = request.json.get('new_label') or label
    pin = request.json.get('pin') or db_servo.pin
    raspi_id = request.json.get('raspi_id') or db_servo.raspi_id
    min_pulse_width = int(request.json.get('min_pulse_width')) or db_servo.min_pulse_width
    max_pulse_width = int(request.json.get('max_pulse_width')) or db_servo.max_pulse_width
    def_pulse_width = int(request.json.get('def_pulse_width')) or db_servo.def_pulse_width

    if ' ' in new_label:
        return jsonify("Le nouveau label de servo moteur ne doit pas contenir d'espace."), 400
    db_servo.label = new_label

    if ' ' in pin:
        return jsonify("Un pin ne doit pas être vide ou contenir d'espace."), 400
    db_servo.pin = pin

    if ' ' in raspi_id:
        return jsonify("Un id de raspberry ne doit pas être vide ou contenir d'espace."), 400
    db_servo.raspi_id = raspi_id

    if min_pulse_width > max_pulse_width:
        return jsonify("La largeur d'impulsion minimum doit être inférieure à la largeur d'impulsion maximum"), 400

    if def_pulse_width < min_pulse_width or def_pulse_width > max_pulse_width:
        return jsonify("La largeur d'impulsion par défaut doit être comprise entre son minimum et son maximum."), 400
    db_servo.min_pulse_width = min_pulse_width
    db_servo.max_pulse_width = max_pulse_width
    db_servo.def_pulse_width = def_pulse_width

    db.session.commit()
    return jsonify("Le servo moteur '" + label + "' a été mis à jour avec succès."), 200
    




@settings.route('/enable_servo', methods=['POST'])
@login_required
def enable_servo():
    label = request.json.get('label')
    value = request.json.get('value')
    if not label or ' ' in label:
        return jsonify("Un label de servomoteur ne doit pas être vide ou contenir d'espace."), 400
    settings.log.info("Updating servo %s", label)
    db_servo = Servo.query.filter_by(label=label).first()
    if db_servo is None:
        return jsonify("Le servomoteur est inconnu."), 400
    db_servo.enabled = value
    db.session.commit()
    return jsonify("L'état du servo moteur '" + label + "' a été modifié."), 200


@settings.route('/delete_servo', methods=['POST'])
@login_required
def delete_servo():
    label = request.json.get('label')
    if not label or ' ' in label:
        return jsonify("Un label de servomoteur ne doit pas être vide ou contenir d'espace."), 400
    settings.log.info("Deleting servo %s", label)
    db_servo = Servo.query.filter_by(label=label).first()
    if db_servo is None:
        return jsonify("Le servomoteur est inconnu."), 400
    db.session.delete(db_servo)
    db.session.commit()
    return jsonify("Le servo moteur '" + label + "' a été supprimé avec succès."), 200


@settings.route('/update_camera_url', methods=['POST'])
@login_required
def update_camera_url():
    url = request.json.get('camera_url')
    if url and ' ' in url:  # if the string is empty, update is accepted
        return jsonify("L'url ne doit pas contenir d'espace."), 400
    settings.log.info("Updating camera URL: %s", url)
    core_config.set_camera_url(url)
    return jsonify("L'URL de la caméra a été mis à jour."), 200


@settings.route('/update_audio_source', methods=['POST'])
@login_required
def update_audio_source():
    value = request.json.get('value')
    settings.log.info("Updating audio source: %s", str(value))
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
    settings.log.info("Updating motion raspi id: " + id)
    core_config.set_motion_raspi_id(id)
    return jsonify("L\'id du raspberry chargé des déplacements a été mis à jour."), 200

@settings.route('/update_enable_motion', methods=['POST'])
@login_required
def update_enable_motion():
    value = request.json.get('value')
    settings.log.info("Updating enable motion: " + str(value))
    core_config.set_enable_motion(value)
    if value:
        response = "Les déplacement ont été activés."
    else:
        response = "Les déplacements ont été désactivés."
    return jsonify(response), 200

@settings.route('/update_robot_name', methods=['POST'])
@login_required
def update_robot_name():
    name = request.json.get('robot_name')
    settings.log.info("Updating robot name: " + name)
    core_config.set_robot_name(name)
    return jsonify("Le nom du robot a été mis à jour."), 200

from flask import Flask, request, Response, render_template, flash, send_from_directory, jsonify
from os.path import join
from . import core
from cipher.config import core_config
from cipher.security import login_required
from cipher.core.actions import Action
from cipher.model import Sequence

@core.app_errorhandler(400)
def invalid_page(e):
    return render_template('error.html', error_code=400, error_message="La requête est invalide"), 400


@core.app_errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Cette page n'existe pas"), 404


@core.app_errorhandler(405)
def method_not_allowed(e):
    return render_template('error.html', error_code=405, error_message="Cette page n'existe pas"), 405

#@core.app_errorhandler(Exception)
#def unhandled_exception(e):
#	core.log.error(e)
#	return jsonify("Une erreur imprévue est survenue."), 500


@core.route('/play_sound/<sound_name>', methods=['GET'])
@login_required
def play_sound(sound_name):
    """
    Stream the specified sound to the client.
    """
    def generate():
        with open(join(core_config.SOUNDS_LOCATION, sound_name), 'rb') as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype='audio/x-wav')

@core.route('/check_action_parameters', methods=['POST'])
def check_action_parameters():
    name = request.json.get('action_name')
    parameters = request.json.get('parameters')
    return jsonify(Action.get_from_name(name).check_parameters(**parameters)), 200

@core.route('/check_sequence', methods=['POST'])
def check_sequence():
    name = request.json.get('name')
    if Sequence.query.filter_by(id=name).first() is None:
        return jsonify((False, 'Unknown sequence \'' + str(name) + '\'.')), 200
    else:
        return jsonify((True, None)), 200

@core.route('/favicon.ico')
def favicon():
    return send_from_directory(join(core.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

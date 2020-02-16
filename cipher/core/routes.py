import logging
from flask import Flask, Response, render_template, flash, send_from_directory, jsonify
from os.path import join
from . import core
from cipher.model import config
from cipher.security import login_required


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
#	logging.error(e)
#	return jsonify("Une erreur imprévue est survenue."), 500


@core.route('/play_sound/<sound_name>', methods=['GET'])
@login_required
def play_sound(sound_name):
    """
    Stream the specified sound to the client.
    """
    def generate():
        with open(join(config.get_sounds_location(), sound_name), 'rb') as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype='audio/x-wav')


@core.route('/favicon.ico')
def favicon():
    return send_from_directory(join(core.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

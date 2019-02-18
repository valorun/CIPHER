import logging
from flask import Flask, Response, flash, send_from_directory
from os.path import join
from . import core
from app.constants import SOUNDS_LOCATION
from app.security import login_required

@core.errorhandler(400)
def invalid_page(e):
    return "La requête est invalide", 400

@core.errorhandler(404)
def page_not_found(e):
    return "Cette page n'existe pas", 404

@core.errorhandler(405)
def method_not_allowed(e):
    return "Cette page n'existe pas", 405


@core.route("/play_sound/<sound_name>", methods=['GET'])
@login_required
def play_sound(sound_name):
    """
    Stream the specified sound to the client.
    """
    def generate():
        with open(join(SOUNDS_LOCATION,sound_name), "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype="audio/x-wav")

@core.route('/favicon.ico')
def favicon():
    return send_from_directory(join(core.root_path, 'static'), 'favicon.ico',mimetype='image/vnd.microsoft.icon')
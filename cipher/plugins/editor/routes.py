import logging
import re
from flask import request, jsonify
from cipher.security import login_required
from cipher.model import resources
from . import editor


@editor.route('/editor')
@login_required
def editor_page():
    scripts = resources.get_scripts()
    return editor.render_page('editor.html', scripts=scripts)


@editor.route('/delete_script', methods=['POST'])
@login_required
def delete_script():
    """
    Delete a script stored in the scripts folder.
    """
    script_name = request.json.get('script_name')
    if not script_name or ' ' in script_name:
        return jsonify("Un nom de script ne doit pas être vide ou contenir d'espace."), 400
    logging.info("Deleting " + script_name)
    resources.delete_script(script_name)
    return jsonify("Le script '" + script_name + "' a été supprimé avec succès."), 200


@editor.route('/save_script', methods=['POST'])
@login_required
def save_script():
    """
    Save a script into the scripts folder.
    """
    script_name = request.json.get('script_name')
    logging.info("Saving " + str(script_name))

    script_data = request.json.get('script_data')
    if not script_name or ' ' in script_name:
        return jsonify("Un nom de script ne doit pas être vide ou contenir d'espace."), 400
    logging.info("Saving " + script_name)
    resources.save_script(script_name, script_data)
    return jsonify("Le script '" + script_name + "' a été sauvegardé avec succès."), 200


@editor.route('/read_script/<script_name>', methods=['GET'])
def read_script(script_name):
    """
    Read a script from the scripts folder.
    """
    if not script_name or ' ' in script_name:
        return jsonify("Un nom de script ne doit pas être vide ou contenir d'espace."), 400
    logging.info("Reading " + script_name)
    script_content = resources.read_script(script_name)
    if script_content is None:
        return jsonify("Le script n'existe pas."), 400
    return jsonify(script_content)

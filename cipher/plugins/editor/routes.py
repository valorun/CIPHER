import logging
import re
from flask import request, redirect
from cipher.security import login_required
from cipher.model import resources
from . import editor

@editor.route('/editor')
@login_required
def editor_page():
	scripts=resources.getScripts()
	return editor.render_page('editor.html', scripts=scripts)

@editor.route('/delete_script', methods=['POST'])
@login_required
def delete_script():
	"""
	Delete a script stored in the scripts folder.
	"""
	script_name = request.form.get('script_name')
	if not script_name or ' ' in script_name:
		return 'Un nom de script ne doit pas être vide ou contenir d\'espace.', 400
	logging.info('Deleting ' + script_name)
	resources.deleteScript(script_name)
	return redirect('/editor')

@editor.route('/save_script', methods=['POST'])
@login_required
def save_script():
	"""
	Save a script into the scripts folder.
	"""
	script_name = request.form.get('script_name')
	script_data = request.form.get('script_data')
	if not script_name or ' ' in script_name:
		return 'Un nom de script ne doit pas être vide ou contenir d\'espace.', 400
	logging.info('Saving ' + script_name)
	resources.saveScript(script_name, script_data)
	return redirect('/editor')

@editor.route('/read_script/<script_name>', methods=['GET'])
def read_script(script_name):
	"""
	Read a script from the scripts folder.
	"""
	if not script_name or ' ' in script_name:
		return 'Un nom de script ne doit pas être vide ou contenir d\'espace.', 400
	logging.info('Reading ' + script_name)
	return resources.readScript(script_name)

import logging
from . import debug
from cipher.model import Servo



@debug.route('/debug')
def debug_page():
	servos = Servo.query.filter_by(enabled=True).all()

	return debug.render_page('debug.html', servos=servos)
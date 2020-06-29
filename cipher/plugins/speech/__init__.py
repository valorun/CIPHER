from cipher.plugins import Plugin

speech = Plugin('speech', __name__, 'Actions vocales', 'fa-comments')

from . import routes, model, speech_recognizer
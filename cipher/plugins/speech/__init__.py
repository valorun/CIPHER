from cipher.plugins import Plugin

speech = Plugin('speech', __name__, 'Synthèse vocale', 'fa-comment')

from . import routes, events, config
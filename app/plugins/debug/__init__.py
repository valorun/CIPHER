from app.plugins import Plugin

debug = Plugin('debug', __name__, 'Panneau de debug', 'fa-bug')

from . import routes

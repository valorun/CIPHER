from cipher.plugins import Plugin

sequences = Plugin('sequences', __name__, 'Gestion des sequences', 'fa-project-diagram')

from . import routes

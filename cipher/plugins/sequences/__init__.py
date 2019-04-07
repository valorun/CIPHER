from cipher.plugins import Plugin

sequences = Plugin('sequences', __name__, 'Gestion des séquences', 'fa-project-diagram')

from . import routes

from cipher.plugins import Plugin

hearing = Plugin('hearing', __name__, 'Actions vocales', 'fa-comments')

from . import routes, model, events
from cipher.plugins import Plugin

editor = Plugin('editor', __name__, 'Editeur de scripts', 'fa-edit')

from . import routes

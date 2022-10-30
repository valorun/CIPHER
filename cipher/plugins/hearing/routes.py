from flask import Flask
from . import hearing
from .model import chat_queue
from cipher.core.triggers import registered_triggers
from cipher.security import login_required

@hearing.route('/hearing')
@login_required
def hearing_page():
    triggers = [t for t in registered_triggers if t.startswith('intent_')]
    return hearing.render_page('hearing.html', chat_records=list(chat_queue), intents=triggers)
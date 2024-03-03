from flask import Flask
from . import hearing
from .model import chat_queue
from cipher.security import login_required

@hearing.route('/hearing')
@login_required
def hearing_page():
    return hearing.render_page('hearing.html', chat_records=list(chat_queue))

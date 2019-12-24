from cipher.model import db


class UserCommandPanel(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    grid = db.Column(db.String(50))

from cipher.model import db


class Intent(db.Model):
    intent = db.Column(db.String(50), primary_key=True)
    sequence_id = db.Column(db.String(50), db.ForeignKey('sequence.id'), nullable=True)
    action_name = db.Column(db.String(50), nullable=True)
    enabled = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Intent %r>' % self.intent

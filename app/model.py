from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Sequence(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.Text, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Sequence %r>' % self.id

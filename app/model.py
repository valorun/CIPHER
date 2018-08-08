from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

db = SQLAlchemy()
#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'server_data.db')
#db = SQLAlchemy(app)


class Sequence(db.Model):
	id = db.Column(db.String(50), primary_key=True)
	value = db.Column(db.Text, nullable=False)
	enabled = db.Column(db.Boolean, nullable=False)

	def __repr__(self):
		return '<Sequence %r>' % self.id

class Relay(db.Model):
	label = db.Column(db.String(50), primary_key=True)
	pin = db.Column(db.String(4), nullable=False)
	enabled = db.Column(db.Boolean, nullable=False)
	parity = db.Column(db.String(20), nullable=False)
	
	def __repr__(self):
		return '<Relay %r : >' % self.id

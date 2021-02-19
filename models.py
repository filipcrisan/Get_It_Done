from flask_login import UserMixin
from app import db
from datetime import datetime

# change --> flask db migrate --> flask db upgrade

user_project = db.Table('user_project',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)

	# personal info
	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	re_pass = db.Column(db.String(100))

	tasks = db.relationship('Task', backref='assigned_to')

class Project(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True)
	description = db.Column(db.String(200))
	creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	created_on = db.Column(db.DateTime)
	tasks = db.relationship('Task', backref='in_project')
	users = db.relationship('User', secondary=user_project, backref=db.backref('assigned_projects', lazy='dynamic'))

class Task(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(200))
	state = db.Column(db.String(100))
	priority = db.Column(db.String(100))
	in_project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
	assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
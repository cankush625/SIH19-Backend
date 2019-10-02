from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class Admin(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200))
	email = db.Column(db.String(120), unique=True, nullable=False, index=True)
	phone_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
	password_hash = db.Column(db.String(128), nullable=False)
	role = db.Column(db.String(10), default='admin')
	websites = db.relationship('Website', backref='admin', lazy='dynamic')

	def __repr__(self):
		return f'<User {self.name}>'

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class Website(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False)
	url = db.Column(db.String(150), unique=True, nullable=False, index=True)
	http_status_code = db.Column(db.Integer, default=200)
	message_sent = db.Column(db.Boolean, default=False)
	remark = db.Column(db.String(200), default='N/A', nullable=False)
	approved = db.Column(db.Boolean, default=False)
	verification_doc_url = db.Column(db.String())
	admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

	def __repr__(self):
		return f'<Website {self.name}>'

@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))
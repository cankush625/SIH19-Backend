from flask import render_template, url_for, flash, redirect, request
from werkzeug.urls import url_parse
from app import app
from app.forms import RegistrationForm, LoginForm, WebsiteForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Admin, Website
from app import db, get_celery
import requests
from celery import uuid


celery = get_celery()

@celery.task(name="tasks.urltest")
def urltest(url):
    r = requests.get(url)
    return r.status_code

@app.route('/')
@app.route('/index/')
@app.route('/home/')
def index():
	websites = Website.query.filter_by(approved=True)
	return render_template('index.html', title='Home', websites=websites)


@app.route('/login/', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = Admin.query.filter_by(email=form.email.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		if current_user.role == 'superadmin':
			return redirect(url_for('superadmin'))
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title="Login", form=form)


@app.route("/register/", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		if Admin.query.all() == None:
			role = 'superadmin'
		else:
			role = 'admin'
		user = Admin(name=form.name.data, email=form.email.data, phone_number=form.phone_number.data, role=role)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash(f'Account created for { form.name.data }!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title="Register", form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/website/add", methods=['GET', 'POST'])
@login_required
def add_website():
	if current_user.role == 'superadmin':
		return "NOT ALLOWED"
	form = WebsiteForm()
	if form.validate_on_submit():
		website = Website(name=form.name.data, url=form.url.data, verification_doc_url=form.verification_doc_url.data, admin=current_user)
		db.session.add(website)
		db.session.commit()
		flash('Your website has been created! Will be listed after super-admin approval.' , 'success')
		return redirect(url_for('index'))
	return render_template('add_website.html', title='Add Website', form=form)



@app.route("/superadmin/", methods=["GET", "POST"])
@login_required
def superadmin():
	if current_user.role != 'superadmin':
		return "NOT ALLOWED"
	websites = Website.query.filter_by(approved=False)
	return render_template('superadmindashboard.html', websites=websites)

@app.route("/approve/")
@login_required
def approve():
	if current_user.role != 'superadmin':
		return "NOT ALLOWED!"
	wid = request.args["wid"]
	website = Website.query.filter_by(id=wid).first()
	website.approved = True
	db.session.commit()
	return redirect(url_for('superadmin'))
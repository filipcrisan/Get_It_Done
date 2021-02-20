"""
    This module handles the authentication process (register & login/out).
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from repository.models import User
from start import db


# create the auth blueprint and then some routes for it, with GET and POST methods
auth = Blueprint('auth', __name__)


# LOGIN ================================================================================================================


@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    if not email or not password:
        flash('Please fill in everything.')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Incorrect username or password, please try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.index'))


# LOGOUT ===============================================================================================================


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# REGISTER =============================================================================================================


@auth.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    return render_template('register.html')


@auth.route('/register', methods=['POST'])
def register_post():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    re_pass = request.form.get('re_pass')

    if not first_name or not last_name or not email or not password or not re_pass:
        flash('Please fill in everything.')
        return redirect(url_for('auth.register'))

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        flash('Email address already exists.')
        return redirect(url_for('auth.register'))

    if password != re_pass:
        flash('You must re-enter the same password.')
        return redirect(url_for('auth.register'))

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=generate_password_hash(password, method='sha256'),
        re_pass=generate_password_hash(password, method='sha256')
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

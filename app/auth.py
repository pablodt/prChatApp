from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import database
from .models import User
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

import re

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif len(username) < 5:
            flash('Username is too short.', category='error')
        elif len(password) < 6:
            flash('Password is too short.', category='error')
        elif invalid_email(email):
            flash('Email is invalid', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
            database.session.add(new_user)
            database.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')

            return redirect(url_for('views.index'))

    return render_template("register.html")


def invalid_email(email):
    pattern = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+$'

    if re.match(pattern, email):
        return False
    else:
        return True


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in!')
                return redirect(url_for('views.index'))
            else:
                flash('Password is incorrect', category='error')
        else:
            flash('Email is incorrect', category='error')

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
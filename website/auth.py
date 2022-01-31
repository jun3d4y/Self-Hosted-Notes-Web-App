from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from .models import User
from .__init__ import db

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login() :
    return render_template("login.html")

@auth.route("/login", methods=["POST"])
def login_post() :
    username = request.form.get('username')
    password = request.form.get('password')
    remember_me = request.form.get('rememberMe')

    if username is not None and username != '' and password is not None and password != "" :
        if remember_me == 'on' :
            remember_me = True
        else :
            remember_me = False

        user = User.query.filter_by(username=username).first()
        if user is not None and check_password_hash(user.password, password) :
            login_user(user, remember=remember_me)

            return redirect(url_for('views.home'))

    return redirect(url_for('auth.login'))

@auth.route("/register")
def register() :
    return render_template("register.html")

@auth.route("/register", methods=["POST"])
def register_post() :

    username = request.form.get("username")
    password = request.form.get("password")
    password_verif = request.form.get("password_verif")

    if User.query.filter_by(username=username).first() is None :
        if password == password_verif and len(password) > 5:
            new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            try:
                db.session.commit()
                return redirect(url_for('auth.login'))
            except:
                db.session.rollback()
                raise

    return render_template("register.html")

@auth.route("/change", methods=["POST"])
@login_required
def change() :
    username = request.form.get("username")
    password = request.form.get("password")
    password_verif = request.form.get("password_verif")
    string_id = request.form.get("string_id")

    if username is not None and password is not None and password_verif is not None and string_id is not None :
        if password == password_verif and len(password)>5 :
            current_user.username = username
            current_user.password = generate_password_hash(password, method='sha256')

            try :
                db.session.commit()
                return redirect(url_for('views.note', string_id=string_id))
            except :
                return redirect(url_for('views.home'))

    return redirect(url_for('views.home'))


@auth.route("/logout")
@login_required
def logout() :
    logout_user()
    return redirect(url_for('views.home'))

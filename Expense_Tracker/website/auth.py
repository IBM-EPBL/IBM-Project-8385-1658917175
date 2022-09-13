from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        rname = request.form.get('rname')
        remail = request.form.get('remail')
        rpassword = request.form.get('rpassword')
        rconfirmpassword = request.form.get('rconfirmpassword')

        user = User.query.filter_by(email=remail).first()

        if user:
            flash('Email already exists!', category='error')
        elif rname != '' and remail != '' and rpassword != '' and rconfirmpassword != '':
            if len(rpassword) < 5 or len(rpassword) > 11:
                flash('Password must be length of 6 to 11 characters', category='error')
            elif rpassword != rconfirmpassword:
                flash('Passwords don\'t match', category='error')
            else:
                # add user database
                new_user = User(name=rname, email=remail, password=generate_password_hash(rpassword, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                flash('Registered Successfully', category='success')
                return redirect(url_for('auth.login'))
    return render_template("register.html", user=current_user)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('lemail')
        password = request.form.get('lpassword')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Email doesn\'t exists!', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
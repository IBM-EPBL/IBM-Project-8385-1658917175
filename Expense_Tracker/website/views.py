from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    return render_template("home.html")

@views.route('/profile')
@login_required
def profile():
    return "<p>Profile Page</p>"

@views.route('/changepassword')
@login_required
def changepassword():
    return "<p>Password Page</p>"
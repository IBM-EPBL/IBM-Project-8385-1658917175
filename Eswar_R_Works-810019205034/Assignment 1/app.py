
from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from __init__   import create_app, db
main = Blueprint('main', __name__)

@main.route('/') 
@main.route('/login')
def index():
    return render_template('login.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
    
@main.route('/about')
def aboutus():
    return render_template('about.html')
 
@main.route('/signup')
def aboutus():
    return render_template('signup.html')

app = create_app() 
if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True
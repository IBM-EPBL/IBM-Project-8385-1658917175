from website import create app
from flask import render_template,request,url_for
app=create_app()
@app.route('/register', methods=['POST'])
def register():
  if request.method=="POST";
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    roll number=request.form.get('roll number')

    return(
        "<div style='background-color: teal; padding:20px;border-radius: 10px; color: white'>"
        "<p>Email: "+email+"</p>"
        "<p>Username: "+username+"</p>"
        "<p>Password: "+password+"</p>"
        "<p>Roll number: "+roll number+"</p>"
        "</div>"
       )
    return render_template('register.html')
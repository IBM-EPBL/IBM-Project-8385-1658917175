from website import create_app
from flask import render_template, request, url_for


app = create_app()

@app.route('/register', methods =["GET", "POST"])
def register():
    if request.method == "POST":
       username = request.form.get("username")
       email = request.form.get("email")
       country = request.form.get("country")
       phone = request.form.get("phone")

       return(
        "<div style='background-color: teal; padding:20px;border-radius: 10px; color: white'>"
        "<p>Username: "+username+"</p>"
        "<p>Email: "+email+"</p>"
        "<p>Phone: "+phone+"</p>"
        "<p>Country: "+country+"</p>"
        "</div>"
       )
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
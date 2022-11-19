from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta 
import re

from flask_db2 import DB2
import ibm_db
import ibm_db_dbi
from sendemail import sendgridmail,sendmail

from sqlalchemy import Integer

app = Flask(__name__)

app.secret_key = 'expensetrackersecretkey'
app.permanent_session_lifetime = timedelta(days=1)

app.config['database'] = 'ibmexpense'
app.config['hostname'] = '0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud'
app.config['port'] = '31198'
app.config['protocol'] = 'tcpip'
app.config['uid'] = 'dxk20137'
app.config['pwd'] = '63ZfdzVa5XDeIuR3'
app.config['security'] = 'SSL'
try:
    mysql = DB2(app)

    conn_str='database=ibmexpense;hostname=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;port=31198;protocol=tcpip;\
            uid=dxk20137;pwd=63ZfdzVa5XDeIuR3;security=SSL'
    ibm_db_conn = ibm_db.connect(conn_str,'','')
        
    print("Database connected without any error !!")
except:
    print("IBM DB Connection error   :     " + DB2.conn_errormsg()) 

#SIGN--UP--OR--REGISTER

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        sql = "SELECT * FROM register WHERE email = ?"
        stmt = ibm_db.prepare(ibm_db_conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        result = ibm_db.execute(stmt)
        print(result)
        account = ibm_db.fetch_row(stmt)
        print(account)

        param = "SELECT * FROM user WHERE email = " + "\'" + email + "\'"
        res = ibm_db.exec_immediate(ibm_db_conn, param)

        if account:
            msg = 'Username already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            sql2 = "INSERT INTO register (username, email,password) VALUES (?, ?, ?)"
            stmt2 = ibm_db.prepare(ibm_db_conn, sql2)
            ibm_db.bind_param(stmt2, 1, username)
            ibm_db.bind_param(stmt2, 2, email)
            ibm_db.bind_param(stmt2, 3, password)
            ibm_db.execute(stmt2)
            msg = 'You have successfully registered !'
        return render_template('signup.html', msg = msg)

#LOGIN--PAGE

@app.route("/signin")
def signin():
    return render_template("login.html")

@app.route('/index')
def index():
    return render_template("homepage.html")

#HOME--PAGE
@app.route('/')
@app.route('/home')
def home():
    if 'user' in session:
        # user = session['user']
        # return f" <h1>{user}</h1>"
        return render_template('home.html', user = session['user'][1])
        # return render_template('home.html')
    else:
        return redirect(url_for('index'))

#log-out
@app.route('/logout')
def logout():
   session.pop('user', None)
   return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
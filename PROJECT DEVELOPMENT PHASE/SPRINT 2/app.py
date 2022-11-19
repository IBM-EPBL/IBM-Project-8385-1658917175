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

@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']
        
        sql = "SELECT * FROM user WHERE username = ? and password = ?"
        stmt = ibm_db.prepare(ibm_db_conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        result = ibm_db.execute(stmt)
        print(result)
        account = ibm_db.fetch_row(stmt)
        print(account)
        
        param = "SELECT * FROM user WHERE email = " + "\'" + email + "\'" + " and password = " + "\'" + password + "\'"
        res = ibm_db.exec_immediate(ibm_db_conn, param)

        if account:
            session['loggedin'] = True
            session['id'] = dictionary["ID"]
            userid = dictionary["ID"]
            session['username'] = dictionary["USERNAME"]
            session['email'] = dictionary["EMAIL"]
           
            return redirect('/home')
        else:
            msg = 'Incorrect username / password !'
        
    return render_template('login.html', msg = msg)

@app.route('/login',methods =['GET', 'POST'])
def login()
    errormsg = ''
     
    if request.method == 'POST' :
        session.permanent = True
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        
        sql = "SELECT * FROM user WHERE email = ? and password = ?"
        stmt = ibm_db.prepare(ibm_db_conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        result = ibm_db.execute(stmt)
        account = ibm_db.fetch_row(stmt)
        print(account)
        
        if account:
            if check_password_hash(account[3], password):
                session['user'] = account
                return redirect(url_for('home'))
            else:
                errormsg = 'Password might be wrong !'
        else:
            errormsg = 'Invalid credentials !'
    return render_template('login.html', errormsg = errormsg)

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

@app.route("/add")
def adding():
    if 'user' in session:
        return render_template('add.html', user = session['user'][1])
    else:
        return redirect(url_for('index'))

@app.route('/addexpense',methods=['GET', 'POST'])
def addexpense():
    
    id = session['user'][2]
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    paymode = request.form['paymode']
    category = request.form['category']
    
    sql = "INSERT INTO expenses (id, date, expensename, amount, paymode, category) VALUES (?, ?, ?, ?, ?, ?)"
    stmt = ibm_db.prepare(ibm_db_conn, sql)
    ibm_db.bind_param(stmt, 1, session['id'])
    ibm_db.bind_param(stmt, 2, p4)
    ibm_db.bind_param(stmt, 3, expensename)
    ibm_db.bind_param(stmt, 4, amount)
    ibm_db.bind_param(stmt, 5, paymode)
    ibm_db.bind_param(stmt, 6, category)
    ibm_db.execute(stmt)
    
    param = "SELECT * FROM expenses WHERE userid = " + str(session['id']) + " AND MONTH(date) = MONTH(current timestamp) AND YEAR(date) = YEAR(current timestamp) ORDER BY date DESC"
    res = ibm_db.exec_immediate(ibm_db_conn, param)
    print(date + " " + expensename + " " + amount + " " + paymode + " " + category)
    
    return redirect("/display")

#DISPLAY---graph 
@app.route("/display")
def display():
    if 'user' in session:
        id = session['user'][2]
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM expenses WHERE user=%s AND date ORDER BY `expenses`.`date` DESC',[id])
        expense = cursor.fetchall()
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM expenses WHERE user=%s AND date ORDER BY `expenses`.`date` DESC',[id])
        expense = cursor.fetchall()

        cursorfood = mysql.connection.cursor()
        cursorfood.execute('SELECT sum(amount) from expenses WHERE category="Food" and user=%s', [id])
        sfood = cursorfood.fetchone()
        if sfood[0] == None:
            sfooddata = 0
        else:
            sfooddata = sfood[0]
        
        cursorentertainment = mysql.connection.cursor()
        cursorentertainment.execute('SELECT sum(amount) from expenses WHERE category="Entertainment" and user=%s', [id])
        sentertainment = cursorentertainment.fetchone()
        if sentertainment[0] == None:
            sentertainmentdata = 0
        else:
            sentertainmentdata = sentertainment[0]
        
        cursorbusiness = mysql.connection.cursor()
        cursorbusiness.execute('SELECT sum(amount) from expenses WHERE category="Business" and user=%s', [id])
        sbusiness = cursorbusiness.fetchone()
        if sbusiness[0] == None:
            sbusinessdata = 0
        else:
            sbusinessdata = sbusiness[0]
        
        cursorrent = mysql.connection.cursor()
        cursorrent.execute('SELECT sum(amount) from expenses WHERE category="Rent" and user=%s', [id])
        srent = cursorrent.fetchone()
        if srent[0] == None:
            srentdata = 0
        else:
            srentdata = srent[0]
        
        cursoremi = mysql.connection.cursor()
        cursoremi.execute('SELECT sum(amount) from expenses WHERE category="EMI" and user=%s', [id])
        semi = cursoremi.fetchone()
        if semi[0] == None:
            semidata = 0
        else:
            semidata = semi[0]
        
        cursorother = mysql.connection.cursor()
        cursorother.execute('SELECT sum(amount) from expenses WHERE category="Other" and user=%s', [id])
        sother = cursorother.fetchone()
        if sother[0] == None:
            sotherdata = 0
        else:
            sotherdata = sother[0]
        
        cursortotal = mysql.connection.cursor()
        cursortotal.execute('SELECT sum(amount) from expenses WHERE user=%s', [id])
        stotal = cursortotal.fetchone()
        if stotal[0] == None:
            stotaldata = 0
        else:
            stotaldata = stotal[0]
        
        return render_template('display.html', user = session['user'][1], expense = expense, sfood = sfooddata, sentertainment = sentertainmentdata, sbusiness = sbusinessdata, srent = srentdata, semi = semidata, sother = sotherdata, stotal = stotaldata)
    else:
        return redirect(url_for('index'))

#delete---the--data
@app.route('/delete/<string:id>', methods = ['POST', 'GET' ])
def delete(id):
     param = "DELETE FROM expenses WHERE  id = " + format.id
     res = ibm_db.exec_immediate(ibm_db_conn, param)
     print('deleted successfully')    
     return redirect("/display")

#UPDATE---DATA
@app.route('/edit/<id>', methods = ['POST', 'GET' ])
def edit(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM expenses WHERE  id = %s', (id,))
    row = cursor.fetchall()
   
    print(row[0])
    return render_template('edit.html', expenses = row[0], user = session['user'][1])

@app.route('/update/<id>', methods = ['POST'])
def update(id):
  if request.method == 'POST' :
   
      date = request.form['date']
      expensename = request.form['expensename']
      amount = request.form['amount']
      paymode = request.form['paymode']
      category = request.form['category']
      
      sql = "UPDATE expenses SET date = ? , expensename = ? , amount = ?, paymode = ?, category = ? WHERE id = ?"
      stmt = ibm_db.prepare(ibm_db_conn, sql)
      ibm_db.bind_param(stmt, 1, p4)
      ibm_db.bind_param(stmt, 2, expensename)
      ibm_db.bind_param(stmt, 3, amount)
      ibm_db.bind_param(stmt, 4, paymode)
      ibm_db.bind_param(stmt, 5, category)
      ibm_db.bind_param(stmt, 6, id)
      ibm_db.execute(stmt)
      
      print('successfully updated')
      return redirect("/display")


#log-out
@app.route('/logout')
def logout():
   session.pop('user', None)
   return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
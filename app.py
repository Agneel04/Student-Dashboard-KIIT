from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "secretkey"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'agneel2004'   
app.config['MYSQL_DB'] = 'user_auth'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = bcrypt.generate_password_hash(
        request.form['password']
    ).decode('utf-8')

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO users(username,email,password) VALUES(%s,%s,%s)",
        (username, email, password)
    )
    mysql.connection.commit()
    cur.close()

    flash("Account created successfully. Please login.", "success")
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT password FROM users WHERE username=%s", (username,))
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.check_password_hash(user[0], password):
        session['user'] = username
        return redirect('/dashboard')
    else:
        flash("Invalid username or password", "danger")
        return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

    cur = mysql.connection.cursor()
    cur.execute("SELECT subject, marks FROM grades")
    grades = cur.fetchall()
    cur.close()

    return render_template('dashboard.html', grades=grades)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    print("USER AUTH APP RUNNING")
    app.run(debug=True)

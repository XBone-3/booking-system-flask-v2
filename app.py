from flask import Flask, flash, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
from wtforms import StringField, EmailField, PasswordField, validators, SelectField, Form
from passlib.hash import sha256_crypt
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.secret_key = SECRET_KEY
PASSWORD = 'fool'.encode()

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "call_me_x"
app.config['MYSQL_PASSWORD'] = PASSWORD.decode()
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'crittle'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/bookslot')
def book_slot():
    return render_template('slots.html')

@app.route('/admin_home')
def admin_home():
    if 'admin' in request.args:
        admin_name = request.args['admin']
        return render_template('admin.html', admin=admin_name)
    return render_template("admin.html")

class LoginForm(Form):
    username = StringField('Username', [validators.length(min=3, max=11), validators.DataRequired()], render_kw={'placeholder':'User Name'})
    password = PasswordField('Password', [validators.length(min=6), validators.DataRequired()], render_kw={'placeholder':'Enter your password'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        user_password = form.password.data
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username=%(user_name)s", {'user_name': username})
        if result > 0:
            data = cur.fetchone()
            name = data['name']
            password = data['user_password']
            uid = data['id']
            admin = data['admin']
            if sha256_crypt.verify(user_password, password):
                session['logged'] = True
                session['uid'] = uid
                session['name'] = name
                session['admin'] = admin
                online = 1
                cur.execute("UPDATE users SET online=%(online_status)s WHERE id=%(user_id)s", {'online_status': online, 'user_id': uid})
                cur.close()
                return redirect(url_for('index'))
            else:
                cur.close()
                return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        admin_password = form.password.data
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM admins WHERE username = %(user_name)s ", {'user_name': username})
        if result > 0:
            data = cur.fetchone()
            password = data['admin_password']
            uid = data['id']
            name = data['name']
            admin = data['admin']
            if sha256_crypt.verify(admin_password, password):
                session['logged'] = True
                session['uid'] = uid
                session['name'] = name
                session['admin'] = admin
                online = 1
                cur.execute("UPDATE admins SET online=%(online_status)s where id=%(admin_id)s", {'admin_id': uid, 'online_status': online})
                cur.close()
                flash("Successfully Logged")
                return redirect(url_for("admin_home", admin=name))
            else:
                cur.close()
                return redirect(url_for('admin_login'))
    return render_template('admin_login.html', form=form)

@app.route('/logout')
def logout():
    if 'uid' in session:
        cur = mysql.connection.cursor()
        online = 0
        uid = session['uid']
        if session['admin'] == 1:
            cur.execute("UPDATE admins SET online=%(online_status)s where id=%(user_id)s", {'user_id': uid, 'online_status': online})
        else:
            cur.execute("UPDATE users SET online=%(online_status)s where id=%(user_id)s", {'user_id': uid, 'online_status': online})
        cur.close()
        session.clear()
    return redirect(url_for('index'))

class RegisterForm(Form):
    name = StringField('Name', [validators.length(min=3, max=15), validators.DataRequired()], render_kw={'autofocus':True, 'placeholder':'Full Name'})
    username = StringField('Username', [validators.length(min=3, max=11), validators.DataRequired()], render_kw={'placeholder':'Name you wish to see'})
    password = PasswordField('Password', [validators.length(min=6), validators.DataRequired()], render_kw={'placeholder':'Password minimum 8 characters'})
    email = EmailField('Email', [validators.length(min=6), validators.DataRequired(), validators.Email()], render_kw={'placeholder': 'Email'})
    mobile = StringField('Mobile', [validators.length(min=10), validators.DataRequired()], render_kw={'placeholder':'mobile "ex : 1234567890"'})

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        email = form.email.data
        mobile = form.mobile.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, username, user_password, email, mobile) VALUES(%s, %s, %s, %s, %s)", (name, username, password, email, mobile))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run()

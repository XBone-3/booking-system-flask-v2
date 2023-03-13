from flask import Flask, render_template
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.secret_key = SECRET_KEY
PASSWORD = 'fool'.encode()

mysql = MySQL()
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "call_me_x"
app.config['MYSQL_PASSWORD'] = PASSWORD.decode()
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'crittle'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql.init_app(app)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run()

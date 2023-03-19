from flask import Flask, flash, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
from forms import  LoginForm, RegisterForm, SlotBookingForm, PasswordResetForm
from passlib.hash import sha256_crypt
from datetime import datetime
from statics import COURT_1, COURT_2, CRICKET, MONTHS, SLOTS, C_SLOTS, PASSWORD, SECRET_KEY

FORGOT_PASSWORD_STATUS = False

app = Flask(__name__)
app.secret_key = SECRET_KEY


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


@app.route('/admin_home')
def dashboard():
    return render_template("admin.html")

@app.route('/FAQ')
def faq():
    return render_template("FAQ.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'search' in request.args:
        search_term = request.args['search']
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        user_password = form.password.data
        cur = mysql.connection.cursor()
        result = cur.execute(
            "SELECT * FROM users WHERE username=%(user_name)s", {'user_name': username})
        if result > 0:
            data = cur.fetchone()
            name = data['name']
            password = data['user_password']
            uid = data['id']
            admin = data['admin']
            username = data['username']
            mobile = data['mobile']
            if sha256_crypt.verify(user_password, password):
                session['logged'] = True
                session['uid'] = uid
                session['name'] = name
                session['admin'] = admin
                session['username'] = username
                session['mobile'] = mobile
                online = 1
                cur.execute("UPDATE users SET online=%(online_status)s WHERE id=%(user_id)s", {
                            'online_status': online, 'user_id': uid})
                mysql.connection.commit()
                cur.close()
                return redirect(url_for('index'))
            else:
                mysql.connection.commit()
                cur.close()
                flash("Password wrong, Please enter correct Password.")
                return redirect(url_for('login'))
        else:
            flash("User Does not exist, Please register.")
            return redirect(url_for("register"))
    return render_template('login.html', form=form, forgot_password=FORGOT_PASSWORD_STATUS)


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        admin_password = form.password.data
        cur = mysql.connection.cursor()
        result = cur.execute(
            "SELECT * FROM admins WHERE username = %(user_name)s ", {'user_name': username})
        if result > 0:
            data = cur.fetchone()
            password = data['admin_password']
            uid = data['id']
            name = data['name']
            admin = data['admin']
            username = data['username']
            if sha256_crypt.verify(admin_password, password):
                session['logged'] = True
                session['uid'] = uid
                session['name'] = name
                session['admin'] = admin
                session['username'] = username
                online = 1
                cur.execute("UPDATE admins SET online=%(online_status)s where id=%(admin_id)s", {
                            'admin_id': uid, 'online_status': online})
                mysql.connection.commit()
                cur.close()
                flash("Successfully Logged")
                return redirect(url_for("dashboard"))
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
            cur.execute("UPDATE admins SET online=%(online_status)s where id=%(user_id)s", {
                        'user_id': uid, 'online_status': online})
        else:
            cur.execute("UPDATE users SET online=%(online_status)s where id=%(user_id)s", {
                        'user_id': uid, 'online_status': online})
        mysql.connection.commit()
        cur.close()
        session.clear()
    return redirect(url_for('index'))

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    FORGOT_PASSWORD_STATUS = True
    form = LoginForm(request.form)
    reset_form = PasswordResetForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        mobile = form.mobile.data
        cur = mysql.connection.cursor()
        if 'reset' in request.args:
            if reset_form.confirm_new_password.data == reset_form.new_password.data:
                new_password = sha256_crypt.encrypt(str(reset_form.new_password.data))
                cur.execute("UPDATE users SET user_password=%(new_pass)s WHERE username=%(user_name)s", {'user_name':username, 'new_pass':new_password})
                mysql.connection.commit()
                cur.close()
                flash("password updated successfully")
                return redirect(url_for('login'))
            else:
                flash("password mismatch")
                return render_template('reset.html', form=reset_form)
        result = cur.execute("SELECT * FROM users WHERE username=%(user_name)s", {'user_name': username})
        if result > 0:
            user = cur.fetchone()
            if user['mobile'] == mobile:
                cur.close()
                FORGOT_PASSWORD_STATUS = False
                return render_template('reset.html', form=reset_form)
            else:
                cur.close()
                flash("please enter correct mobile")
                return render_template('login.html', form=form, forgot_password=FORGOT_PASSWORD_STATUS)
        else:
            cur.close()
            flash("Please enter Valid details")
            return render_template('login.html', form=form, forgot_password=FORGOT_PASSWORD_STATUS)
    return render_template('login.html', form=form, forgot_password=FORGOT_PASSWORD_STATUS)


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
        result = cur.execute("SELECT username FROM users WHERE username=%(user_name)s", {
                             'user_name': username})
        if result == 0:
            cur.execute("INSERT INTO users(name, username, user_password, email, mobile) VALUES(%s, %s, %s, %s, %s)",
                        (name, username, password, email, mobile))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('index'))
        else:
            cur.close()
            flash(f"{username} already exist please login or try creating account with unique Username")
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


def helper(sport):
    flash(f"Select a slot for {sport}")
    return redirect(url_for('book_slot'))


@app.route('/bookslot', methods=['GET', 'POST'])
def book_slot():
    court_1 = SlotBookingForm(request.form, label=COURT_1, sport='Badminton')
    court_2 = SlotBookingForm(request.form, label="Court 2", sport="Badminton")
    cricket = SlotBookingForm(request.form, label=CRICKET, sport="Cricket")
    radio_day = SlotBookingForm(request.form, label="Day", sport="")
    booked_slots = disable_slots()
    if request.method == 'POST':
        court1_slot_value = court_1.court1_slots.data
        court1_comment_value = court_1.court1_comment.data
        court2_slot_value = court_2.court2_slots.data
        court2_comment_value = court_2.court2_comment.data
        cricket_slot_value = cricket.cricket_slots.data
        cricket_comment_value = cricket.cricket_comment.data
        day_value = radio_day.days.data
        print(day_value)
        # TODO: implement next day slots
        date = datetime.now().date()
        cur = mysql.connection.cursor()
        if 'logged' in session:
            sport = request.args['sport']
            query_string = "INSERT INTO bookings(username, user_id, sport, courtname, year, month, day, timeslot, comment) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            update_query = "UPDATE slotsavailable SET availability=0 WHERE courtname=%(court_name)s and timeslot=%(time_slot)s and date=%(date)s"
            if sport == CRICKET and cricket_slot_value != None:
                cur.execute(query_string, (session['username'], session['uid'], "Cricket", sport, date.year, MONTHS[date.month], date.day, cricket_slot_value, cricket_comment_value))
                cur.execute(update_query, {'court_name':sport, 'time_slot':cricket_slot_value, 'date':date})
            elif sport == CRICKET and cricket_slot_value == None:
                helper(sport)
            elif sport == COURT_1 and court1_slot_value != None:
                cur.execute(query_string, (session['username'], session['uid'], "Badminton", sport, date.year, MONTHS[date.month], date.day, court1_slot_value, court1_comment_value))
                cur.execute(update_query, {'court_name':sport, 'time_slot':court1_slot_value, 'date':date})
            elif sport == COURT_1 and court1_slot_value == None:
                helper(sport)
            elif sport == COURT_2 and court2_slot_value != None:
                cur.execute(query_string, (session['username'], session['uid'], "Badminton", sport, date.year, MONTHS[date.month], date.day, court2_slot_value, court2_comment_value))
                cur.execute(update_query, {'court_name':sport, 'time_slot':court2_slot_value, 'date':date})
            elif sport == COURT_2 and court2_slot_value == None:
                helper(sport)
            mysql.connection.commit()
            cur.close()
            flash(f"Slot booked successfully for {sport}")
            return redirect(url_for('book_slot'))
        else:
            cur.close()
            flash("please Login to Book a Slot")
            return redirect(url_for('login'))
    return render_template('slots.html', court_1=court_1, court_2=court_2, cricket=cricket, day_choice=radio_day, booked_slots=booked_slots)


@app.route('/timeline')
def timeline():
    if "logged" in session:
        cur = mysql.connection.cursor()
        result = cur.execute(
            "SELECT * FROM bookings WHERE username=%(user_name)s", {'user_name': session['username']})
        if result > 0:
            bookings = cur.fetchall()
            cur.close()
            return render_template('timeline.html', bookings=bookings, length=len(bookings))
    return render_template('timeline.html', bookings=[], length=0)


def disable_slots():
    date = datetime.now().date()
    time = str(datetime.now().time()).split(':')
    hour = int(time[0])
    booked_slots = {
        CRICKET: [],
        COURT_1: [],
        COURT_2: []
        }
    if hour >= 20:
        booked_slots[COURT_1].extend(SLOTS)
        booked_slots[COURT_2].extend(SLOTS)
        booked_slots[CRICKET].extend(C_SLOTS)
    elif hour >= 17:
        booked_slots[COURT_1].extend(SLOTS[:3])
        booked_slots[COURT_2].extend(SLOTS[:3])
        booked_slots[CRICKET].extend(C_SLOTS[:2])
    elif hour >= 14:
        booked_slots[COURT_1].extend(SLOTS[:2])
        booked_slots[COURT_2].extend(SLOTS[:2])
        booked_slots[CRICKET].extend(C_SLOTS[:2])
    elif hour >= 10:
        booked_slots[COURT_1].extend(SLOTS[:2])
        booked_slots[COURT_2].extend(SLOTS[:2])
        booked_slots[CRICKET].append(C_SLOTS[0])
    elif hour >= 8:
        booked_slots[COURT_1].extend(SLOTS[:2])
        booked_slots[COURT_2].extend(SLOTS[:2])
    elif hour >= 6:
        booked_slots[COURT_1].append(SLOTS[0])
        booked_slots[COURT_2].append(SLOTS[0])
    cur = mysql.connection.cursor()
    available_slots = cur.execute("SELECT * FROM slotsavailable WHERE availability=1 and date=%(date)s", {'date':date})
    if available_slots == 0:
        booked_slots[COURT_1].extend(SLOTS)
        booked_slots[COURT_2].extend(SLOTS)
        booked_slots[CRICKET].extend(C_SLOTS)
        cur.close()
        return booked_slots
    result = cur.execute("SELECT courtname, timeslot FROM slotsavailable WHERE availability=0 and date=%(date)s", {'date':date})
    if result > 0:
        current_day_slots = cur.fetchall()
        for slot in current_day_slots:
            if slot['timeslot'] not in booked_slots[slot['courtname']]:
                booked_slots[slot['courtname']].append(slot['timeslot'])
        cur.close()
        return booked_slots
    else:
        cur.close()
        return booked_slots
    


if __name__ == '__main__':
    app.run()

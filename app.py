from flask import Flask, flash, jsonify, render_template, request, session, redirect, url_for
from forms import LoginForm, RegisterForm, SlotBookingForm, PasswordResetForm, AdminSlotBookingForm
from passlib.hash import sha256_crypt
from datetime import datetime, timedelta
from statics import COURT_1, COURT_2, CRICKET, MONTHS, PASSWORD, B_SLOTS, C_SLOTS, SECRET_KEY, HTMLS, BADMINTON, SUCCESSFULL_LOGIN_MESSAGE
from models import db, Users, Bookings, Slots, Conf

FORGOT_PASSWORD_STATUS = False

app = Flask(__name__)
app.secret_key = SECRET_KEY

Conf(app, PASSWORD.decode())

db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/')
@app.route('/home')
def index():
    session['day'] = 'today'
    return render_template(HTMLS['index'])

@app.route('/about')
def about():
    session['day'] = 'today'
    return render_template(HTMLS['about'])

def prepare_slots(court1_blocked_slots, court2_blocked_slots, cricket_blocked_slots, date):
    slots = []
    for timeslot in C_SLOTS:
        if timeslot in cricket_blocked_slots:
            slots.append(Slots(sport=CRICKET, courtname=CRICKET, timeslot=timeslot, availability=0, date=date))
        else:
            slots.append(Slots(sport=CRICKET, courtname=CRICKET, timeslot=timeslot, date=date))
    for timeslot in B_SLOTS:
        if timeslot in court1_blocked_slots:
            slots.append(Slots(sport=BADMINTON, courtname=COURT_1, timeslot=timeslot, availability=0, date=date))
        else:
            slots.append(Slots(sport=BADMINTON, courtname=COURT_1, timeslot=timeslot, date=date))
        if timeslot in court2_blocked_slots:
            slots.append(Slots(sport=BADMINTON, courtname=COURT_2, timeslot=timeslot, availability=0, date=date))
        else:
            slots.append(Slots(sport=BADMINTON, courtname=COURT_2, timeslot=timeslot, date=date))
    return slots

def update_slots(court1_blocked_slots, court2_blocked_slots, cricket_blocked_slots, date):
    slots = Slots.query.filter_by(date=date).count()
    if slots > 0:
        flash("slots already available for today")
        return redirect(url_for('dashboard'))
    else:
        slots = prepare_slots(court1_blocked_slots, court2_blocked_slots, cricket_blocked_slots, date)
        db.session.add_all(slots)
        db.session.commit()
        flash("slots updated successfully")
        return redirect(url_for('dashboard'))

@app.route('/admin_home', methods=['GET', 'POST'])
def dashboard():
    session['day'] = 'today'
    court_1 = AdminSlotBookingForm(label=COURT_1, sport=BADMINTON)
    court_2 = AdminSlotBookingForm(label=COURT_2, sport=BADMINTON)
    cricket = AdminSlotBookingForm(label=CRICKET, sport=CRICKET)
    blocked_slots, blocked_slots_1 = disable_slots()    # this function gives unavailable slots 
    online_users = Users.query.filter_by(online=1).count()
    if request.method == 'POST':
        court1_blocked_slots = court_1.court1_slots.data if court_1.court1_slots.data != None else []
        court2_blocked_slots = court_2.court2_slots.data if court_2.court2_slots.data != None else []
        cricket_blocked_slots = cricket.cricket_slots.data if cricket.cricket_slots.data != None else []
        court1_blocked_slots_1 = court_1.court1_slots_1.data if court_1.court1_slots_1.data != None else []
        court2_blocked_slots_1 = court_2.court2_slots_1.data if court_2.court2_slots_1.data != None else []
        cricket_blocked_slots_1 = cricket.cricket_slots_1.data if cricket.cricket_slots_1.data != None else []
        if 'logged' in session:
            slot = int(request.args['slot'])            # 0 is for today, 1 is for next day
            date = datetime.now().date()
            if slot == 0:
                return update_slots(court1_blocked_slots, court2_blocked_slots, cricket_blocked_slots, date=date)
            elif slot == 1:
                date += timedelta(days=slot)
                return update_slots(court1_blocked_slots_1, court2_blocked_slots_1, cricket_blocked_slots_1, date=date)
            else:
                flash("something went wrong")
                return redirect(url_for('dashboard'))   
        else:
            flash("please login to make changes")
            return redirect(url_for('login'))  
    return render_template(HTMLS['admin'], ONLINE_USERS=online_users, court_1=court_1, court_2=court_2, cricket=cricket, blocked_slots=blocked_slots, blocked_slots_1=blocked_slots_1)


@app.route('/FAQ')
def faq():
    session['day'] = 'today'
    return render_template(HTMLS['faq'])


@app.route('/search', methods=['GET', 'POST'])
def search():
    session['day'] = 'today'
    if request.method == 'GET':
        print('requested')
        if 'search' in request.args:
            search_term = request.args['search']
            print(search_term, "tested")
            return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    session['day'] = 'today'
    form = LoginForm()
    if request.method == 'POST':
        username = form.username.data
        user_password = form.password.data
        user = Users.query.filter_by(username=username).first()
        if user:
            name = user.name
            uid = user.user_id
            admin = user.admin
            username = user.username
            mobile = user.mobile
            email = user.email
            if user.verify_password(str(user_password)):
                session['logged'] = True
                session['uid'] = uid
                session['name'] = name
                session['admin'] = admin
                session['username'] = username
                session['mobile'] = mobile
                session['email'] = email
                user.online = 1
                db.session.commit()
                if user.is_admin():
                    flash(SUCCESSFULL_LOGIN_MESSAGE)
                    return redirect(url_for("dashboard"))
                else:
                    flash(SUCCESSFULL_LOGIN_MESSAGE)
                    return redirect(url_for('book_slot'))
            else:
                flash("Password wrong, Please enter correct Password.")
                return redirect(url_for('login'))
        else:
            flash("User Does not exist, Please register.")
            return redirect(url_for("register"))
    return render_template(HTMLS['login'], form=form, forgot_password=FORGOT_PASSWORD_STATUS)


@app.route('/logout')
def logout():
    session['day'] = 'today'
    if 'uid' in session:
        uid = session['uid']
        user = Users.query.filter_by(user_id=uid).first()
        user.online = 0
        db.session.commit()
        session.clear()
    return redirect(url_for('index'))


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    session['day'] = 'today'
    FORGOT_PASSWORD_STATUS = True
    form = LoginForm()
    reset_form = PasswordResetForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        mobile = form.mobile.data
        if 'reset' in request.args:
            if reset_form.confirm_new_password.data == reset_form.new_password.data:
                new_password = sha256_crypt.encrypt(str(reset_form.new_password.data))
                user = Users.query.filter_by(username=session['username']).first()
                user.password = new_password
                db.session.commit()
                flash("password updated successfully")
                session.clear()
                return redirect(url_for('login'))
            else:
                flash("password mismatch")
                return render_template(HTMLS['reset'], form=reset_form)
        user = Users.query.filter_by(username=username).first()
        if user:
            if user.mobile == mobile:
                FORGOT_PASSWORD_STATUS = False
                session['username'] = username
                session['mobile'] = mobile
                return render_template(HTMLS['reset'], form=reset_form)
            else:
                flash("please enter correct mobile")
                return render_template(HTMLS['login'], form=form, forgot_password=FORGOT_PASSWORD_STATUS)
        else:
            flash("Please enter Valid details")
            return render_template(HTMLS['login'], form=form, forgot_password=FORGOT_PASSWORD_STATUS)
    return render_template(HTMLS['login'], form=form, forgot_password=FORGOT_PASSWORD_STATUS)


@app.route('/register', methods=['GET', 'POST'])
def register():
    session['day'] = 'today'
    form = RegisterForm()
    if request.method == 'POST':
        name = form.name.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        email = form.email.data
        mobile = form.mobile.data
        result = Users.query.filter_by(username=username).first()
        if result is None or result == 0:
            user = Users(
                name=name,
                username=username,
                password=password,
                email=email,
                mobile=mobile
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            flash(f"{username} already exist please login or try creating account with unique Username")
            return redirect(url_for('login'))
    return render_template(HTMLS['register'], form=form)

@app.route('/get_usernames', methods=['GET'])
def get_username():
    user_names = Users.query.with_entities(Users.username).all()
    return [tuple(row) for row in user_names]


def helper(sport, court, booked):
    '''
    sport : String,
    court : String,
    booked: Boolean

    show a flash message depending on the booked status.
    returns a flask responce.
    '''
    if booked:
        flash(f"Slot booked successfully for {sport} at {court}")
    else:
        flash(f"Select a slot for {sport} at {court}")
    return redirect(url_for('book_slot'))

def time_comment_data(court_1, court_2, cricket):
    '''
    court_1 :   class 'forms.SlotBookingForm',
    court_2 :   class 'forms.SlotBookingForm',
    cricket :   class 'forms.SlotBookingForm'

    returns tuple of String objects.

    given the form objects this outputs the timeslot and comment data provided by the user.
    '''
    timeslot = list()
    comment = list()
    timeslot.append(court_1.court1_slots.data) if court_1.court1_slots.data != None else timeslot.append(str(0))
    comment.append(court_1.court1_comment.data) if court_1.court1_comment.data != None else comment.append('')
    timeslot.append(court_2.court2_slots.data) if court_2.court2_slots.data != None else timeslot.append(str(0))
    comment.append(court_2.court2_comment.data) if court_2.court2_comment.data != None else comment.append('')
    timeslot.append(cricket.cricket_slots.data) if cricket.cricket_slots.data != None else timeslot.append(str(0))
    comment.append(cricket.cricket_comment.data) if cricket.cricket_comment.data != None else comment.append('')
    timeslot.sort()
    comment.sort()
    return timeslot[-1], comment[-1]

@app.route('/bookslot', methods=['GET', 'POST'])
def book_slot():
    court_1 = SlotBookingForm(label=COURT_1, sport=BADMINTON)
    court_2 = SlotBookingForm(label=COURT_2, sport=BADMINTON)
    cricket = SlotBookingForm(label=CRICKET, sport=CRICKET)
    radio_day = SlotBookingForm(label="Day", sport="")
    blocked_slots, blocked_slots_1 = disable_slots()
    if request.method == 'POST':
        timeslot, comment = time_comment_data(court_1=court_1, court_2=court_2, cricket=cricket)
        date = datetime.now().date()
        next_day_date = date+timedelta(days=1)
        if 'logged' in session:
            sport = request.args['sport']
            court = request.args['court']
            if timeslot == "0":
                return helper(sport=sport, court=court, booked=False)
            it_is_today = session['day'] == 'today'
            booking = Bookings(
                    user_id=session['uid'],
                    sport=sport,
                    courtname=court,
                    year=date.year if it_is_today else next_day_date.year,
                    month=MONTHS[date.month if it_is_today else next_day_date.month],
                    day=date.day if it_is_today else next_day_date.day,
                    timeslot=timeslot,
                    comment=comment if comment != '' else None
                    )
            if session['day'] == "tomorrow":
                slot = Slots.query.filter_by(courtname=court, timeslot=timeslot, date=date+timedelta(days=1)).first()
            else:
                slot = Slots.query.filter_by(courtname=court, timeslot=timeslot, date=date).first()
            slot.availability = 0
            db.session.add(booking)
            db.session.commit()
            return helper(sport=sport, court=court, booked=True)
        else:
            flash("please Login to Book a Slot")
            return redirect(url_for('login'))
    return render_template(HTMLS['slots'], court_1=court_1, court_2=court_2, cricket=cricket, day_choice=radio_day, blocked_slots=blocked_slots, blocked_slots_1=blocked_slots_1)

@app.route('/bookslot/<day>')
def update_session(day):
    session['day'] = day
    return redirect(url_for('book_slot'))


@app.route('/timeline')
def timeline():
    session['day'] = 'today'
    if "logged" in session:
        bookings = Bookings.query.filter_by(user_id=session['uid']).all()
        return render_template(HTMLS['timeline'], bookings=bookings, length=len(bookings))
    return render_template(HTMLS['timeline'], bookings=[], length=0)

def time_block_slots(available_slots, hour, blocked_slots, tomorrow=False):
    '''
    available_slots :   Int,
    hour    : Int,
    blocked_slots   :   dictionary of lists,
                        {
                            court_1 :   []
                            ...
                        }
    tomorrow    :   Boolean

    returns None

    updates the blocked_slots object inplace.
    '''
    if available_slots == 0:
        blocked_slots[COURT_1].extend(B_SLOTS)
        blocked_slots[COURT_2].extend(B_SLOTS)
        blocked_slots[CRICKET].extend(C_SLOTS)
    if tomorrow == False:
        if hour >= 20:
            blocked_slots[COURT_1].extend(B_SLOTS)
            blocked_slots[COURT_2].extend(B_SLOTS)
            blocked_slots[CRICKET].extend(C_SLOTS)
        elif hour >= 17:
            blocked_slots[COURT_1].extend(B_SLOTS[:3])
            blocked_slots[COURT_2].extend(B_SLOTS[:3])
            blocked_slots[CRICKET].extend(C_SLOTS[:2])
        elif hour >= 14:
            blocked_slots[COURT_1].extend(B_SLOTS[:2])
            blocked_slots[COURT_2].extend(B_SLOTS[:2])
            blocked_slots[CRICKET].extend(C_SLOTS[:2])
        elif hour >= 10:
            blocked_slots[COURT_1].extend(B_SLOTS[:2])
            blocked_slots[COURT_2].extend(B_SLOTS[:2])
            blocked_slots[CRICKET].append(C_SLOTS[0])
        elif hour >= 8:
            blocked_slots[COURT_1].extend(B_SLOTS[:2])
            blocked_slots[COURT_2].extend(B_SLOTS[:2])
        elif hour >= 6:
            blocked_slots[COURT_1].append(B_SLOTS[0])
            blocked_slots[COURT_2].append(B_SLOTS[0])


def disable_slots():
    '''
    returns tuple[dict[str, list], dict[str, list]]
    '''
    date = datetime.now().date()
    time = str(datetime.now().time()).split(':')
    hour = int(time[0])
    blocked_slots = {
        CRICKET: [],
        COURT_1: [],
        COURT_2: []
    }
    blocked_slots_tomorrow = {
        CRICKET: [],
        COURT_1: [],
        COURT_2: []
    }
    available_slots_today = Slots.query.filter_by(availability=1, date=date).count()
    available_slots_tomorrow = Slots.query.filter_by(availability=1, date=date+timedelta(days=1)).count()
    time_block_slots(available_slots=available_slots_today, hour=hour, blocked_slots=blocked_slots)
    time_block_slots(available_slots=available_slots_tomorrow, hour=hour, blocked_slots=blocked_slots_tomorrow, tomorrow=True)
    current_day_slots = Slots.query.filter_by(availability=0, date=date).all()
    next_day_slots = Slots.query.filter_by(availability=0, date=date+timedelta(days=1)).all()
    if len(current_day_slots) > 0:
        for slot in current_day_slots:
            if slot.timeslot not in blocked_slots[slot.courtname]:
                blocked_slots[slot.courtname].append(slot.timeslot)
    if len(next_day_slots) > 0:
        for slot in next_day_slots:
            if slot.timeslot not in blocked_slots_tomorrow[slot.courtname]:
                blocked_slots_tomorrow[slot.courtname].append(slot.timeslot)
    return blocked_slots, blocked_slots_tomorrow


if __name__ == '__main__':
    app.run()

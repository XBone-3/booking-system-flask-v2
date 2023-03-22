import os


MONTHS = {	
            1:'January',
            2:'February',
            3:'March',
            4:'April',
            5:'May',
            6:'June',
            7:'July',
            8:'August',
            9:'September',
            10:'October',
            11:'November',
            12:'December'
        }

COURT_1 = 'Court 1'
COURT_2 = 'Court 2'
CRICKET = 'Cricket'
BADMINTON = 'Badminton'
SLOTS = ['6:00 am', '8:00 am', '5:30 pm', '8:30 pm']
C_SLOTS = ['forenoon', 'afternoon', 'night']
PASSWORD = 'fool'.encode()
SECRET_KEY = os.urandom(32)

BADMINTON_CHOICES = [("6:00 am", "slot 1"), ("8:00 am", "slot 2"), ("5:30 pm", "slot 3"), ("8:30 pm", "slot 4")]
CRICKET_CHOICES = [("forenoon", "forenoon"), ("afternoon", "afternoon"), ("night", "night")]
DAY_CHOICES = [('today', "Today"), ('tomorrow', "Tomorrow")]

HTMLS = {
    'login':'login.html',
    'admin':'admin.html',
    'timeline':'timeline.html',
    'reset': 'reset.html',
    'register':'register.html',
    'slots': 'slots.html',
    'index': 'index.html',
    'faq': 'FAQ.html',
    'admin login': 'admin_login.html',
    'about': 'About.html',
}

QUERY = '''INSERT INTO slotsavailable 
            (sport, courtname, availability, timeslot)
            VALUES 
            ("Cricket", "Cricket", 1, "forenoon"),
            ("Cricket", "Cricket", 1, "afternoon"),
            ("Cricket", "Cricket", 1, "night"),
            ("Badminton", "Court 1", 1, "6:00 am"),
            ("Badminton", "Court 1", 1, "8:00 am"),
            ("Badminton", "Court 1", 1, "5:30 pm"),
            ("Badminton", "Court 1", 1, "8:30 pm"),
            ("Badminton", "Court 2", 1, "6:00 am"),
            ("Badminton", "Court 2", 1, "8:00 am"),
            ("Badminton", "Court 2", 1, "5:30 pm"),
            ("Badminton", "Court 2", 1, "8:30 pm");'''
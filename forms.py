from wtforms import StringField, EmailField, PasswordField, validators, Form, RadioField, TextAreaField
from statics import COURT_2, COURT_1, CRICKET


class LoginForm(Form):
    username = StringField('Username', [validators.length(
        min=3, max=11), validators.DataRequired()], render_kw={'placeholder': 'User Name'})
    password = PasswordField('Password', [validators.length(
        min=6), validators.DataRequired()], render_kw={'placeholder': 'Enter your password'})
    mobile = StringField('Registered Mobile', [validators.length(min=10), validators.DataRequired()], render_kw={'placeholder':'enter registered mobile'})


class RegisterForm(Form):
    name = StringField('Name', [validators.length(min=3, max=15), validators.DataRequired(
    )], render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    username = StringField('Username', [validators.length(
        min=3, max=11), validators.DataRequired()], render_kw={'placeholder': 'Name you wish to see'})
    password = PasswordField('Password', [validators.length(min=6), validators.DataRequired(
    )], render_kw={'placeholder': 'Password minimum 8 characters'})
    confirm_password = PasswordField('Confirm Password', [validators.EqualTo("password", message="password mismatch")], render_kw={'placeholder':'enter same password'})
    email = EmailField('Email', [validators.length(min=6), validators.DataRequired(
    ), validators.Email()], render_kw={'placeholder': 'Email'})
    mobile = StringField('Mobile', [validators.length(min=10), validators.DataRequired(
    )], render_kw={'placeholder': 'mobile "ex : 1234567890"'})


class PasswordResetForm(Form):
    new_password = PasswordField('New Password', [validators.length(
        min=6), validators.DataRequired()], render_kw={'placeholder': 'Enter your new password'})
    confirm_new_password = PasswordField('Confirm new Password', [validators.EqualTo('new_password', message='password mismatch')], render_kw={'placeholder': 'enter same password'})
    
    

class SlotBookingForm(Form):
    choices = [("6:00 am", "slot 1"), ("8:00 am", "slot 2"), ("5:30 pm", "slot 3"), ("8:30 pm", "slot 4")]
    day_choices = [('today', "Today"), ('tomorrow', "Tomorrow")]
    days = RadioField(label='Day', choices=day_choices)

    court1_slots = RadioField(label=COURT_1, choices=choices)
    
    court1_comment = TextAreaField(label='Comment', render_kw={'cols':24, 'rows':3, 'placeholder':'comment'})

    court2_slots = RadioField(label=COURT_2, choices=choices)
    
    court2_comment = TextAreaField(label="Comment", render_kw={'cols':25, 'rows':3, 'placeholder':'comment'})
    
    cricket_slots = RadioField(label=CRICKET, choices=[(
        "forenoon", "forenoon"), ("afternoon", "afternoon"), ("night", "night")])
    
    cricket_comment = TextAreaField(label="Comment", render_kw={'cols':25, 'rows':3, 'placeholder':'comment'})

    def __init__(self, formdata=None, obj=None, prefix="", data=None, meta=None, **kwargs):
        super().__init__(formdata, obj, prefix, data, meta, **kwargs)
        self.label = kwargs['label']
        self.sport = kwargs['sport']
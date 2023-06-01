from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, validators, RadioField, TextAreaField, SelectMultipleField, MultipleFileField, widgets
from statics import COURT_2, COURT_1, CRICKET, BADMINTON_CHOICES, DAY_CHOICES, CRICKET_CHOICES


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.length(
        min=3, max=11), validators.DataRequired()], render_kw={'placeholder': 'User Name'})
    password = PasswordField('Password', [validators.length(
        min=6), validators.DataRequired()], render_kw={'placeholder': 'Enter your password'})
    mobile = StringField('Registered Mobile', [validators.length(min=10), validators.DataRequired()], render_kw={'placeholder':'enter registered mobile'})


class RegisterForm(FlaskForm):
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


class PasswordResetForm(FlaskForm):
    new_password = PasswordField('New Password', [validators.length(
        min=6), validators.DataRequired()], render_kw={'placeholder': 'Enter your new password'})
    confirm_new_password = PasswordField('Confirm new Password', [validators.EqualTo('new_password', message='password mismatch')], render_kw={'placeholder': 'enter same password'})
    
    

class SlotBookingForm(FlaskForm):
    days = RadioField(label='Day', choices=DAY_CHOICES)

    court1_slots = RadioField(label=COURT_1, choices=BADMINTON_CHOICES)
    
    court1_comment = TextAreaField(label='Comment', render_kw={'cols':24, 'rows':3, 'placeholder':'comment'})

    court2_slots = RadioField(label=COURT_2, choices=BADMINTON_CHOICES)
    
    court2_comment = TextAreaField(label="Comment", render_kw={'cols':25, 'rows':3, 'placeholder':'comment'})
    
    cricket_slots = RadioField(label=CRICKET, choices=CRICKET_CHOICES)
    
    cricket_comment = TextAreaField(label="Comment", render_kw={'cols':25, 'rows':3, 'placeholder':'comment'})

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.label = kwargs['label']
        self.sport = kwargs['sport']


class MultiSelect(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AdminSlotBookingForm(FlaskForm):
    days = RadioField(label='Day', choices=DAY_CHOICES)

    court1_slots = MultiSelect(label=COURT_1, choices=BADMINTON_CHOICES)

    court2_slots = MultiSelect(label=COURT_2, choices=BADMINTON_CHOICES)
    
    cricket_slots = MultiSelect(label=CRICKET, choices=CRICKET_CHOICES)

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.label = kwargs['label']
        self.sport = kwargs['sport']
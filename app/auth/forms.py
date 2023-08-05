import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from wtforms import ValidationError

from app.auth.models import User


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(5, 200),
            Email()
        ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(3, 100),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must contains only letters, underscores or digits')
        ],
        render_kw={'placeholder': 'Enter your name'}
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(10, 200),
            Email()
        ]
    )
    info = StringField(
        'Info',
        validators=[
            DataRequired(),
            Length(3, 200)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            EqualTo('password_repeat', message='Password must match')
        ]
    )
    password_repeat = PasswordField(
        'Confirm password',
        validators=[DataRequired()]
    )
    submit = SubmitField(
        'Register',
        render_kw={
            'class': 'btn btn-primary'
        }
    )

    def validate_email(self, field):
        if User.select().where(User.email == field.data).first():
            raise ValidationError('Email already exist')

    def validate_password(self, field):
        # length_error = len(field.data) < 8
        # digit_error = re.search(r"\d", field.data) is None
        # uppercase_error = re.search(r"[A-Z]", field.data) is None
        # lowercase_error = re.search(r"[a-z]", field.data) is None
        # symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', field.data) is None
        #
        # password_error = any([length_error, digit_error, uppercase_error, lowercase_error, symbol_error])

        if len(field.data) < 8:
            raise ValidationError('Password must be at least 8 chars include Upper, Lower, Digit, Punctuation')

from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, Email


class GenerateDataForm(FlaskForm):
    qty = SelectField(
        'Quantity',
        validators=[DataRequired()],
        choices=[10, 15, 25]
    )
    submit = SubmitField('Generate')


class EditUserForm(FlaskForm):
    id = HiddenField()
    username = StringField(
        'Edit username',
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
    submit = SubmitField('Edit')

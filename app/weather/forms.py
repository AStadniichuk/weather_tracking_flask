from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CityForm(FlaskForm):
    city_name = StringField(
        'What city are you interested in?',
        validators=[DataRequired(), Length(3, 150)],
        render_kw={'placeholder': 'City name'}
    )
    submit = SubmitField('Show')

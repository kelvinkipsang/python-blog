from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import Optional, Length, DataRequired, URL, Email
from wtforms.fields.html5 import DateField


class TalkForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(1, 128)])
    description = TextAreaField('Description')
    slides = StringField('Slides Embed Code (450 pixels wide)')
    video = StringField('Video Embed Code (450 pixels wide)')
    venue = StringField('Venue',
                        validators=[DataRequired(), Length(1, 128)])
    venue_url = StringField('Venue URL',
                            validators=[Optional(), Length(1, 128), URL()])
    date = DateField('Date')
    submit = SubmitField('Submit')
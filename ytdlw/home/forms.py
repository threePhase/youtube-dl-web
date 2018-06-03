from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, Email
from wtforms.validators import url as URL


class DownloadForm(FlaskForm):
    url = URLField('URL',
        validators=[DataRequired(), URL()])
    outputDir = URLField('Output Directory')
    authenticate = BooleanField('Authenticate?')
    provider = SelectField('Provider',
        choices=[('Comcast/Xfinity', 'Comcast/Xfinity')])
    username = StringField('Username',
        validators=[Email()])
    password = PasswordField('Password')

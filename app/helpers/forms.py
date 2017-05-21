from wtforms import BooleanField, Form, StringField, validators


class RegistrationForm(Form):
    user_id = StringField('User Id', [validators.Regexp(r'^[a-zA-Z0-9_]+$')])
    admin = BooleanField('Admin', [validators.DataRequired()])
    transcriber = BooleanField('Transcriber', [validators.DataRequired()])
    voicer = BooleanField('Voicer', [validators.DataRequired()])
    name = StringField('Name', [validators.DataRequired()])
    email = StringField('Email Address', [
        validators.DataRequired(), validators.Email()])

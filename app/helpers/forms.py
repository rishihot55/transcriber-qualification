from wtforms import BooleanField, Form, StringField, validators


class RegistrationForm(Form):
    user_id = StringField('User Id', [validators.Regexp(r'^[a-zA-Z0-9_]+$')])
    admin = BooleanField('Admin', [validators.DataRequired()])
    transcriber = BooleanField('Transcriber', [])
    voicer = BooleanField('Voicer', [])
    name = StringField('Name', [])
    email = StringField('Email Address', [
        validators.DataRequired(), validators.Email()])


class TranscriptForm(Form):
    """
    Process the submit transcript form.

    Only a subset of symbols are allowed to be submitted.
    This is to ensure that no attempt is made to pass highly garbled input
    or some form of vulnerability inducing input
    """
    transcript = StringField('Transcript',
                             [validators.DataRequired(),
                              validators.Regexp(r'^[\w\'";?!,.: ]+$')])

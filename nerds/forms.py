from wtforms import Form, BooleanField, TextField, PasswordField, validators

class RegistrationForm(Form):
    first_name = TextField('First Name', [validators.Length(min=2, max=25)])
    last_name = TextField('Last Name', [validators.Length(min=2, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=40),validators.Email(message=u'Invalid email address.')])
    password = PasswordField('New Password', [
        validators.Length(min=6),
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    email = TextField('Email Address')
    password = PasswordField('Password')

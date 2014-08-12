from wtforms import Form, BooleanField, TextField, PasswordField, validators, SelectField

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

class ClassForm(Form):
    teacher = TextField('First Name', [validators.Length(min=2, max=25)])
    dif = SelectField('Difficulty', ["Level", "Honors", "Pre-AP", "Dual Credit", "AP", "N/A"])
    period = SelectField('Period', [1,2,3,4,5,6,7])

class SceduleForm(Form):
    period1 = SelectField('period1', ["placeholder"])
    period2 = SelectField('period2', ["placeholder"])
    period3 = SelectField('period3', ["placeholder"])
    period4 = SelectField('period4', ["placeholder"])
    period5 = SelectField('period5', ["placeholder"])
    period6 = SelectField('period6', ["placeholder"])
    period7 = SelectField('period7', ["placeholder"])



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
    teacher = TextField('Teacher Name (Last Only)', [validators.Length(min=2, max=25)])
    classname = TextField('Class Name - i.e. English III', [validators.Length(min=2, max=25)])
    dif = SelectField('Difficulty', choices=[
        ('N/A', 'N/A'),
        ('Level', 'Level'),
        ('Honors', 'Honors'),
        ('Pre-AP', 'Pre-AP'),
        ('Dual Credit', 'Dual Credit'),
        ('AP', 'AP')
    ])
    period = SelectField('Period', choices=[
        (1, '1st'),
		(2, '2nd'),
		(3, '3rd'),
		(4, '4th'),
		(5, '5th'),
		(6, '6th'),
		(7, '7th')
    ], coerce=int)

class ScheduleForm(Form):
    period1 = SelectField('period1', [validators.Required()], choices=[(x, x) for x in range(300)], coerce=int) # lol idk
    period2 = SelectField('period2', [validators.Required()], choices=[(x, x) for x in range(300)], coerce=int)
    period3 = SelectField('period3', [validators.Required()], choices=[(x, x) for x in range(300)], coerce=int)
    period4 = SelectField('period4', [validators.Required()], choices=[(x, x) for x in range(300)], coerce=int)
    period5 = SelectField('period5', [validators.Required()], choices=[(x, x) for x in range(300)], coerce=int)
    period6 = SelectField('period6', [validators.Required()], choices=[(x, x) for x in range(300)], coerce=int)
    period7 = SelectField('period7', [validators.Required()], choices=[(x, x) for x in range(300)], coerce=int)



from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, \
     check_password_hash

from forms import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nerds.db'
db = SQLAlchemy(app)

app.secret_key = 'QWERTYUIOPASDFGHJKLZXCVBNM'


"""
      ********************************
      **********   MODELS   **********
      ********************************
"""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    email = db.Column(db.String(50), unique=True)
    pwhash = db.Column(db.Binary(20)) #use hex and unhex
    schedID = db.Column(db.ForeignKey('schedule.id'))

    def __init__(self, first, last, mail, pw):
        self.firstname = first
        self.lastname = last
        self.email = mail
        self.pwhash = generate_password_hash(pw)
        self.schedID = 0;

    def check_password(self, password):
        return check_password_hash(self.pwhash, password)

    def set_schedule(self, id):
        self.schedID = id


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.ForeignKey('class.id'))
    second = db.Column(db.ForeignKey('class.id'))
    third = db.Column(db.ForeignKey('class.id'))
    fourth = db.Column(db.ForeignKey('class.id'))
    fifth = db.Column(db.ForeignKey('class.id'))
    sixth = db.Column(db.ForeignKey('class.id'))
    seventh = db.Column(db.ForeignKey('class.id'))

    def __init__(self, fir, sec, thi, fou, fif, six, sev):
        self.first = fir
        self.second = sec
        self.third = thi
        self.fourth = fou
        self.fifth = fif
        self.sixth = six
        self.seventh = sev

    def change_sched(self, fir, sec, thi, fou, fif, six, sev):
        self.first = fir
        self.second = sec
        self.third = thi
        self.fourth = fou
        self.fifth = fif
        self.sixth = six
        self.seventh = sev


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.String(20))
    dif = db.Column(db.String(10))
    period = db.Column(db.Integer)

    def __init__(self, teach, df, per):
        teacher = teach
        dif = df
        period = per

    def __repr__(self):
        return "" + self.dif + " " + self.teacher + " " + self.period



"""
      *********************************
      **********   ROUTING   **********
      *********************************
"""

@app.route('/')
def index():
    return render_template('base.html')

@app.route("/register/", methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        create_user(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
        flash('Your account was successfully created. Welcome, ' + form.first_name.data + "!")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login/", methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            flash('logged in as ' + user.firstname + " " + user.lastname)
            session["user_id"] = user.id
            session["firstlast"] = user.firstname + " " + user.lastname
            return redirect(url_for('index')) # or myprofile?
        else:
            flash('incorrect email or password')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', form=form)

@app.route('/logout/')
def logout():
    if "user_id" in session:
        session["user_id"] = ""
        print "logged out"
        flash("logged out")
    return redirect(url_for('index'))

@app.route('/class/<int:class_id>/')
def class_overview(class_id):
    return redirect(url_for('index'))

@app.route('/edit/', methods=['GET','POST'])
def class_edit():
    form = ScheduleForm(request.form)
    if request.method == 'POST' and form.validate():
        class1id = create_class(form.c1_teacher.data, form.c1_dif.data, form.c1_period.data)
        class2id = create_class(form.c2_teacher.data, form.c2_dif.data, form.c2_period.data)
        class3id = create_class(form.c3_teacher.data, form.c3_dif.data, form.c3_period.data)
        class4id = create_class(form.c4_teacher.data, form.c4_dif.data, form.c4_period.data)
        class5id = create_class(form.c5_teacher.data, form.c5_dif.data, form.c5_period.data)
        class6id = create_class(form.c6_teacher.data, form.c6_dif.data, form.c6_period.data)
        class7id = create_class(form.c7_teacher.data, form.c7_dif.data, form.c7_period.data)
        schedule = Schedule(class1id, class2id, class3id, class4id, class5id, class6id, class7id)

    if "user_id" in session:
        flash("schedule changed")
    else:
        flash("You need to log in to edit your schedule")
    return redirect(url_for('index'))

@app.route('/createclass/', methods=['GET','POST'])


@app.route('/user/<int:user_id>/')
def user_overview(user_id):
    if User.query.filter_by(id=user_id).first() is not None: #if it's a real user
        schedule = get_schedule(user_id)
        return render_template('user_overview.html', schedule=schedule)
    else:
        flash("that user does not exist")
        return redirect(url_for('index'))

@app.route('/secretclubhouse/')
def secret_clubhouse():
    return "no girls allowed!"


def create_user(fn, ln, email, pw):
    new_user = User(fn, ln, email, pw)
    db.session.add(new_user)
    db.session.commit()
    return new_user.id

def create_schedule(c1, c2, c3, c4, c5, c6, c7):
    new_schedule = Schedule(c1, c2, c3, c4, c5, c6, c7)
    db.session.add(new_schedule)
    db.session.commit()
    return new_schedule.id

def create_class(teach, dif, per):
    new_class = Class(teach, dif, per)
    db.session.add(new_schedule)
    db.session.commit()
    return new_class.id


#returns a list of classes
def get_schedule(user_id):
    user = User.query.filter_by(id=session["user_id"]).first()
    if user.schedID == 0: return []
    schedule = Schedule.query.filter_by(id=user.schedID)
    return [
        Class.query.filter_by(id=schedule.first).first(),
        Class.query.filter_by(id=schedule.second).first(),
        Class.query.filter_by(id=schedule.third).first(),
        Class.query.filter_by(id=schedule.fourth).first(),
        Class.query.filter_by(id=schedule.fifth).first(),
        Class.query.filter_by(id=schedule.sixth).first(),
        Class.query.filter_by(id=schedule.seventh).first()]


if __name__ == "__main__":
    app.run(debug=True)
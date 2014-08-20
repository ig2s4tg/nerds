from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mobility import Mobility
from flask.ext.mobility.decorators import mobile_template
from werkzeug.security import generate_password_hash, \
     check_password_hash

from forms import *

app = Flask(__name__)
Mobility(app)
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
        db.session.commit()


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period1 = db.Column(db.ForeignKey('class.id'))
    period2 = db.Column(db.ForeignKey('class.id'))
    period3 = db.Column(db.ForeignKey('class.id'))
    period4 = db.Column(db.ForeignKey('class.id'))
    period5 = db.Column(db.ForeignKey('class.id'))
    period6 = db.Column(db.ForeignKey('class.id'))
    period7 = db.Column(db.ForeignKey('class.id'))

    def __init__(self, fir, sec, thi, fou, fif, six, sev):
        self.period1 = fir
        self.period2 = sec
        self.period3 = thi
        self.period4 = fou
        self.period5 = fif
        self.period6 = six
        self.period7 = sev

    def change_sched(self, fir, sec, thi, fou, fif, six, sev):
        self.period1 = fir
        self.period2 = sec
        self.period3 = thi
        self.period4 = fou
        self.period5 = fif
        self.period6 = six
        self.period7 = sev


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.String(20))
    classname = db.Column(db.String(30))
    dif = db.Column(db.String(10))
    period = db.Column(db.Integer)

    def __init__(self, teach, cn, df, per):
        self.teacher = teach
        self.classname = cn
        self.dif = df
        self.period = per

"""
      *********************************
      **********   ROUTING   **********
      *********************************
"""

@app.route('/')
@mobile_template('{mobile/}index.html')
def index(template):
    return render_template(template)

@app.route("/register/", methods=['GET','POST'])
@mobile_template('{mobile/}register.html')
def register(template):
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        create_user(form.first_name.data.title(), form.last_name.data.title(), form.email.data, form.password.data)
        flash('Your account was successfully created. Welcome, ' + form.first_name.data.title() + "!", "success")
        return redirect(url_for('login'))
    return render_template(template, form=form)

@app.route("/login/", methods=['GET','POST'])
@mobile_template('{mobile/}login.html')
def login(template):
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            flash('logged in as ' + user.firstname + " " + user.lastname, "success")
            session["user_id"] = user.id
            session["firstlast"] = user.firstname + " " + user.lastname
            return redirect(url_for('index')) # or myprofile?
        else:
            flash('incorrect email or password', "danger")
            return redirect(url_for('login'))
    else:
        return render_template(template, form=form)

@app.route('/logout/')
def logout():
    if "user_id" in session:
        session["user_id"] = ""
        flash("logged out", "info")
    return redirect(url_for('index'))

@app.route('/edit/', methods=['GET','POST'])
@mobile_template('{mobile/}edit_sched.html')
def edit(template):
    form = ScheduleForm(request.form)
    if "user_id" in session:
        if request.method == 'POST' and form.validate():

            scheduleID = create_schedule(
                form.period1.data,
                form.period2.data,
                form.period3.data,
                form.period4.data,
                form.period5.data,
                form.period6.data,
                form.period7.data
            )
            User.query.filter_by(id=session["user_id"]).first().set_schedule(scheduleID)
            flash("schedule edited", "success")
            return redirect(url_for('user_overview', user_id=session["user_id"]))
        else:
            form.period1.choices = [(c.id, c.teacher + " - " + c.dif + " " + c.classname) for c in Class.query.filter_by(period=1).order_by("teacher").all()]
            form.period2.choices = [(c.id, c.teacher + " - " + c.dif + " " + c.classname) for c in Class.query.filter_by(period=2).order_by("teacher").all()]
            form.period3.choices = [(c.id, c.teacher + " - " + c.dif + " " + c.classname) for c in Class.query.filter_by(period=3).order_by("teacher").all()]
            form.period4.choices = [(c.id, c.teacher + " - " + c.dif + " " + c.classname) for c in Class.query.filter_by(period=4).order_by("teacher").all()]
            form.period5.choices = [(c.id, c.teacher + " - " + c.dif + " " + c.classname) for c in Class.query.filter_by(period=5).order_by("teacher").all()]
            form.period6.choices = [(c.id, c.teacher + " - " + c.dif + " " + c.classname) for c in Class.query.filter_by(period=6).order_by("teacher").all()]
            form.period7.choices = [(c.id, c.teacher + " - " + c.dif + " " + c.classname) for c in Class.query.filter_by(period=7).order_by("teacher").all()]
            return render_template(template, form=form)

    else:
        flash("You need to log in to edit your schedule", "warning")
        return redirect(url_for('login'))

@app.route('/new_class/', methods=['GET', 'POST'])
@mobile_template('{mobile/}new_class.html')
def new_class(template):
    form = ClassForm(request.form)
    if request.method == 'POST' and form.validate():
        create_class(form.teacher.data.lower().capitalize(), cap(form.classname.data), form.dif.data, form.period.data)
        flash("class created", "success")
        return redirect(url_for('edit'))
    else:
        return render_template(template, form=form)


@app.route('/user/<int:user_id>/')
@mobile_template('{mobile/}user_overview.html')
def user_overview(template, user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None: #if it's a real user
        schedule = get_classes(user.schedID)
        if len(schedule) == 0:
            return render_template("no_sched.html", user_id=user_id)
        else:
            classmates = get_classmates(user.schedID)
            combined = combine_mates(schedule, classmates)
            return render_template(template, user=User.query.filter_by(id=user_id).first(), combined=combined)
    else:
        flash("that user does not exist", "warning")
        return render_template("no_sched.html", user_id=user_id)

@app.route('/secretclubhouse/')
def secret_clubhouse():
    return "no girls allowed!"

@app.route('/about/')
@mobile_template('{mobile/}about.html')
def about(template):
    return render_template(template)

@app.route('/search/')
@mobile_template('{mobile/}search.html')
def search(template):
    users = User.query.order_by("lastname")
    return render_template(template, users=users)

@app.route('/no_sched/')
#@mobile_template('{mobile/}no_sched.html')
def no_sched(user_id):
    return render_template("no_sched.html", user_id=user_id)

def create_user(fn, ln, email, pw):
    if User.query.filter_by(email=email).first() is None:
        new_user = User(fn, ln, email, pw)
        db.session.add(new_user)
        db.session.commit()
        return new_user.id
    else:
        flash("That email is already in use!", "danger")
        return redirect(url_for('register'))

def create_schedule(c1, c2, c3, c4, c5, c6, c7):
    new_schedule = Schedule(c1, c2, c3, c4, c5, c6, c7)
    db.session.add(new_schedule)
    db.session.commit()
    return new_schedule.id

def create_class(teach, cn, dif, per):
    print "created a new class - " + teach + " " + dif + " " + cn + " " + str(per)
    new_class = Class(teach, cn, dif, per)
    db.session.add(new_class)
    db.session.commit()
    return new_class.id

# to deal with the capitalization of Roman numerals in class names
def cap(my):
    my = my.upper().split(" ")
    new = []
    for x in my:
        if x == "I" or x == "II" or x == "III" or x == "IV" or x == "V":
            new.append(x)
        else:
            new.append(x.lower().capitalize())
    final = ""
    for x in new:
        final += str(x) + " "
    final = final[:-1]
    return final



#returns a list of classes
def get_classes(schedID):
    schedule = Schedule.query.filter_by(id=schedID).first()
    if schedule is None:
        return []
    else:
        return [
            Class.query.filter_by(id=schedule.period1).first(),
            Class.query.filter_by(id=schedule.period2).first(),
            Class.query.filter_by(id=schedule.period3).first(),
            Class.query.filter_by(id=schedule.period4).first(),
            Class.query.filter_by(id=schedule.period5).first(),
            Class.query.filter_by(id=schedule.period6).first(),
            Class.query.filter_by(id=schedule.period7).first()]

def get_schedule(schedID):
    schedule = Schedule.query.filter_by(id=schedID).first()
    if schedule is None:
        return []
    else:
        return schedule

def get_classmates(sched_id):
    schedule = Schedule.query.filter_by(id=sched_id).first()
    if schedule is None:
        return []
    else:
        all_users = User.query.all()
        all_sched = []
        period1mates = []
        period2mates = []
        period3mates = []
        period4mates = []
        period5mates = []
        period6mates = []
        period7mates = []

        for u in all_users:
            all_sched.append(get_schedule(u.schedID))

        for i in range(len(all_sched)):
            if all_sched[i] != []:
                if all_sched[i].period1 == schedule.period1:
                    period1mates.append(all_users[i])
                if all_sched[i].period2 == schedule.period2:
                    period2mates.append(all_users[i])
                if all_sched[i].period3 == schedule.period3:
                    period3mates.append(all_users[i])
                if all_sched[i].period4 == schedule.period4:
                    period4mates.append(all_users[i])
                if all_sched[i].period5 == schedule.period5:
                    period5mates.append(all_users[i])
                if all_sched[i].period6 == schedule.period6:
                    period6mates.append(all_users[i])
                if all_sched[i].period7 == schedule.period7:
                    period7mates.append(all_users[i])

        return [period1mates, period2mates, period3mates, period4mates, period5mates, period6mates, period7mates]

def combine_mates(s, m):
    n = []
    for i in range(len(s)):
        n.append([s[i], m[i]])
    return n






if __name__ == "__main__":
    app.run(debug=True)
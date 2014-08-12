from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask.ext.sqlalchemy import SQLAlchemy

from forms import *
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nerds.db'
db = SQLAlchemy(app)

app.secret_key = 'QWERTYUIOPASDFGHJKLZXCVBNM'



"""
      *********************************
      **********   ROUTING   **********
      *********************************
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register/", methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        create_user(form.first_name.data.title(), form.last_name.data.title(), form.email.data, form.password.data)
        flash('Your account was successfully created. Welcome, ' + form.first_name.data.title() + "!")
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

@app.route('/edit/', methods=['GET','POST'])
def class_edit():
    if "user_id" in session:
        form = ScheduleForm(request.form)
        if request.method == 'POST' and form.validate():
            #class1id = form.
            class2id = create_class(form.c2_teacher.data, form.c2_dif.data, form.c2_period.data)
            class3id = create_class(form.c3_teacher.data, form.c3_dif.data, form.c3_period.data)
            class4id = create_class(form.c4_teacher.data, form.c4_dif.data, form.c4_period.data)
            class5id = create_class(form.c5_teacher.data, form.c5_dif.data, form.c5_period.data)
            class6id = create_class(form.c6_teacher.data, form.c6_dif.data, form.c6_period.data)
            class7id = create_class(form.c7_teacher.data, form.c7_dif.data, form.c7_period.data)
            scheduleID = create_schedule(class1id, class2id, class3id, class4id, class5id, class6id, class7id)
            User.query.filter_by(id=session["user_id"]).first().set_schedule(scheduleID)
            flash("schedule edited")
        else: #the get
            return render_template('edit_sched.html', classes=User.query.filter_by(id=session["user_id"]).all())
    else:
        flash("You need to log in to edit your schedule")
    return redirect(url_for('index'))

@app.route('/createclass/', methods=['POST'])
def new_class():
    form = ClassForm(request.form)
    if request.method == 'POST' and form.validate():
        create_class(form.teacher.data, form.dif.data, form.period.data)


@app.route('/user/<int:user_id>/')
def user_overview(user_id):
    if User.query.filter_by(id=user_id).first() is not None: #if it's a real user
        schedule = get_schedule(user_id)
        return render_template('user_overview.html', user=User.query.filter_by(id=user_id).first(), schedule=schedule)
    else:
        flash("that user does not exist")
        return redirect(url_for('search'))

@app.route('/secretclubhouse/')
def secret_clubhouse():
    return "no girls allowed!"

@app.route('/search/')
def search():
    users = User.query.order_by("lastname")
    return render_template('search.html', users=users)

def create_user(fn, ln, email, pw):
    if User.query.filter_by(email=email).first() is None:
        new_user = User(fn, ln, email, pw)
        db.session.add(new_user)
        db.session.commit()
        return new_user.id
    else:
        flash("That email is already in use!")
        return redirect(url_for('register'))

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
    user = User.query.filter_by(id=user_id).first()
    schedule = Schedule.query.filter_by(id=user.schedID).first()
    if schedule is None:
        print "schedule is None"
        return render_template('no_sched.html')
    else:
        print "schedule is " + schedule.id
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
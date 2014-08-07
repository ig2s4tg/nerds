from flask import Flask, render_template, redirect, request, session, url_for
from sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, \
     check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nerds.db'
db = SQLAlchemy(app)

app.secret_key = 'SECRETSSECRETSARENOFUN'



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
        self.pwhash = set_password(pw)
        self.schedID = 0;

    def set_password(self, password):
        self.pwhash = generate_password_hash(password)

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






@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return render_template('base.html')

@app.route("/register/", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route("/login/", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('base.html')

@app.route('/logout/')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/class/<int:class>/')
def class_overview():
    return redirect(url_for('index'))

@app.route('/user/<int:user>/')
def user_overview():
    return redirect(url_for('index'))




#def create_user(fn, ln, email, pw):




if __name__ == "__main__":
    app.run(debug=True)
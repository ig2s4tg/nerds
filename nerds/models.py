from werkzeug.security import generate_password_hash, \
     check_password_hash

from nerds import db


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




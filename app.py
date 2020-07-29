from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #Database linking
app.config['SECRET_KEY'] = 'abababab'
db = SQLAlchemy(app)

#Database

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    blood_grp = db.Column(db.String(8))
    gender = db.Column(db.String(8))
    contact = db.Column(db.Integer)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    dept = db.Column(db.String(15))
    qual = db.Column(db.String(20))

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(50))
    allergy = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('patient.id'))
    
class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease = db.Column(db.String(25))
    med = db.Column(db.String(15))
    dos = db.Column(db.String(20))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doc_name = db.Column(db.String(50))
    patient_name = db.Column(db.String(50))
    dept = db.Column(db.String(15))
    date = db.Column(db.Integer)
    time = db.Column(db.Integer)
    status = db.Column(db.String(15), default='Pending')
    created_by_patient = db.Column(db.Integer, db.ForeignKey('patient.id'))
    created_by_doc = db.Column(db.Integer, db.ForeignKey('doctor.id'))

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_n = db.Column(db.String(50))
    doc_name = db.Column(db.String(50))
    med = db.Column(db.String(50))
    dosage = db.Column(db.Integer)
    fee = db.Column(db.Integer)
    created_by_patient = db.Column(db.Integer, db.ForeignKey('patient.id'))
    created_by_doc = db.Column(db.Integer, db.ForeignKey('doctor.id'))


@app.route('/')
def index():
    return render_template('base.html')
@app.route('/dsignup',methods=['GET','POST']) #only POST required i guess
def dsignup():
    if request.method == 'POST':
        name = request.form['dname']
        pwd = request.form['pwd']
        dept = request.form['dept']
        qual = request.form['qual']
        ob = Doctor(name=name,password=pwd,dept=dept,qual=qual)

        db.session.add(ob)
        db.session.commit()   
    return render_template('dsignup.html')
@app.route('/psignup',methods=['GET','POST']) #only POST required i guess
def psignup():
    if request.method == 'POST':
        name = request.form['pname']
        pwd = request.form['pwd']
        bg = request.form['bg']
        gender = request.form['gender']
        no = request.form['no']
        ob = Patient(name=name,password=pwd,blood_grp=bg,gender=gender,contact=no)

        db.session.add(ob)
        db.session.commit()

    return render_template('psignup.html')
@app.route('/dlogin')
def dlogin():
    return render_template('dlogin.html')
@app.route('/plogin')
def plogin():
    return render_template('plogin.html')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)


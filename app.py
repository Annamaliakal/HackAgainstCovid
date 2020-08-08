
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

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
    created_by = db.Column(db.Integer, db.ForeignKey('patient.id'))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doc_name = db.Column(db.String(50))
    patient_name = db.Column(db.String(50))
    desc = db.Column(db.String(50))
    symptoms = db.Column(db.String(75))
    dept = db.Column(db.String(15))
    date = db.Column(db.Integer)
    time = db.Column(db.Integer)
    status = db.Column(db.String(15), default='Pending')
    created_by_patient = db.Column(db.Integer, db.ForeignKey('patient.id'))
    # createdby_name= db.Column(db.String(50),db.ForeignKey('patient.id'))

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(50))
    doc_name = db.Column(db.String(50))
    med = db.Column(db.String(50))
    dosage = db.Column(db.Integer)
    fee = db.Column(db.Integer)
    direction=db.Column(db.String(100))
    created_by_patient = db.Column(db.Integer, db.ForeignKey('patient.id'))
    created_by_doc = db.Column(db.Integer, db.ForeignKey('doctor.id'))


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('pname', None)
        if name is not None:
            pwd = request.form['pwd']
            patient = Patient.query.filter_by(name=name, password=pwd).first()
            
            if patient:
                flash('Login succesful!', 'success')
                print(patient.id)
                session['patient'] = patient.id
                return redirect(url_for('pindex'))
            else:
                flash('Invalid credentials', 'danger')
                return render_template('home.html')
        else:
            name = request.form['dname']
            pwd = request.form['pwd']
            doc = Doctor.query.filter_by(name=name, password=pwd).first()

            if doc:
                flash('Login succesful!', 'success')
                print(doc.id)
                session['doctor'] = doc.id
                return redirect(url_for('dindex'))
            else:
                flash('Invalid credentials', 'danger')
                return render_template('home.html')
    else:
        return render_template('home.html')

@app.route('/dsignup',methods=['GET','POST']) #only POST required i guess
def dsignup():
    if request.method == 'POST':
        name = request.form['dname']
        pwd = request.form['pwd']
        cnf_pwd = request.form['cnf_pwd']
        dept = request.form['dept']
        qual = request.form['qual']
        ob = Doctor(name=name,password=pwd,dept=dept,qual=qual)

        if pwd == cnf_pwd:
            db.session.add(ob)
            db.session.commit()
            flash("Register succesful! Login here!", "success")
            return redirect(url_for('index'))
        
        else:
            flash("Passwords do not match! Please enter same password", "danger")
            return render_template('dsignup.html')
    return render_template('dsignup.html')

@app.route('/psignup',methods=['GET','POST']) #only POST required i guess
def psignup():
    if request.method == 'POST':
        name = request.form['pname']
        pwd = request.form['pwd']
        cnf_pwd = request.form['cnf_pwd']
        bg = request.form['bg']
        gender = request.form['gender']
        no = request.form['no']
        ob = Patient(name=name,password=pwd,blood_grp=bg,gender=gender,contact=no)

        if pwd == cnf_pwd:
            db.session.add(ob)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            flash("Passwords do not match! Please enter same password")
            return render_template('psignup.html')
    return render_template('psignup.html')


@app.route('/plogout')
def plogout():
    session.pop('patient')
    # flash('Successfully logged out!', 'success')
    return redirect(url_for('index'))

@app.route('/dlogout')
def dlogout():
    # session.pop('doctor')
    # flash('Successfully logged out!', 'success')
    return redirect(url_for('index'))

@app.route('/history',methods=['GET','POST']) #ADD history
def history():
    if request.method == 'POST':
        disease = request.form['disease']
        med = request.form['med']
        dos = request.form['dos']

        desc = request.form['desc']
        allergy = request.form['allergy']

        med_ob = Medication(disease=disease,med=med,dos=dos, created_by=session['patient'])
        db.session.add(med_ob)
        db.session.commit()

        hist_ob = History(desc=desc,allergy=allergy, created_by=session['patient'])
        db.session.add(hist_ob)
        db.session.commit() 
        flash('Entered details successfully!', 'success')
        return redirect(url_for('pindex'))
    else:
        return render_template('history.html')

@app.route('/pindex',methods=['GET','POST'])
def pindex():
    if request.method == 'GET':
        patient_id=session['patient']
        confirmed_app = Appointment.query.filter_by(created_by_patient=patient_id,status='Confirmed').all()
        presc= Prescription.query.filter_by(created_by_patient=patient_id).all() 
                                                                                                                                                
    return render_template('pindex.html',confirmed_app=confirmed_app,presc=presc)

## Kavya

@app.route('/bookAppointment', methods=['GET', 'POST'])  # Book appointment
def appointment():
    if request.method == 'GET':
        docs = Doctor.query.with_entities(Doctor.name, Doctor.dept).all()
        print(docs)
        return render_template('book_appointment.html', docs=docs)
    else:
        patient_id = session['patient']
        doc = request.form.get('doc')
        print(doc,"doc")
        patient_name = Patient.query.get(patient_id).name
        print(patient_name,"patient")
        # print(doc_id)
       
        dept = request.form.get('dept')
        print(dept,"dept")
        desc = request.form['desc']
        date = request.form['date']
        time = request.form['time']
        symptoms = request.form.getlist('symptom')
        symptoms = ', '.join(symptoms)
        print('symptoms', symptoms)
        other_symptoms = request.form.get('other symptoms')
        all_symptoms = symptoms + ', ' + other_symptoms
        print('all symptoms', all_symptoms)
        new_appointment = Appointment(doc_name=doc, patient_name=patient_name,desc=desc, dept=dept, date=date, time=time, created_by_patient=patient_id, symptoms=all_symptoms)

        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment booked. Waiting for doctor\'s confirmation','success')
        return redirect(url_for('pindex'))


@app.route('/upcomingAppointment')
def upcomingAppointment():
    doc_id = session['doctor']
    doc_name = Doctor.query.get(doc_id).name
    print(doc_id,'doc_id', doc_name, 'doc_name')
    cnf_appointments = Appointment.query.filter_by(doc_name=doc_name, status='Confirmed').all()
    print(cnf_appointments)
    return render_template('upcomingAppointment.html', cnf_appointments=cnf_appointments)

@app.route('/previousAppointment')
def previousAppointment():
    doc_id = session['doctor']
    doc_name = Doctor.query.get(doc_id).name
    print(doc_id,'doc_id', doc_name, 'doc_name')
    cnf_appointments = Appointment.query.filter_by(doc_name=doc_name, status='Completed').all()
    print(cnf_appointments)
    return render_template('previousAppointment.html', cnf_appointments=cnf_appointments)


@app.route('/todayAppointments')
def todayAppointments():
    today = date.today()
    todayAppointments = Appointment.query.filter_by(date=today).all()
    return render_template('todayAppointments.html', todayAppointments=todayAppointments)

# @app.route('/dAppointment')
# def d_viewAppointment():
#     name = Doctor.query.get(session['doctor']).name
#     appointments = Appointment.query.with_entities(Appointment.doc_name).all()
#     print(name, "name")
#     print(appointments, "apps")
#     return render_template('dAppointment.html', appointments=appointments)


############## Swathi

@app.route('/dindex')
def dindex():
    doc_id=session['doctor']
    docname=Doctor.query.get(doc_id).name
    print(docname)
    appointments=Appointment.query.filter_by(doc_name=docname,status='Pending').all()
    print(appointments)
    today = date.today()
    todayAppointments = Appointment.query.filter_by(date=today).all()
    return render_template('dindex.html',appointments=appointments, todayAppointments=todayAppointments)

@app.route('/Confirm')
def Confirm():
    id=request.args['id']
    confirmed_appointments=Appointment.query.filter_by(id=id).first()
    confirmed_appointments.status='Confirmed'
    db.session.commit()
    return redirect(url_for('dindex'))

@app.route('/Deny')
def Deny():
    id=request.args['id']
    denied_appointments=Appointment.query.filter_by(id=id).first()
    denied_appointments.status='Denied'
    db.session.commit()
    return redirect(url_for('dindex'))
# updated #
@app.route('/prescription',methods=['POST','GET'])
def prescriptions():
    if request.method=="POST":
        doc_id=session['doctor']
        print(doc_id)
        cid=request.args['id']
        #user_id=request.args.get('id')
        #print(user_id)
        doc_name=Doctor.query.get(doc_id).name
        patient_name=request.form['pname']
        medicines=request.form['med']
        dosage=request.form['dos']
        fee=request.form['fee']
        direction=request.form['dir']
        ob=Prescription(patient_name=patient_name,med=medicines,dosage=dosage,fee=fee,doc_name=doc_name,direction=direction,created_by_patient=cid,created_by_doc=doc_id)
        db.session.add(ob)
        db.session.commit()
        return redirect(url_for('dindex'))
    else:
        return render_template('prescription.html')
# updated #

@app.route('/pbase')
def pbase():
    return render_template('pbase.html')

@app.route('/UserviewAppointments')
def UserviewAppointments():
    username =Patient.query.get(session['patient']).name
    print(username)
    myAppointments = Appointment.query.filter_by(createdby_name=username).all()
    return render_template('viewall_appointment.html', myAppointments=myAppointments)

@app.route('/viewhistory')
def viewhistory():
    id = session['patient']
    print(id)
    diseases = History.query.filter_by(created_by=id).all()
    medicines = Medication.query.filter_by(created_by=id).all()
    return render_template('viewhistory.html', diseases=diseases, medicines=medicines)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)


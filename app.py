import os
from flask import Flask, render_template, request, flash, redirect, url_for
import login as db
import datetime as dt

app = Flask(__name__)
app.secret_key = 'we_are_56'

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login_signup', methods=['POST'])
def login_signup():
    loginorsignup=request.form.get('loginorsignup')
    usertype = request.form.get('usertype')
    if (loginorsignup=='login'):
        _username = request.form.get('username')
        _password = request.form.get('password')
        x_id, x_name = db.validate_login(usertype, _username, _password)
        if (x_id):
            if usertype == 'doctor':
                return login_doctor(x_id, x_name)
            elif usertype == 'patient':
                return login_patient(x_id, x_name)
            elif usertype == 'pharmacy':
                return login_pharmacy(x_id, x_name)
            elif usertype == 'clinic':
                return login_clinic(x_id, x_name)
        else:
            print('Wrong Credentials!')
            flash('Wrong Credentials')
            return redirect(url_for('home'))
    elif (loginorsignup=='signup'):
        _username=request.form.get('username')
        _password=request.form.get('password')
        return render_template("signup.html",usertype=usertype,username=_username,password=_password)
        # return redirect(url_for('signup',username=_username, password = _password, usertype=usertype))
    # else:
    #     flash('Please try again')
    #     return redirect(url_for('home'))

# @app.route('/signup',methods=['GET','POST'])
# def signup():
#     usertype = request.args.get('usertype')
    
#     return render_template("signup.html",usertype=usertype)

@app.route('/book_appointment',methods=['POST'])
def book_appointment():
    p_id = request.form.get('p_id')
    print(p_id, 'wex')
    specializations = db.get_specializations()
    return render_template("bookappointment.html",specializations = specializations, p_id = p_id)

@app.route('/select_specialization',methods=['POST'])
def select_specialization():
    p_id = request.form.get('p_id')
    specialization = request.form.get('specialization')
    clinics = db.get_clinics_with_specialization(specialization)
    return render_template("bookappointment.html",p_id = p_id, specializations = [specialization], specialization = specialization, clinics=clinics)

@app.route('/select_clinic',methods=['POST'])
def select_clinic():
    c_id, c_name = request.form.get('clinic').split(',')
    specialization,p_id = request.form.get('specialization').split(',')
    doctors = db.get_clinic_sp_docs(c_id, specialization)
    print(specialization, c_id)
    return render_template("bookappointment.html",p_id = p_id, specializations = [specialization], specialization = specialization, clinics=[(c_id, c_name)], clinic = c_id, doctors = doctors)

@app.route('/select_doctor',methods=['POST'])
def select_doctor():
    d_id, d_name = request.form.get('doctor').split(',')
    p_id, specialization, c_id = request.form.get('specialization_clinic').split(',')
    c_name = db.get_c_name(c_id)
    schedules = db.get_doc_schedules(d_id, c_id)
    timings = generate_timings(schedules)
    print(timings, specialization)
    print(p_id,'adext')
    return render_template("bookappointment.html",p_id = p_id,specializations = [specialization], specialization = specialization, clinics=[(c_id, c_name)], clinic = c_id, doctors = [(d_id,d_name)], doctor = d_id, timings = timings)

@app.route('/confirm_booking',methods=['POST'])
def confirm_booking():
    timing = request.form.get('timing')
    description = request.form.get('description')
    p_id, specialization, c_id, d_id = request.form.get('specialization_clinic_doc').split(',')
    c_name = db.get_c_name(c_id)
    d_name = db.get_d_name(d_id)
    p_name = db.get_p_name(p_id)
    db.new_appointment(p_id, d_id, c_id, timing, description)
    return login_patient(p_id, p_name)



@app.route('/new_app',methods=['POST'])
def new_app():
    disease=request.form.get('disease')
    doctor=request.form.get('doctor')
    clinic = request.form.get('clinic')
    timing = request.form.get('timing')
    # add new appointment
    return render_template('patient.html')

@app.route('/showmedicalhistory',methods=['POST'])
def showmedicalhistory():
    return render_template('showmedicalhistory.html',allergies=['skin'],diabetes=['high'],blood_pressure=[],infections=['common cold'],fmly_his=[],sur_his=['appendix'])

@app.route('/treat_patient',methods=['POST'])
def treat_patient():
    a_id, p_id, p_name = request.form.get('a_id').split(',')
    past_prescriptions = db.get_past_prescriptions(p_id)
    allergies, diabetes, bp, infections, fam_history, surgical_history = db.get_medical_history(p_id)
    past_reports = db.get_past_reports(p_id)
    return render_template("treatpatient.html",a_id = a_id, p_id = p_id, name = p_name, past_pres=past_prescriptions,allergies=allergies,diabetes=diabetes,bp=bp,infections=infections,fam_history=fam_history,surgical_history=surgical_history,past_reports=past_reports)

@app.route('/new_prescription',methods=['POST'])
def new_prescription():
    a_id, p_id, p_name = request.form.get('a_id').split(',')
    meds = request.form.get('new_pres')
    d_id = db.get_d_id_from_a_id(a_id)
    db.add_prescription(p_id, d_id, meds)
    past_prescriptions = db.get_past_prescriptions(p_id)
    allergies, diabetes, bp, infections, fam_history, surgical_history = db.get_medical_history(p_id)
    past_reports = db.get_past_reports(p_id)
    return render_template("treatpatient.html",a_id = a_id, p_id = p_id, name = p_name, past_pres=past_prescriptions,allergies=allergies,diabetes=diabetes,bp=bp,infections=infections,fam_history=fam_history,surgical_history=surgical_history,past_reports=past_reports)


@app.route('/add_med_history',methods=['POST'])
def add_med_history():
    type_disease,a_id, p_id, p_name = request.form.get('type_disease').split(',')
    new_med_history = request.form.get('new_med_history')
    db.add_medical_history(p_id, type_disease, new_med_history)
    past_prescriptions = db.get_past_prescriptions(p_id)
    allergies, diabetes, bp, infections, fam_history, surgical_history = db.get_medical_history(p_id)
    past_reports = db.get_past_reports(p_id)
    return render_template("treatpatient.html",a_id = a_id, p_id = p_id, name = p_name, past_pres=past_prescriptions,allergies=allergies,diabetes=diabetes,bp=bp,infections=infections,fam_history=fam_history,surgical_history=surgical_history,past_reports=past_reports)
    # return render_template("treatpatient.html",name = p_name, past_pres=past_prescriptions,allergies=allergies,diabetes=diabetes,bp=bp,infections=infections,fam_history=fam_history,surgical_history=surgical_history,past_reports=past_reports)

@app.route('/add_report',methods=['POST'])
def add_report():
    a_id, p_id, p_name = request.form.get('a_id').split(',')
    symptoms = request.form.get('symptoms')
    disease = request.form.get('disease')
    test_req = request.form.get('test_req')
    test_rep = request.form.get('test_rep')
    d_id = db.get_d_id_from_a_id(a_id)
    db.add_report(p_id, d_id, symptoms, disease, test_req, test_rep)
    past_prescriptions = db.get_past_prescriptions(p_id)
    allergies, diabetes, bp, infections, fam_history, surgical_history = db.get_medical_history(p_id)
    past_reports = db.get_past_reports(p_id)
    return render_template("treatpatient.html",a_id = a_id, p_id = p_id, name = p_name, past_pres=past_prescriptions,allergies=allergies,diabetes=diabetes,bp=bp,infections=infections,fam_history=fam_history,surgical_history=surgical_history,past_reports=past_reports)

@app.route('/reschedule_app',methods=['POST'])
def reschedule_app():
    temp=request.form.get('reschedule')
    who =temp[:6]
    if(who=='doctor'):
        a_id=temp[6:]
    elif(who=='patien'):
        a_id = temp[6:]
        _sel_disease = db  # get from db
        _sel_doctor = db  # get from db
        _sel_clinic = db  # get from db
        _sel_timing = db  # get from db
        return render_template("rescheduleappointment.html",who=who,a_id=a_id,sel_disease=_sel_disease, sel_doctor=_sel_doctor,sel_clinic=_sel_clinic, sel_timing=_sel_timing, diseases=['malaria', "common cold"],clinics=['apollo', 'mars hospital'], doctors=['dr. vats', 'dr.ramesh'],timings=['9:00AM - 09:30 AM', '04:15PM - 04:45 PM'])
    elif(who=='clinic'):
        a_id = temp[7:]
    else:
        print('invalid')
    return

@app.route('/update_app',methods=['POST'])
def update_app():
    temp = request.form.get('update')
    who = temp[:6]
    if (who == 'doctor'):
        a_id = temp[6:]
    elif (who == 'patien'):
        a_id = temp[6:]
    elif (who == 'clinic'):
        a_id = temp[7:]
    else:
        print('invalid')
    return

@app.route('/cancel_app',methods=['POST'])
def cancel_app():
    temp = request.form.get('reschedule')
    who = temp[:6]
    if (who == 'doctor'):
        a_id = temp[6:]
    elif (who == 'patien'):
        a_id = temp[6:]
    elif (who == 'clinic'):
        a_id = temp[7:]
    else:
        print('invalid')
    return

@app.route('/new_pres',methods=['POST'])
def new_pres():
#    add prescription to db
    a_id=request.form.get('treat')
    _username=request.form.get('')  # get from a_id
    return render_template('treatpatient.html',name=_username,past_pres=['sensodyne toothpaste'],allergies=['skin'],diabetes=['high'],blood_pressure=[],infections=['common cold'],fmly_his=[],sur_his=['appendix'],past_reports=['stomach pain','gas','ultrasound','normal'])

@app.route('/manage_schedule',methods=['POST'])
def manage_schedule():
    #  doctor schedule
    return render_template('manageschedule.html',monday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],tuesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],wednesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],thursday=[],friday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],saturday=[],sunday=[])

@app.route('/update_schedule',methods=['POST'])
def update_schedule():
    #  doctor schedule
    _day=request.form.get('day')
    return render_template('updateschedule.html',day=_day,timings=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'])

@app.route('/update_delete_time',methods=['POST'])
def update_delete_time():
    temp=request.form.get('update_or_delete')
    updateordelete=temp[:6]
    if (updateordelete=='update'):
        index=temp[6:]
    #     update doctor schedule db
    elif (updateordelete=='delete'):
        index = temp[6:]
    #     delete form doctor schedule db
    else:
        print('invalid')
    return render_template('manageschedule.html',monday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],tuesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],wednesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],thursday=[],friday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],saturday=[],sunday=[])

@app.route('/add_time',methods=['POST'])
def add_time():
    openingtime = request.form.get('openingtime')
    closingtime = request.form.get('closingtime')
    # add time to doctor schedule db
    return render_template('manageschedule.html',monday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],tuesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],wednesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],thursday=[],friday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],saturday=[],sunday=[])

@app.route('/manage_timings',methods=['POST'])
def manage():
    # for clinic
    return render_template('manageschedule.html',monday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],tuesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],wednesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],thursday=[],friday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],saturday=[],sunday=[])

@app.route('/update_timings',methods=['POST'])
def update():
    # for clinic
    _day=request.form.get('day')
    return render_template('updateschedule.html',day=_day,timings=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'])

@app.route('/update_delete_timings',methods=['POST'])
def update_delet_time():
    temp=request.form.get('update_or_delete')
    updateordelete=temp[:6]
    if (updateordelete=='update'):
        index=temp[6:]
    #     update db clinic
    elif (updateordelete=='delete'):
        index = temp[6:]
    #     delete form db clinic
    else:
        print('invalid')
    return render_template('manageschedule.html',monday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],tuesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],wednesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],thursday=[],friday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],saturday=[],sunday=[])

@app.route('/add_timings',methods=['POST'])
def add_times():
    openingtime = request.form.get('openingtime')
    closingtime = request.form.get('closingtime')
    # add time to db clinic
    return render_template('manageschedule.html',monday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],tuesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],wednesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],thursday=[],friday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],saturday=[],sunday=[])

@app.route('/update_profile',methods=['POST'])
def update_profile():
    usertype=request.form.get('profile_type')
    print(usertype)
    if usertype == 'patient':
        return render_template("profile.html",usertype=usertype, name='Rishab',sex='male', age='20', contact=9876543210)
    elif usertype == 'doctor':
        return render_template("profile.html",usertype=usertype,name='Shashwat',specialization='heart',contact=9876543210,fee=300)
    elif usertype == 'pharmacy':
        return render_template("profile.html", usertype=usertype,name='Apollo pharmacy',contact=9876543210)
    elif usertype == 'clinic':
        return render_template("profile.html",usertype=usertype,name='Mars hospital',address='Delhi',contact=9876543210 )
    return

@app.route('/new_doctor', methods=['POST'])
def new_doctor():
    name = request.form.get('d_name')
    specialization = request.form.get('specialization')
    phone = request.form.get('phone')
    fee = request.form.get('fee')
    username = request.form.get('username')
    password = request.form.get('password')
    d_id = db.new_doctor(name, specialization, fee, phone, username, password)
    return login_doctor(d_id, name)


@app.route('/new_patient', methods=['POST'])
def new_patient():
    name = request.form.get('p_name')
    sex = request.form.get('sex')
    age = request.form.get('age')
    phone = request.form.get('phone')
    username = request.form.get('username')
    password = request.form.get('password')
    p_id = db.new_patient(name, sex, age, phone, username, password)
    return login_patient(p_id, name)

@app.route('/new_clinic', methods=['POST'])
def new_clinic():
    name = request.form.get('c_name')
    days = request.form.getlist('days')
    openingtime = request.form.get('openingtime')
    closingtime = request.form.get('closingtime')
    address = request.form.get('address')
    phone = request.form.get('phone')
    username = request.form.get('username')
    password = request.form.get('password')
    c_id = db.new_clinic(name, address, phone, username, password)
    for day in days:
        db.add_clinic_timing(c_id, day, openingtime, closingtime)
    return login_clinic(c_id, name)

# @app.route('/treat_patient', methods=['POST'])
# def treat_patient():
#     a_id = request.form.get('a_id')
#     return a_id

@app.route('/doc_cancel_appointment', methods=['POST'])
def doc_cancel_appointment():
    a_id = request.form.get('a_id')
    d_id, d_name = db.get_appointment_doc(a_id)
    db.delete_appointment(a_id)
    return login_doctor(d_id, d_name)

@app.route('/clinic_cancel_appointment', methods=['POST'])
def clinic_cancel_appointment():
    a_id = request.form.get('a_id')
    c_id, c_name = db.get_appointment_clinic(a_id)
    db.delete_appointment(a_id)
    return login_clinic(c_id, c_name)

@app.route('/clinic_doctors', methods=['POST'])
def clinic_doctors():
    c_id = request.form.get('c_id')
    doctors = db.view_clinic_docs(c_id)
    return doctors


def login_doctor(d_id, d_name):
    appointments = db.view_doc_upcoming_appointments(d_id)
    print(appointments)
    return render_template("doctor.html", name=d_name, appointments=appointments)

def login_patient(p_id, p_name):
    appointments = db.view_patient_upcoming_appointments(p_id)
    print(p_id, 'adsf')
    return render_template("patient.html", p_id=p_id, name=p_name, appointments = appointments)

def login_pharmacy(pharma_id, pharma_name):
    return render_template("pharmacy.html",name=pharma_name)

def login_clinic(c_id, c_name):
    appointments = db.view_clinic_upcoming_appointments(c_id)
    return render_template("clinic.html",name=c_name, c_id = c_id, appintments=appointments)

@app.route('/fetch_prescriptions', methods=['POST'])
def fetch_prescriptions():
    _username = request.form.get('username')
    prescriptions = db.get_prescriptions(_username)
    if len(prescriptions) == 0:
        prescriptions = 0
    print(prescriptions)
    print('yoyoyo')
    return render_template("pharmacy.html", name='', prescriptions=prescriptions)


def generate_timings(schedules):
    int_day = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
    timings = []
    for schedule in schedules:
        date = dt.date.today()
        today_date = dt.date.today()
        # time_now = round_time(dt.datetime.now()).time()
        print(type((schedule[1] + dt.datetime.min).time()))
        print(type(schedule[1]))
        print(type(schedule[2]))
        start_time = (schedule[1] + dt.datetime.min).time()
        end_time = (schedule[2] + dt.datetime.min).time()
        while (date.weekday() != int_day[schedule[0].lower()]):
            date += dt.timedelta(days=1)
        start_datetime = dt.datetime.combine(date, start_time)
        end_datetime = dt.datetime.combine(date, end_time)
        if (date != today_date):
            date = start_datetime
        else:
            date = round_time(dt.datetime.now())

        while(end_datetime >=    date + dt.timedelta(minutes = 15)):
            timings.append(date)
            date = date + dt.timedelta(minutes = 15)
    return timings

def round_time(dat=None, round_to=60*15):
   if dat == None: 
       dat = dt.datetime.now()
   seconds = (dat - dat.min).seconds
   rounding = (seconds+round_to/2) // round_to * round_to
   return dat + dt.timedelta(0,rounding-seconds,-dat.microsecond)
            

if __name__ == '__main__':
    # app.jinja_env.globals.update(get_i=get_i)
    app.run(debug = True)
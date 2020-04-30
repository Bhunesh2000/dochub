import os
from flask import Flask, render_template, request, flash, redirect, url_for
import queries as db
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
    return render_template("bookappointment.html",p_id = p_id, specializations = [specialization], specialization = specialization, clinics=[(c_id, c_name)], clinic = c_id, doctors = doctors)

@app.route('/select_doctor',methods=['POST'])
def select_doctor():
    d_id, d_name = request.form.get('doctor').split(',')
    p_id, specialization, c_id = request.form.get('specialization_clinic').split(',')
    c_name = db.get_c_name(c_id)
    schedules = db.get_doc_schedules(d_id, c_id)
    timings = generate_timings(schedules)
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
    a_id, p_id, p_name = request.form.get('a_id_p_id_name').split(',')
    allergies = request.form.get('allergies')
    diabetes = request.form.get('diabetes')
    bp = request.form.get('bp')
    infectious_diseases = request.form.get('infectious_diseases')
    family_history = request.form.get('family_history')
    surgical_history = request.form.get('surgical_history')
    db.add_medical_history(p_id, allergies, diabetes, bp, infectious_diseases, family_history, surgical_history)
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


@app.route('/manage_schedule',methods=['POST'])
def manage_schedule():
    d_id = request.form.get('d_id')
    schedules = db.get_doc_schedules(d_id)
    clinics = db.get_doc_clinics(d_id)
    return render_template('manageschedule.html', schedules = schedules, d_id = d_id, clinic_list = clinics)

@app.route('/remove_schedule',methods=['POST'])
def remove_schedule():
    schedule_id, d_id = request.form.get('schedule_id')
    db.remove_schedule(schedule_id)
    schedules = db.get_doc_schedules(d_id)
    clinics = db.get_doc_clinics(d_id)
    return render_template('manageschedule.html', schedules = schedules, d_id = d_id, clinic_list = clinics)

@app.route('/add_schedule_select_clinic',methods=['POST'])
def add_schedule_select_clinic():
    c_id = request.form.get('clinic')
    d_id = request.form.get('d_id')
    c_name = db.get_c_name(c_id)
    schedules = db.get_doc_schedules(d_id)
    clinic_timings = db.get_clinic_timings(c_id)
    return render_template('manageschedule.html', schedules = schedules, d_id = d_id, clinic = c_id, clinic_list = [(c_id, c_name)], clinic_timings = clinic_timings)

@app.route('/add_schedule_select_day_slot',methods=['POST'])
def add_schedule_select_day_slot():
    d_id, c_id = request.form.get('d_id_c_id').split(',')
    c_name = db.get_c_name(c_id)
    day, start, end = request.form.get('day_time').split(',')
    schedules = db.get_doc_schedules(d_id)
    return render_template('manageschedule.html', schedules = schedules, d_id = d_id, clinic = c_id, clinic_list = [(c_id, c_name)], clinic_timings = [(day, start, end)], day = day, start = start, end = end)

@app.route('/add_schedule',methods=['POST'])
def add_schedule():
    d_id, c_id, day = request.form.get('d_id_c_id_day').split(',')
    start = request.form.get('start_time')
    end = request.form.get('end_time')
    db.add_schedule(d_id, c_id, day, start, end)
    schedules = db.get_doc_schedules(d_id)
    clinics = db.get_doc_clinics(d_id)
    return render_template('manageschedule.html', schedules = schedules, d_id = d_id, clinic_list = clinics)

    
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


@app.route('/manage_timings',methods=['POST'])
def manage_timings():
    c_id = request.form.get('c_id')
    timings = db.get_clinic_timings(c_id)
    return render_template('managetimings.html', c_id = c_id, timings = timings)

@app.route('/remove_timings',methods=['POST'])
def remove_timings():
    c_id,day, start, end = request.form.get('c_id_day_start_end')
    db.remove_clinic_timing(c_id, day, start, end)
    timings = db.get_clinic_timings(c_id)
    return render_template('managetimings.html', c_id = c_id, timings = timings)

@app.route('/add_timings',methods=['POST'])
def add_timings():
    c_id = request.form.get('c_id')
    day = request.form.get('day')
    start = request.form.get('start')
    end = request.form.get('end')
    db.add_clinic_timing(c_id, day, start, end)
    timings = db.get_clinic_timings(c_id)
    return render_template('managetimings.html', c_id = c_id, timings = timings)

# @app.route('/update_timings',methods=['POST'])
# def update():
#     # for clinic
#     _day=request.form.get('day')
#     return render_template('updateschedule.html',day=_day,timings=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'])

# @app.route('/update_delete_timings',methods=['POST'])
# def update_delet_time():
#     temp=request.form.get('update_or_delete')
#     updateordelete=temp[:6]
#     if (updateordelete=='update'):
#         index=temp[6:]
#     #     update db clinic
#     elif (updateordelete=='delete'):
#         index = temp[6:]
#     #     delete form db clinic
#     else:
#         print('invalid')
#     return render_template('manageschedule.html',monday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],tuesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],wednesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],thursday=[],friday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],saturday=[],sunday=[])

@app.route('/add_timings',methods=['POST'])
def add_times():
    openingtime = request.form.get('openingtime')
    closingtime = request.form.get('closingtime')
    # add time to db clinic
    return render_template('manageschedule.html',monday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],tuesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],wednesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],thursday=[],friday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],saturday=[],sunday=[])

@app.route('/view_profile',methods=['POST'])
def view_profile():
    usertype, user_id=request.form.get('profile_type').split(',')
    user_details, user_info = db.get_user_details(usertype, user_id)
    username, password = user_info
    if usertype == 'patient':
        name, sex, age, phone = user_details
        return render_template("profile.html",usertype=usertype, name=name,sex=sex, age=age, contact=phone, username = username, password = password, user_id = user_id)
    elif usertype == 'doctor':
        name, specialization, fee, contact = user_details
        return render_template("profile.html",usertype=usertype,name=name,specialization=specialization,contact=contact,fee=fee, username = username, password = password, user_id = user_id)
    elif usertype == 'pharmacy':
        name, phone = user_details
        return render_template("profile.html",usertype=usertype, name=name, contact=phone, username = username, password = password, user_id = user_id)
    elif usertype == 'clinic':
        name, address, phone = user_details
        return render_template("profile.html",usertype=usertype, name=name,addreess=address, contact=phone, username = username, password = password, user_id = user_id)
    return


@app.route('/view_medical_history', methods = ['POST'])
def view_medical_history():
    p_id = request.form.get('p_id')
    p_name = db.get_p_name(p_id)
    allergies, diabetes, bp, infections, fam_history, surgical_history = db.get_medical_history(p_id)
    return render_template("medical_history.html",p_id = p_id, name = p_name, allergies=allergies,diabetes=diabetes,bp=bp,infections=infections,fam_history=fam_history,surgical_history=surgical_history)

@app.route('/patient_add_med_history', methods = ['POST'])
def patient_add_med_history():
    p_id = request.form.get('p_id')
    p_name = db.get_p_name(p_id)
    allergies = request.form.get('allergies')
    diabetes = request.form.get('diabetes')
    bp = request.form.get('bp')
    infectious_diseases = request.form.get('infectious_diseases')
    family_history = request.form.get('family_history')
    surgical_history = request.form.get('surgical_history')
    db.add_medical_history(p_id, allergies, diabetes, bp, infectious_diseases, family_history, surgical_history)
    allergies, diabetes, bp, infections, fam_history, surgical_history = db.get_medical_history(p_id)
    return render_template("medical_history.html",p_id = p_id, name = p_name, allergies=allergies,diabetes=diabetes,bp=bp,infections=infections,fam_history=fam_history,surgical_history=surgical_history)


@app.route('/update_profile',methods=['POST'])
def update_profile():
    usertype, user_id=request.form.get('usertype_id').split(',')
    contact = request.form.get('contact')
    db.update_phone(usertype, user_id, contact)
    if usertype == 'doctor':
        fee = request.form.get('fee')
        db.update_doc_fee(user_id, fee)
        d_name = db.get_d_name(user_id)
        return login_doctor(user_id,d_name)
    elif usertype == 'pharmacy':
        return login_pharmacy(user_id, '')
    elif usertype == 'clinic':
        c_name = db.get_c_name(user_id)
        return login_clinic(user_id, c_name)
    elif usertype == 'patient':
        p_name = db.get_p_name(user_id)
        return login_patient(user_id, p_name)

@app.route('/change_password', methods = ['POST'])
def change_password():

    usertype, user_id = request.form.get('usertype_id').split(',')
    password = request.form.get('password')
    db.change_password(usertype, user_id, password)
    if usertype == 'doctor':
        d_name = db.get_d_name(user_id)
        return login_doctor(user_id,d_name)
    elif usertype == 'pharmacy':
        return login_pharmacy(user_id, '')
    elif usertype == 'clinic':
        c_name = db.get_c_name(user_id)
        return login_clinic(user_id, c_name)
    elif usertype == 'patient':
        p_name = db.get_p_name(user_id)
        return login_patient(user_id, p_name)


@app.route('/new_doctor', methods=['POST'])
def new_doctor():
    name = request.form.get('d_name')
    specialization = request.form.get('specialization')
    phone = request.form.get('phone')
    fee = request.form.get('fee')
    temp=request.form.get('user_pass')
    temp2=temp.split(',')
    username =temp2[0]
    password =temp2[1]
    d_id = db.new_doctor(name, specialization, fee, phone, username, password)
    return login_doctor(d_id, name)


@app.route('/new_patient', methods=['POST'])
def new_patient():
    name = request.form.get('p_name')
    sex = request.form.get('sex')
    age = request.form.get('age')
    phone = request.form.get('phone')
    temp = request.form.get('user_pass')
    temp2 = temp.split(',')
    username = temp2[0]
    password = temp2[1]
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
    temp = request.form.get('user_pass')
    temp2 = temp.split(',')
    username = temp2[0]
    password = temp2[1]
    c_id = db.new_clinic(name, address, phone, username, password)
    for day in days:
        db.add_clinic_timing(c_id, day, openingtime, closingtime)
    return login_clinic(c_id, name)

@app.route('/new_pharmacy', methods=['POST'])
def new_pharmacy():
    name = request.form.get('pharma_name')
    phone = request.form.get('phone')
    temp = request.form.get('user_pass')
    temp2 = temp.split(',')
    username = temp2[0]
    password = temp2[1]
    ph_id=db.new_pharmacy(name,phone,username,password)
    return login_pharmacy(ph_id,name)
# @app.route('/treat_patient', methods=['POST'])
# def treat_patient():
#     a_id = request.form.get('a_id')
#     return a_id
@app.route('/patient_cancel_appointment', methods=['POST'])
def patient_cancel_appointment():
    a_id = request.form.get('a_id')
    p_id, p_name = db.get_appointment_patient(a_id)
    db.delete_appointment(a_id)
    return login_patient(p_id, p_name)

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
    c_name = db.get_c_name(c_id)
    doctors = db.view_clinic_docs(c_id)
    available_doctors = db.get_clinic_available_doctor(c_id)
    return render_template("clinic_docs.html", doctors = doctors, c_id = c_id, c_name = c_name, available_doctors = available_doctors)

@app.route('/remove_clinic_doctor', methods=['POST'])
def remove_clinic_doctor():
    c_id, d_id = request.form.get('c_id_d_id').split(',')
    c_name = db.get_c_name(c_id)
    db.clinic_remove_doc(c_id, d_id)
    doctors = db.view_clinic_docs(c_id)
    available_doctors = db.get_clinic_available_doctor(c_id)
    return render_template("clinic_docs.html", doctors = doctors, c_id = c_id, c_name = c_name, available_doctors = available_doctors)

@app.route('/add_clinic_doctor', methods=['POST'])
def add_clinic_doctor():
    c_id = request.form.get('c_id')
    d_id = request.form.get('d_id')
    salary = request.form.get('salary')
    c_name = db.get_c_name(c_id)
    db.clinic_add_doc(c_id, d_id, salary)
    doctors = db.view_clinic_docs(c_id)
    available_doctors = db.get_clinic_available_doctor(c_id)
    return render_template("clinic_docs.html", doctors = doctors, c_id = c_id, c_name = c_name, available_doctors = available_doctors)

@app.route('/fetch_prescriptions', methods=['POST'])
def fetch_prescriptions():
    _username = request.form.get('username')
    pharma_name, pharma_id = request.form.get('pharma').split(',')
    prescriptions = db.get_prescriptions(_username)
    if len(prescriptions) == 0:
        prescriptions = 0
    return render_template("pharmacy.html",name=pharma_name, pharma_id = pharma_id, prescriptions=prescriptions)

@app.route('/qna', methods=['POST'])
def qna():
    qnas = db.get_answered_qs()
    return render_template("qna.html",qna=qnas)

@app.route('/ask_question', methods=['POST'])
def ask_question():
    return render_template("ask_qna.html")

@app.route('/submit_question', methods=['POST'])
def submit_question():
    question = request.form.get('question')
    db.add_question(question)
    qnas = db.get_answered_qs()
    return render_template("qna.html",qna=qnas)

@app.route('/answer_question', methods=['POST'])
def answer_question():
    questions = db.get_unanswered_qs()
    return render_template("answer_qna.html", questions = questions)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    q_id = request.form.get('q_id')
    answer = request.form.get('answer')
    db.answer_question(q_id, answer)
    questions = db.get_unanswered_qs()
    return render_template("answer_qna.html", questions = questions)

def generate_timings(schedules):
    int_day = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
    timings = []
    for schedule in schedules:
        date = dt.date.today()
        today_date = dt.date.today()
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

def login_doctor(d_id, d_name):
    appointments = db.view_doc_upcoming_appointments(d_id)
    return render_template("doctor.html", d_id = d_id, name=d_name, appointments=appointments)

def login_patient(p_id, p_name):
    appointments = db.view_patient_upcoming_appointments(p_id)
    return render_template("patient.html", p_id=p_id, name=p_name, appointments = appointments)

def login_pharmacy(pharma_id, pharma_name):
    return render_template("pharmacy.html",name=pharma_name, pharma_id = pharma_id)

def login_clinic(c_id, c_name):
    appointments = db.view_clinic_upcoming_appointments(c_id)
    return render_template("clinic.html",name=c_name, c_id = c_id, appointments=appointments)

def round_time(dat=None, round_to=60*15):
   if dat == None: 
       dat = dt.datetime.now()
   seconds = (dat - dat.min).seconds
   rounding = (seconds+round_to/2) // round_to * round_to
   return dat + dt.timedelta(0,rounding-seconds,-dat.microsecond)
            

if __name__ == '__main__':
    # app.jinja_env.globals.update(get_i=get_i)
    app.run(debug = True)
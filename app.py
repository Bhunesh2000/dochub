import os
from flask import Flask, render_template, request, flash, redirect, url_for
import login as db

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
    return render_template("bookappointment.html",diseases=['malaria',"common cold"],clinics=['apollo','mars hospital'],doctors=['dr. vats','dr.ramesh'],timings=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'])

@app.route('/treat_patient',methods=['POST'])
def treat_patient():
    a_id=request.form.get('treat')
    _username=request.form.get('')  # get from a_id
    return render_template("treatpatient.html",name=_username,past_pres=['sensodyne toothpaste'],allergies=['skin'],diabetes=['high'],blood_pressure=[],infections=['common cold'],fmly_his=[],sur_his=['appendix'],past_reports=['stomach pain','gas','ultrasound','normal'])

@app.route('/reschedule_app',methods=['POST'])
def reschedule_app():

    return

@app.route('/cancel_app',methods=['POST'])
def cancel_app():
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
def manage_schedule():
    # for clinic
    return render_template('manageschedule.html',monday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],tuesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],wednesday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],thursday=[],friday=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'],saturday=[],sunday=[])

@app.route('/update_timings',methods=['POST'])
def update_schedule():
    # for clinic
    _day=request.form.get('day')
    return render_template('updateschedule.html',day=_day,timings=['9:00AM - 09:30 AM','04:15PM - 04:45 PM'])

@app.route('/update_delete_timings',methods=['POST'])
def update_delete_time():
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
def add_time():
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


def login_doctor(d_id, d_name):
    appointments = db.view_doc_upcoming_appointments(d_id)
    print(appointments)
    return render_template("doctor.html", name=d_name, appointments=appointments)

def login_patient(p_id, p_name):
    appointments = db.view_patient_upcoming_appointments(p_id)
    print(appointments)
    return render_template("patient.html",name=p_name, appointments = appointments)

def login_pharmacy(pharma_id, pharma_name):
    return render_template("pharmacy.html",name=pharma_name)

def login_clinic(c_id, c_name):
    return render_template("clinic.html",name=c_name)

@app.route('/fetch_prescriptions', methods=['POST'])
def fetch_prescriptions():
    _username = request.form.get('username')
    prescriptions = db.get_prescriptions(_username)
    if len(prescriptions) == 0:
        prescriptions = 0
    print(prescriptions)
    print('yoyoyo')
    return render_template("pharmacy.html", name='', prescriptions=prescriptions)

if __name__ == '__main__':
    # app.jinja_env.globals.update(get_i=get_i)
    app.run(debug = True)
import stdiomask
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "apple212",
    database = "testdata"
    )
mydbcursor = mydb.cursor()

def login_patient(userID, password):
    print('patient')

def login_doctor(userID, password):
    print('doctor')

def login_clinic(userID, password):
    print('clinc')

def login_pharmacy(userID, password):
    print('pharmacy')

def insert(query):
    global mydb, mydbcursor
    try:
        mydbcursor.execute(query)
        mydb.commit()
        print('Added Successfully!')
    except mysql.connector.errors.IntegrityError as e:
        print('Duplicate Entry!')

def update(query):
    global mydb, mydbcursor
    try:
        mydbcursor.execute(query)
        mydb.commit()
        print('Updated Successfully!')
    except mysql.connector.errors.IntegrityError as e:
        print('Duplicate Entry!')
        

def login():
    print('\n-------- Welcome to DocHub Login --------\n')
    option = 0
    while(option<1 or option>4):
        print('Login as:\t1. Patient \t 2. Doctor \t 3. Clinic \t 4. Pharmacy')
        option = int(input())
        if (option >=1 and option <=4):
            userID = input('Username: ')
            password = stdiomask.getpass()
            print(userID, password)
            if (option == 1):
                login_patient(userID, password)
            elif (option == 2):
                validate_login('doctor', userID, password)
                login_doctor(userID, password)
            elif (option == 3):
                login_clinic(userID, password)
            elif (option == 4):
                login_pharmacy(userID, password)
        else :
            print('Invalid option')
            
def validate_login(user_type, username, password):
    global mydbcursor
    x_id = ''
    if(user_type == 'pharmacy'):
        user_type = 'pharmacies'
        x = 'pharma'
    else:
        user_type += 's'
        x = user_type[0]
    query = f"select {x}_id, {x}_name from {user_type} natural join login_{user_type} where username='{username}' and password='{password}';"
    mydbcursor.execute(query)
    ids = list(mydbcursor.fetchall())
    if(len(ids)==1):
        print('LOGGED IN')
        return ids[0]
    return (0,0)

def create_user(type, x_id, username, password):
    login_table = 'login_'
    x_id = ''
    if(type == 'clinic'):
        login_table += 'clinics'
    elif(type=='doctor'):
        login_table += 'doctors'
    elif(type=='patient'):
        login_table += 'patients'
    elif(type=='pharmacy'):
        login_table += 'pharmacies'
    query = f"insert into {login_table} values(NULL, {x_id}, '{username}', '{password}');"



def new_clinic(name, address, phone, username, password):
    global mydb, mydbcursor
    query = f"insert into clinics values(NULL, '{name}','{address}','{phone}')"
    mydbcursor.execute(query)
    mydb.commit()
    mydbcursor.execute("select last_insert_id()")
    c_id = mydbcursor.fetchall()[0][0]
    query = f"insert into login_clinics values(NULL, {c_id}, '{username}', '{password}')"
    mydbcursor.execute(query)
    mydb.commit()
    return c_id


def new_doctor(name, specialization, fee, phone, username, password):
    global mydb, mydbcursor
    query = f"insert into doctors values(NULL, '{name}','{specialization}', '{fee}','{phone}')"
    mydbcursor.execute(query)
    mydb.commit()
    mydbcursor.execute("select last_insert_id()")
    d_id = mydbcursor.fetchall()[0][0]
    query = f"insert into login_doctors values(NULL, {d_id}, '{username}', '{password}')"
    mydbcursor.execute(query)
    mydb.commit()
    return d_id        

def new_patient(name, sex, age, phone, username, password):
    global mydb, mydbcursor
    query = f"insert into patients values(NULL, '{name}','{sex}', {age},'{phone}')"
    mydbcursor.execute(query)
    mydb.commit()
    mydbcursor.execute("select last_insert_id()")
    p_id = mydbcursor.fetchall()[0][0]
    query = f"insert into login_patients values(NULL, {p_id}, '{username}', '{password}')"
    mydbcursor.execute(query)
    mydb.commit()
    return p_id

def new_pharmacy(name, phone, username, password):
    global mydb, mydbcursor
    query = f"insert into pharmacies values(NULL, '{name}', '{phone}')"
    mydbcursor.execute(query)
    mydb.commit()
    mydbcursor.execute("select last_insert_id()")
    pharma_id = mydbcursor.fetchall()[0][0]
    query = f"insert into login_pharmacies values(NULL, {pharma_id}, '{username}', '{password}')"
    mydbcursor.execute(query)
    mydb.commit()
    return pharma_id

def view_clinic_upcoming_appointments(c_id):
    global mydb, mydbcursor
    query = f"select a_id, p_id, p_name, d_id, d_name, schedule, description from appointments natural join doctors natural join patients where c_id = {c_id} and schedule >= now()"
    mydbcursor.execute(query)
    appointments = map(lambda x: x[:-2] + (x[-2].strftime("%d-%b-%Y %I:%M"),x[-1]) , mydbcursor.fetchall())
    appointments = list(appointments)
    return appointments

def view_clinic_past_appointments(c_id):
    global mydb, mydbcursor
    query = f"select a_id, p_id, p_name, d_id, d_name, schedule, description from appointments natural join doctors natural join patients where c_id = {c_id} and schedule < now()"
    mydbcursor.execute(query)
    appointments = map(lambda x: x[:-2] + (x[-2].strftime("%d-%b-%Y %I:%M"),x[-1]) , mydbcursor.fetchall())
    appointments = list(appointments)
    return appointments


def view_doc_upcoming_appointments(d_id, c_id = 0):
    global mydb, mydbcursor
    if(c_id):
        query = f"select a_id, p_id, p_name, c_name, schedule, description from appointments natural join clinics natural join patients where d_id = {d_id} and c_id = {c_id} and schedule >= now()"
    else:
        query = f"select a_id, p_id, p_name, c_name, schedule, description from appointments natural join clinics natural join patients where d_id = {d_id} and schedule >= now()"
    mydbcursor.execute(query)
    appointments = map(lambda x: x[:-2] + (x[-2].strftime("%d-%b-%Y %I:%M"),x[-1]) , mydbcursor.fetchall())
    appointments = list(appointments)
    return appointments

def view_doc_past_appointments(d_id, c_id = 0):
    global mydb, mydbcursor
    if(c_id):
        query = f"select a_id, p_id, p_name, c_name, schedule, description from appointments natural join clinics natural join patients where d_id = {d_id} and c_id = {c_id} and schedule < now()"
    else:
        query = f"select a_id, p_id, p_name, c_name, schedule, description from appointments natural join clinics natural join patients where d_id = {d_id} and schedule < now()"
    mydbcursor.execute(query)
    appointments = map(lambda x: x[:-2] + (x[-2].strftime("%d-%b-%Y %I:%M"),x[-1]) , mydbcursor.fetchall())
    appointments = list(appointments)
    return appointments

def view_docs():
    global mydb, mydbcursor
    query = f"select * from doctors"
    mydbcursor.execute(query)
    doctors = list(mydbcursor.fetchall())
    return doctors

def view_clinic_docs(c_id):
    global mydb, mydbcursor
    query = f"select * from doctors natural join clinic_doctors where c_id={c_id}"
    mydbcursor.execute(query)
    doctors = list(mydbcursor.fetchall())
    return doctors

def clinic_add_doc(c_id, d_id, salary):
    global mydb, mydbcursor
    query = f"insert into clinic_doctors values({d_id}, {c_id}, {salary}, date(now())) "
    mydbcursor.execute(query)
    mydb.commit()

def clinic_remove_doc(c_id, d_id):
    global mydb, mydbcursor
    query = f"DELETE FROM  clinic_doctors WHERE c_id = {c_id} and d_id = {d_id}"
    mydbcursor.execute(query)
    mydb.commit()
    query = f"DELETE FROM  schedules WHERE c_id = {c_id} and d_id = {d_id}"
    mydbcursor.execute(query)
    mydb.commit()

def view_patient_upcoming_appointments(p_id):
    global mydb, mydbcursor
    query = f"select a_id, c_name, d_name, schedule, description from appointments natural join doctors natural join clinics where p_id = {p_id} and schedule >= now()"
    mydbcursor.execute(query)
    appointments = map(lambda x: x[:-2] + (x[-2].strftime("%d-%b-%Y %I:%M"),x[-1]) , mydbcursor.fetchall())
    appointments = list(appointments)
    return appointments

def view_patient_past_appointments(p_id):
    global mydb, mydbcursor
    query = f"select a_id, c_name, d_name, schedule, description from appointments natural join doctors natural join clinics where p_id = {p_id} and schedule < now()"
    mydbcursor.execute(query)
    appointments = map(lambda x: x[:-2] + (x[-2].strftime("%d-%b-%Y %I:%M"),x[-1]) , mydbcursor.fetchall())
    appointments = list(appointments)
    return appointments


def new_appointment(p_id, d_id, c_id, datetime):
    global mydb, mydbcursor
    query = f"insert into appointments values(NULL,{p_id},{d_id},{c_id},'{datetime}')"
    insert(query)

def delete_appointment(a_id):
    global mydb, mydbcursor
    query = f"DELETE FROM appointments WHERE a_id = {a_id}"
    mydbcursor.execute(query)
    mydb.commit()

def add_schedule(d_id,c_id,day, start, end):
    query = f"insert into schedules values(NULL,{d_id},{c_id},'{day}','{start}', '{end}')"
    insert(query)

def delete_schedule(schedule_id):
    global mydb, mydbcursor
    query = f"DELETE FROM schedules WHERE schedule_id = {schedule_id}"
    mydbcursor.execute(query)
    mydb.commit()

def show_schedules(d_id):
    global mydb, mydbcursor
    query = f"select * from schedules where d_id = {d_id}"
    mydbcursor.execute(query)
    return list(mydbcursor.fetchall())

def add_clinic_timing(c_id, day, start, end):
    global mydb, mydbcursor
    query = f"insert into clinic_timings values({c_id},'{day}','{start}', '{end}')"
    mydbcursor.execute(query)
    mydb.commit()

def pharma_manageProfile(pharma_id,type,new):
    global mydb, mydbcursor
    if(type=="password"):
        query=f"update login_pharmacies set password='{new}' where pharma_id={pharma_id}"
    elif(type=="phone"):
        query=f"update pharmacies set phone='{new}' where pharma_id={pharma_id}"
    mydbcursor.execute(query)
    mydb.commit()

def patient_manageProfile(p_id,type,new):
    global mydb, mydbcursor
    if(type=="password"):
        query=f"update login_patients set password='{new}' where p_id={p_id}"
    elif(type=="phone"):
        query=f"update patients set phone='{new}' where p_id={p_id}"
    mydbcursor.execute(query)
    mydb.commit()

def doctor_manageProfile(d_id,type,new):
    global mydb, mydbcursor
    if(type=="password"):
        query=f"update login_doctors set password='{new}' where d_id={d_id}"
    elif(type=="phone"):
        query=f"update doctors set contact='{new}' where d_id={d_id}"
    elif(type=="fee"):
        query=f"update doctors set fee={new} where d_id={d_id}"
    mydbcursor.execute(query)
    mydb.commit()

def clinic_manageProfile(c_id,type,new):
    global mydb, mydbcursor
    if(type=="password"):
        query=f"update login_clinics set password='{new}' where c_id={c_id}"
    elif(type=="phone"):
        query=f"update clinics set c_phone='{new}' where c_id={c_id}"
    elif(type=="address"):
        query=f"update clinics set c_address='{new}' where c_id={c_id}"
    mydbcursor.execute(query)
    mydb.commit()

def doctorSchedule(d_id,c_id,task):
    global mydb, mydbcursor
    if(task=="remove"):
        query=f"delete from schedules where d_id={d_id} and c_id={c_id}"
    elif(task=="edit"):
        print("Select appropriate option:\t 1. Change Days \t 2. Change Start and End Timings")
        option=int(input())
        if(option==1):
            print("Enter new Days")
            newDay=input()
            query=f"update schedules set day ={newDay} where d_id={d_id} and c_id={c_id}"
        if(option==2):
            print("Enter new Start Timings")
            newStart=input()
            print("Enter new End Timings")
            newEnd=input()
            query=f"update schedules set Start ={newStart},End={newEnd} where d_id={d_id} and c_id={c_id}"
    elif(task=="add"):
        print("Enter Days")
        newDay=input()
        print("Enter Start Timings")
        newStart=input()
        print("Enter End Timings")
        newEnd=input()
        query=f"insert into schedules (d_id, c_id, day, start, end) VALUES ('{d_id}', '{c_id}', '{newDay}', '{newStart}', '{newEnd}')"
    mydbcursor.execute(query)
    mydb.commit()

def get_prescriptions(p_username):
    global mydb, mydbcursor
    query = f"select meds from prescriptions natural join login_patients where username = '{p_username}' and prescription_id = (select max(prescription_id) from prescriptions natural join login_patients where username = '{p_username}')"
    # lect description from (SELECT a_id, description from appointments natural join login_patients where username = 'shashwat90') t where a_id = (SELECT MAX(a_id) FROM appointments natural join login_patients where username = '{p_username}')
    mydbcursor.execute(query)
    return list(mydbcursor.fetchall())

def get_appointment_doc(a_id):
    global mydb, mydbcursor
    query = f"select d_id, d_name from appointments natural join doctors where a_id = {a_id}"
    mydbcursor.execute(query)
    return mydbcursor.fetchall()[0]

def get_appointment_clinic(a_id):
    global mydb, mydbcursor
    query = f"select c_id, c_name from appointments natural join clinics where a_id = {a_id}"
    mydbcursor.execute(query)
    return mydbcursor.fetchall()[0]

if __name__ == "__main__":
    
    mydbcursor.execute('SHOW TABLES')
    for x in mydbcursor:
        print(x)
    new_clinic('test clinic','gk1','12043485')
    login()
import stdiomask
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "apple212",
    database = "test"
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
            
def validate_login(type, username, password):
    global mydbcursor
    query = "select d_id from login_doctors where username='" + username +"' and password='"+password+"';"
    mydbcursor.execute(query)
    # userids = list(mydbcursor.fetchall())
    ids = [i[0] for i in mydbcursor.fetchall()]
    if(len(ids)==1):
        print('LOGGED IN')
        return ids[0]
    return 0

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



def new_clinic(name, address, phone):
    global mydb, mydbcursor
    query = f"insert into clinics values(NULL, '{name}','{address}','{phone}')"
    try:
        mydbcursor.execute(query)
        mydb.commit()
        mydbcursor.execute("select last_insert_id()")
        c_id = mydbcursor.fetchall()[0][0]
    except mysql.connector.errors.IntegrityError as e:
        print(e)
    # create_user('clinic', c_id, 'username', 'password')


def new_doctor(name, specialization, fee, phone):
    global mydb, mydbcursor
    query = f"insert into doctors values(NULL, '{name}','{specialization}', '{fee}','{phone}')"
    try:
        mydbcursor.execute(query)
        mydb.commit()
        mydbcursor.execute("select last_insert_id()")
        d_id = mydbcursor.fetchall()[0][0]
        #create user account
    except mysql.connector.errors.IntegrityError as e:
        print(e)

def new_patient(name, sex, age, phone):
    global mydb, mydbcursor
    query = f"insert into patients values(NULL, '{name}','{sex}', {age},'{phone}')"
    try:
        mydbcursor.execute(query)
        mydb.commit()
        mydbcursor.execute("select last_insert_id()")
        d_id = mydbcursor.fetchall()[0][0]
        #create user account
    except mysql.connector.errors.IntegrityError as e:
        print(e)

def new_pharmacy(name, phone):
    global mydb, mydbcursor
    query = f"insert into pharmacies values(NULL, '{name}', '{phone}')"
    try:
        mydbcursor.execute(query)
        mydb.commit()
        mydbcursor.execute("select last_insert_id()")
        d_id = mydbcursor.fetchall()[0][0]
        #create user account
    except mysql.connector.errors.IntegrityError as e:
        print(e)

def view_doc_upcoming_appointments(d_id, c_id = 0):
    global mydb, mydbcursor
    if(c_id):
        query = f"select * from appointments where d_id = {d_id} and c_id = {c_id} and schedule >= now()"
    else:
        query = f"select * from appointments where d_id = {d_id} and schedule >= now()"
    mydbcursor.execute(query)
    appointments = list(mydbcursor.fetchall())
    return appointments

def view_doc_past_appointments(d_id, c_id = 0):
    global mydb, mydbcursor
    if(c_id):
        query = f"select * from appointments where d_id = {d_id} and c_id = {c_id} and schedule < now()"
    else:
        query = f"select * from appointments where d_id = {d_id} and schedule < now()"
    mydbcursor.execute(query)
    appointments = list(mydbcursor.fetchall())
    return appointments

def view_docs():
    global mydb, mydbcursor
    query = f"select * from doctors"
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
    query = f"select * from appointments where p_id = {p_id} and schedule >= now()"
    mydbcursor.execute(query)
    appointments = list(mydbcursor.fetchall())
    return appointments

def view_patient_past_appointments(p_id):
    global mydb, mydbcursor
    query = f"select * from appointments where p_id = {p_id} and schedule < now()"
    mydbcursor.execute(query)
    appointments = list(mydbcursor.fetchall())
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

if __name__ == "__main__":
    
    mydbcursor.execute('SHOW TABLES')
    for x in mydbcursor:
        print(x)
    new_clinic('test clinic','gk1','12043485')
    login()
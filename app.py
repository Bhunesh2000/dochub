import os
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'we_are_56'

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login_signup', methods=['POST'])
def login_signup():
    loginorsignup=request.form.get('loginorsignup')
    print(loginorsignup)
    usertype = request.form.get('usertype')
    _username = request.form.get('username')
    if (loginorsignup=='login'):
        if usertype == 'patient':
            return render_template("patient.html", username=_username,name='Rishab',appointments = [['shashwat', 'sunday 10AM', 'paf'], ['bhunesh', 'tuesday 7PM', 'aslkdfj']])
        elif usertype == 'doctor':
            return render_template("doctor.html", username=_username, name='Shashwat', appointments = [['shashwat', 'sunday 10AM', 'paf'], ['bhunesh', 'tuesday 7PM', 'aslkdfj']])
        elif usertype == 'pharmacy':
            return render_template("pharmacy.html", username=_username)
        elif usertype == 'clinic':
            return render_template("clinic.html", username=_username)
        else:
            flash('Please select user type')
            return redirect(url_for('home'))
    elif (loginorsignup=='signup'):
        return render_template("signup.html",usertype=usertype)
    else:
        flash('Please try again')
        return redirect(url_for('home'))
i = 0
def get_i():
    global i
    i+=1
    return i


if __name__ == '__main__':
    app.jinja_env.globals.update(get_i=get_i)
    app.run(debug = True)
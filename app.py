import os
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("home.html")


@app.route('/login', methods=['POST'])
def login():
    usertype = request.form.get('usertype')
    _username = request.form.get('username')
    if usertype == 'patient':
        return render_template("patient.html", username=_username)
    elif usertype == 'doctor':
        return render_template("doctor.html", username=_username)
    elif usertype == 'pharmacy':
        return render_template("pharmacy.html", username=_username)
    elif usertype == 'clinic':
        return render_template("clinic.html", username=_username)


if __name__ == '__main__':
    app.run()

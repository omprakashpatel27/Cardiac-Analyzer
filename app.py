from email import message
from glob import glob
from flask import Flask, render_template, request,session
from flask_sqlalchemy import SQLAlchemy
import pickle
import numpy as np
import re

# Create flask app
flask_app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

global loggeduser
global loggedmail

db = SQLAlchemy(flask_app)

class login(db.Model):
    __tablename__ = 'hdp'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.Integer)
    email = db.Column(db.String(200))

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

@flask_app.route('/login')
def loginpage():
    return render_template("login.html")

@flask_app.route('/faq')
def faqpage():
    return render_template("faq.html")

@flask_app.route('/formpage')
def indexpage():
    return render_template("index.html")

@flask_app.route('/')
def Home():
    return render_template("register.html")

@flask_app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if username == '' or password == '' or email == '' or password.isnumeric() == False:
            return render_template('register.html', message='Please enter required fields correctly')

        if re.fullmatch(regex,email) == None:
            return render_template('register.html', message='Please enter required fields correctly')

        if db.session.query(login).filter(login.username == username).count() == 0:
            global loggedmail
            loggedmail = email
            global loggeduser
            loggeduser = username
            data = login(username, password, email)
            db.session.add(data)
            db.session.commit()
            return render_template('login.html', message = 'Login Here')
        return render_template('login.html', message='You have already Registered')


@flask_app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        chk = password.isnumeric()

        if username == '' or password == '' or chk == False:
            return render_template('login.html', message='Please enter required fields correctly')

        result = db.session.query(login).filter(login.username == username)
        ok = 0
        global loggeduser
        loggeduser = username
        for x in result:
            if int(x.password) == int(password):
                global loggedmail
                loggedmail = x.email
                ok = 1
        
        if ok == 1:
            return render_template('home.html', username = username)
        else :
            return render_template('login.html', message='Wrong Username or Password')

@flask_app.route("/predict", methods = ["GET","POST"])
def predict():
    age = request.form['age']
    if age.isnumeric() == False:
        return render_template('index.html', msg = 'age must be numeric')
    age = int (age)
    gender = request.form['sex']
    if gender.isnumeric() == False:
        return render_template('index.html', msg = 'gender value must be numeric')
    gender = int(gender)
    cp = request.form['cp']
    if cp.isnumeric() == False:
        return render_template('index.html', msg = 'cp must be numeric')
    cp = int(cp)
    trestbps = request.form['trestbps']
    if trestbps.isnumeric() == False:
        return render_template('index.html', msg = 'trestbps must be numeric')
    trestbps = int(trestbps)
    chol = request.form['chol']
    if chol.isnumeric() == False:
        return render_template('index.html', msg = 'chol must be numeric')
    chol = int(chol)
    fbs = request.form['fbs']
    if fbs.isnumeric() == False:
        return render_template('index.html', msg = 'fbs must be numeric')
    fbs = int(fbs)
    restecg = request.form['restecg']
    if restecg.isnumeric() == False:
        return render_template('index.html', msg = 'restecg must be numeric')
    restecg = int(restecg)
    thalach = request.form['thalach']
    if thalach.isnumeric() == False:
        return render_template('index.html', msg = 'thalach must be numeric')
    thalach = int(thalach)
    exang = request.form['exang']
    if exang.isnumeric() == False:
        return render_template('index.html', msg = 'exang must be numeric')
    exang = int(exang)
    oldpeak = request.form['oldpeak']
    if oldpeak.isnumeric() == False:
        return render_template('index.html', msg = 'oldpeak must be numeric')
    oldpeak = int(oldpeak)
    slope = request.form['slope']
    if slope.isnumeric() == False:
        return render_template('index.html', msg = 'slope must be numeric')
    slope = int(slope)
    ca = request.form['ca']
    if ca.isnumeric()  == False:
        return render_template('index.html', msg = 'ca must be numeric')
    ca = int(ca)
    thal = request.form['thal']
    if thal.isnumeric() == False:
        return render_template('index.html', msg = 'thal must be numeric')
    thal = int(thal)

    if cp > 3:
        return render_template('index.html', msg = 'cp value must be between 0 to 3')
    if gender > 1:
        return render_template('index.html', msg = 'gender value must be between 0 or 1')
    if trestbps > 400:
        return render_template('index.html', msg = 'trestbps value should be less than 400')
    if chol > 400:
        return render_template('index.html', msg = 'chol value should be less than 400')
    if fbs > 1:
        return render_template('index.html', msg = 'fbs value should be either 0 or 1')
    if restecg > 2:
        return render_template('index.html', msg = 'restecg value must be between 0 to 2')
    if exang > 1:
        return render_template('index.html', msg = 'exang value should be either 0 or 1')
    if slope > 2:
        return render_template('index.html', msg = 'slope value must be between 0 to 2')
    if ca > 3:
        return render_template('index.html', msg = 'ca value must be between 0 to 3')
    if thal > 3:
        return render_template('index.html', msg = 'thal value must be between 0 to 3')
    

    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = model.predict(features)
    return render_template('report.html', name = loggeduser, email = loggedmail, data = prediction,age=age,gender=gender,cp=cp,trestbps=trestbps,chol=chol,fbs=fbs,restecg=restecg,thalach=thalach,exang=exang,oldpeak=oldpeak,slope=slope,ca=ca,thal=thal)

if __name__ == '__main__':
    flask_app.run()



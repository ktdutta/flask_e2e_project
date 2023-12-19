from flask import Flask, render_template, url_for, redirect, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
import logging
import json
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
from datetime import datetime
from sqlalchemy.orm import sessionmaker

import sys
sys.path.append('../db/')  # Adjust the relative path as needed
from db import PatientVisit, Base


# Load environment variables from .env
load_dotenv()
app = Flask(__name__)

### Part 2 - initial sqlalchemy-engine to connect to db:
DB_HOST = os.getenv("HOST")
DB_USER = os.getenv("USER")
DB_PASSWORD = os.getenv("PASSWORD")
DB_NAME = os.getenv("NAME")
DB_PORT = int(os.getenv("PORT", 3306))
DB_CHARSET = os.getenv("CHARSET", "utf8mb4")
DB_DATABASE = os.getenv("DATABASE")

DATABASE_URL = conn_string = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    f"?charset={DB_CHARSET}"
)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
Base.metadata.bind = app
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
db_session = Session()
## Test connection


## OAuth
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = "http://127.0.0.1:8000/google/auth"

app.secret_key = os.urandom(12)
oauth = OAuth(app)

# Configuring the Logger
logger = logging.getLogger(__name__)
date_time = datetime.now()
format = '%Y-%m-%d %H:%M:%S'
string = date_time.strftime(format)
handler = logging.FileHandler('../logs/log-' + string + ".log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s \n \n')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Configure the database URI using PyMySQL


# Initialize the SQLAlchemy instance

#
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/google/')
def google():
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    ###note, if running locally on a non-google shell, do not need to override redirect_uri
    ### and can just use url_for as below
    #redirect_uri = url_for('google_auth', _external=True)
    session['nonce'] = generate_token()
    ##, note: if running in google shell, need to override redirect_uri 
    ## to the external web address of the shell, e.g.,
    redirect_uri = 'https://8000-cs-743936412124-default.cs-us-east1-rtep.cloudshell.dev/google/auth/'
    return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, nonce=session['nonce'])
    session['user'] = user
    logger.info("Google User in session: ", user)
    return redirect('/home')

@app.route('/home')
def dashboard():
    logger.info("Changed route to home page")
    if "user" in session:
        return render_template('dashboard.html')
    return redirect(url_for("index"))

@app.route('/patients')
def patients():
    logger.info("Changed route to seeing patients")
    patients = db_session.query(PatientVisit).all()

    if "user" in session:
        return render_template('patients.html', patients=patients)
    return redirect(url_for("index"))

@app.route('/indicators')
def indicators():
    logging.info("Changed route to indicator")
    if "user" in session:
        return render_template('indicators.html')
    return redirect(url_for("index"))

@app.route('/addpatient',  methods=['GET', 'POST'])
def addpatient():
    logger.info("Changed route to adding patient")
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        age = request.form['age']
        last_visit = request.form['last_visit']
        reason_for_visit = request.form['reason_for_visit']
        patient_history = request.form['patient_history']
        temperature = request.form['temperature']
        weight = request.form['weight']
        height = request.form['height']
        blood_pressure = request.form['blood_pressure']
        symptoms = request.form['symptoms']
        diagnosis = request.form['diagnosis']
        treatment = request.form['treatment']

        # Create a new PatientVisit object and add it to the database
        new_patient = PatientVisit(
            name=name,
            age=age,
            last_visit=last_visit,
            reason_for_visit=reason_for_visit,
            patient_history=patient_history,
            temperature=temperature,
            weight=weight,
            height=height,
            blood_pressure=blood_pressure,
            symptoms=symptoms,
            diagnosis=diagnosis,
            treatment=treatment
        )

        db_session.add(new_patient)
        db_session.commit()
    if "user" in session:
        return render_template('addpatient.html')
    return redirect(url_for("index"))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(
        debug=True,
        port=8000
    )
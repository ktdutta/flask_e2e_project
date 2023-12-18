from flask import Flask, render_template, url_for, redirect, session
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


# Load environment variables from .env
load_dotenv()

### Part 2 - initial sqlalchemy-engine to connect to db:


## Test connection


## OAuth
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = "http://127.0.0.1:8000/google/auth"

app = Flask(__name__)

app.secret_key = os.urandom(12)
oauth = OAuth(app)

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
    print(" Google User ", user)
    return redirect('/dash')

@app.route('/dash')
def dashboard():
    if "user" in session:
        return json.dumps({"message": "you are logged in"})
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(
        debug=True,
        port=8000
    )
#from flask import Flask

#app = Flask(__name__)
#@app.route("/")
#def hello_world():
#    return "Hello World"

import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#create database enginr
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect the database into our classes
Base = automap_base()

#reflect database
Base.prepare(engine, reflect=True)

#create a variable for each of the classes
Measurement = Base.classes.measurement
Station = Base.classes.station

#create a session link from Python to database
session = Session(engine)

#define flask app
app = Flask(__name__)

#define the welcome route
@app.route("/")

#create a function
#return statement will have f-strings as a reference to all of the other routes
#add the precipitation, stations, tobs, and temp routes into return statement
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
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

#new app route for precipitation
@app.route("/api/v1.0/precipitation")

def precipitation():
    #calculate the date one year ago from the most recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    #format results into a JSON structured file
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#new app route for precipitation
@app.route("/api/v1.0/dd")

def precip():
    #calculate the date one year ago from the most recent date in the database
    #prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date).all()
    #format results into a JSON structured file
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#new app route for stations
@app.route("/api/v1.0/stations")

def stations():
    #create query that gets all stations
    results = session.query(Station.station).all()
    # unravel results into a one-dimensional array
    #convert results into a list
    stations = list(np.ravel(results))
    #jsonify the list. return as JSON
    return jsonify(stations=stations)

#new app route for temperatures
@app.route("/api/v1.0/tobs")

def temp_monthly():
    #calculate the date one year ago from the last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #query the primary station for all the temperature observations from the previous year
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    #unravel the results into a one-dimensional array and convert that array into a list
    temps = list(np.ravel(results))
    #jsonify the list and return results
    return jsonify(temps=temps)

#create statistics app route
#displays both starting and end date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#add start and end parameters set to None
def stats(start=None, end=None):
    #create query to select the minimum, average, and maximum temperatures from database
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    #determine the starting and ending date with an "if-not" statement
    if not end:
        #query database 
        #an asterisk is used to indicate there will be multiple results for the query: minimum, average, and maximum temperatures
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        #unravel the results into a one-dimensional array and convert them to a list
        temps = list(np.ravel(results))
        #jsonify results and return them
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
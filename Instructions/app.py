import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    '''somethiong'''
    # Calculate the date 1 year ago from the last data point in the database
    lastdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    lastdate = dt.datetime.strptime(str(lastdate[0]), '%Y-%m-%d')

    # Perform a query to retrieve the data and precipitation scores
    yearago =  lastdate - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date>=yearago).\
        order_by(Measurement.date.asc()).all()

    return jsonify({k:v for k,v in results})

@app.route("/api/v1.0/stations")
def stations():
    results1 = session.query(Station.station).all()

    return jsonify(results1)

@app.route("/api/v1.0/tobs")
def tobs():
    lastdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    lastdate = dt.datetime.strptime(str(lastdate[0]), '%Y-%m-%d')
    yearago =  lastdate - dt.timedelta(days=365)
    results = session.query(Measurement.tobs, Measurement.date).\
    filter(Measurement.date >= yearago).all()

    return jsonify(results)

@app.route("/api/v1.0/<start_date>")
def calc_temps(start_date):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()


    return jsonify(results)
#    result = session.query(Measurement.tobs).\
#    filter(Measurement.station == 'USC00519281').\
#    filter(Measurement.date >= yearago).all()

# @app.route("/api/v1.0/<start>/<end>")
# def names():


if __name__ == '__main__':
    app.run(debug=True)

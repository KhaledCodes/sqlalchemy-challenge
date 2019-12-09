import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect = True)

Measurement = Base.classes.Measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations" )​
​
@app.route("/api/v1.0/precipitation")
def precipitation():
    '''somethiong'''
    # Calculate the date 1 year ago from the last data point in the database
    lastdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    lastdate = dt.datetime.strptime(str(lastdate[0]), '%Y-%m-%d')
​
    # Perform a query to retrieve the data and precipitation scores
    yearago =  lastdate - dt.timedelta(days=365)
​
    results = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date>=yearago).\
        order_by(Measurement.date.asc()).all()
​
    return jsonify({k:v for k,v in results})
​
@app.route("/api/v1.0/stations")
def stations():
    ''' do code'''
​
# @app.route("/api/v1.0/<start>")
# def stats():
# @app.route("/api/v1.0/<start>/<end>")
# def names():
​
​
if __name__ == '__main__':
    app.run(debug=True)


import numpy as np
import pandas as pd
import numpy as np
from flask import Flask, jsonify
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy import create_engine, func
from sqlalchemy import Column, Integer, String, Float, Date
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD"
    )
    
# `/api/v1.0/precipitation`
#Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def rain():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    all_days = []
    for day in results:
        day_dict = {}
        day_dict[day[0]] = day[1]
        all_days.append(day_dict)
    return jsonify(all_days)

#`/api/v1.0/stations`
#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name).all()
    session.close()
    all_stations = []
    for stn in results:
        stn_dict = {}
        stn_dict[stn[0]] = stn[1]
        all_stations.append(stn_dict)
    return jsonify(all_stations)

#`/api/v1.0/tobs`
#query for the dates and temperature observations from a year from the last data point.
#Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def temp():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23').all()
    session.close()
    all_days = []
    for day in results:
        day_dict = {}
        day_dict[day[0]] = day[1]
        all_days.append(day_dict)
    return jsonify(all_days)

#`/api/v1.0/<start>` and 
#Return a JSON list of the minimum temperature, the average temperature, 
#   and the max temperature for a given start or start-end range.
#When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` 
#   for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def since(start):
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > start).all()
    session.close()
    dates = []
    temps = []
    for day in results:
        dates.append(day[0])
        temps.append(day[1])
    tmin = np.min(temps)
    tavg = np.mean(temps)
    tmax = np.max(temps)
    for day in results:
        if day[1] == tmax:
            maxDay = day[0]
        elif day[1] == tmin:
            minDay = day[0]
    stats = []
    tempDict = {}
    max = [maxDay, tmax]
    min = [minDay, tmin]
    avg = ['n/a', tavg]
    tempDict['tmin'] = min
    tempDict['tavg'] = avg
    tempDict['tmax'] = max
    stats.append(tempDict)
    return jsonify(stats)

#`/api/v1.0/<start>/<end>`
#When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` 
#   for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def between(start, end):
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(and_(Measurement.date > start, Measurement.date < end)).all()
    session.close()
    dates = []
    temps = []
    for day in results:
        dates.append(day[0])
        temps.append(day[1])
    tmin = np.min(temps)
    tavg = np.mean(temps)
    tmax = np.max(temps)
    for day in results:
        if day[1] == tmax:
            maxDay = day[0]
        elif day[1] == tmin:
            minDay = day[0]
    stats = []
    tempDict = {}
    max = [maxDay, tmax]
    min = [minDay, tmin]
    avg = ['n/a', tavg]
    tempDict['tmin'] = min
    tempDict['tavg'] = avg
    tempDict['tmax'] = max
    stats.append(tempDict)
    return jsonify(stats)




if __name__ == "__main__":
    app.run(debug=True)

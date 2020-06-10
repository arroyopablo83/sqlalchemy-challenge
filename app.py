import datetime as dt 
import numpy as np
import pandas as pd
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Sessio(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to Climate App <br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(weeks=4 * 12)
    precipitation = session.query(Measurement.date, Measurement,prcp).\
        filter(Measurement.date >= prev_year).all()

    result = {date: prcp for date, prcp in precipitation}
    return jsonify(result)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    result = list(np.ravel(result))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(weeks=4 * 12)
    tobs = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
            filter(Measurement.date >= prev_year).all()
    result = list(np.ravel(result))
    return jsonify(result)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start)
    if end:
        result = list(np.ravell(result).all())
        return jsonify(result)
    result = result.filter(Measurement.date <= end).all()
    result = list(np.ravel(result))
    return jsonify(result)

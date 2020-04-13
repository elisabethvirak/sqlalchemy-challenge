import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found
Base.classes.keys()
# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station

# Create an app
app = Flask(__name__)


# Define home page
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (f"Welcome to my Climate Analysis of Hawaii!<br/></br>"
    f"Available Routes:<br/>"
    f"Precipitation Analysis: /api/v1.0/precipitation<br/>"
    f"Station Analysis: /api/v1.0/stations<br/>"
    f"Temperature Analysis: /api/v1.0/tobs<br/>"
    )



# Define precipitation page
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    
    # query session for precipitation data
    session=Session(engine)
    results_p = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # create a dictionary collecting the precipitation and date data
    precip_data = []
    for date, prcp in results_p:
        precip_dict = {}
        precip_dict['Date'] = date
        precip_dict['Precipitation'] = prcp
        precip_data.append(precip_dict)
    
    # jsonify dictionary
    return  jsonify(precip_data)

# Define precipitation page
@app.route("/api/v1.0/stations")
def station():
    print("Server received request for 'Stations' page...")
    
    # query session for station data
    session=Session(engine)
    results_s = session.query(Station.station, Station.name).all()
    session.close()

    # create a dictionary collecting the station and station name
    station_data = []
    for station, name in results_s:
        station_dict = {}
        station_dict['Station'] = station
        station_dict['Name'] = name
        station_data.append(station_dict)

    # jsonify dictionary
    return jsonify(station_data)

# Define precipitation page
@app.route("/api/v1.0/tobs")
def temperature():
    print("Server received request for 'Temperature' page...")
    
    # query session for temperature data
    session = Session(engine)
    results_t = session.query(Station.name, Measurement.station, Measurement.date,\
        Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >='2016-08-23').all()
    session.close()

    # create a dictionary collecting the dates and temperatures of the specified station
    
    '''attempted the below first, but it did not work. found an option through someone else
    to append by index instead. see below'''
    '''tobs_data = []
    for name, date, tobs in results_t:
        tobs_dict = {}
        tobs_dict['name']=name
        tobs_dict['date']=date
        tobs_dict['tobs']=tobs
        tobs_data.append(tobs_dict)
    '''

    tobs_data = []
    for t in results_t:
        tobs_dict = {}
        tobs_dict['Station'] = t[0]
        tobs_dict['Name'] = t[1]
        tobs_dict['Date'] = t[2]
        tobs_dict['Temperature'] = t[3]
        tobs_data.append(tobs_dict)

    # jsonify the dictionary
    return jsonify(tobs_data)


if __name__ == "__main__":
    app.run(debug=True)

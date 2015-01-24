#!/usr/bin/env python
import ow
import time

"""Read data from 1-wire sensors in an USB adapter and log the data to sqlite"""

# Translations from sensor ID codes to human-readable names
# CREATE TABLE locations (location TEXT, sensor TEXT);
# Raw measurement data without filtering
# CREATE TABLE measurements (sensor TEXT, date TEXT, value INTEGER, FOREIGN KEY(sensor) REFERENCES locations(sensor));
# Use sensor as primary key on latest_measurement to allow INSERT OR REPLACE to keep it up to date
# CREATE TABLE latest_measurement (sensor TEXT PRIMARY KEY, date TEXT, value INTEGER);
# PRAGMA foreign_keys = ON;

import sqlite3
import datetime
conn = sqlite3.connect("/home/pi/bin/temp.sqlite")
c = conn.cursor()

ow.init("u")

sensors = ow.Sensor("/").sensorList()

for sensor in sensors[:]:
    # remove the id token contained in the usb module
    if sensor.type == "DS1420":
        sensors.remove(sensor)

measurement_time = datetime.datetime.now().isoformat();
for sensor in sensors:
    stmt = "INSERT INTO measurements (sensor, date, value) VALUES ('%s', '%s', %s);" % (sensor.address, measurement_time, sensor.temperature)
    stmt2 = "INSERT OR REPLACE INTO latest_measurement (sensor, date, value) VALUES ('%s', '%s', %s);" % (sensor.address, measurement_time, sensor.temperature)
    c.execute(stmt)
    c.execute(stmt2)

conn.commit()
c.close()

# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
import requests

import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *

import datetime
import time

from apscheduler.schedulers.blocking import BlockingScheduler

apikey = "69509fc01ef79df4"
country_code = "FI"
city = "Jyvaskyla"

# TODO:
# forecast10day
# hourly


def wunderground(method):
    api_url = "http://api.wunderground.com/api/%s/%s/q/%s/%s.json" % (apikey, method, country_code, city)
    r = requests.get(api_url)

    return r


def current_temp():
    current_weather = wunderground("conditions").json()['current_observation']
    return current_weather['temp_c']

def log_temp(stream):
    print(stream)
    temp = current_temp()
    now = datetime.datetime.now()
    stream.write({'x': now, 'y': temp})
    print(now)
    print(temp)
    print("-----")


if __name__ == '__main__':

    stream_ids = tls.get_credentials_file()['stream_ids']
    
    wunder_trace = Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        name='Wunderground',
        stream = Stream(token=stream_ids[0], maxpoints=72)
        )

    outside_trace = Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        name='Outside',
        stream = Stream(token=stream_ids[1], maxpoints=72)
        )

    inside_trace = Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        name='Inside',
        stream = Stream(token=stream_ids[2], maxpoints=72)
        )

    data = Data([wunder_trace, outside_trace])

    layout = Layout(
        title='Weather in Jyväskylä',
        showlegend=True,
    )

    figure = Figure(data=data, layout=layout)
    url = py.plot(figure, filename='piweather')
    print(url)
    
    wunder_stream = py.Stream(stream_ids[0])
    wunder_stream.open()
    outside_stream = py.Stream(stream_ids[1])
    outside_stream.open()
    inside_stream = py.Stream(stream_ids[2])
    inside_stream.open()
    
    import time

    import sqlite3
    conn = sqlite3.connect("/home/pi/bin/temp.sqlite")
    c = conn.cursor()

    while True:
        c.execute("select locations.location, latest_measurement.date, latest_measurement.value from latest_measurement join locations on latest_measurement.sensor = locations.sensor where location = 'Ulko'")
        res = c.fetchall()
        out_temp = res[0][2]
        c.execute("select locations.location, latest_measurement.date, latest_measurement.value from latest_measurement join locations on latest_measurement.sensor = locations.sensor where location = 'Makuuhuone'")
        res = c.fetchall()
        in_temp = res[0][2]

        now = datetime.datetime.now()

        wunder_stream.write({'x': now, 'y': current_temp()})
        outside_stream.write({'x': now, 'y': out_temp})
        inside_stream.write({'x': now, 'y': in_temp})

        time.sleep(60)


    # scheduler = BlockingScheduler()
    # scheduler.add_job(log_temp, trigger='cron', minute="*/30", args=[stream])

    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     pass

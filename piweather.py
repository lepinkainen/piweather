from __future__ import print_function, division, absolute_import, unicode_literals
import requests

import plotly.plotly as py
#import plotly.tools as tls
#from plotly.graph_objs import *

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

    stream = py.Stream('223q4ee939')
    stream.open()
    log_temp(stream)
    scheduler = BlockingScheduler()
    scheduler.add_job(log_temp, trigger='cron', minute="*/30", args=[stream])

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

import os
from flask import Flask, render_template, request
import requests
import json
import logging
import time
import functools
from functools import lru_cache
import datetime as dt
from datetime import timedelta
from redis import Redis

# -----------------------------DATA_VARIABLES--------------------------------

base_timezone_url = 'http://worldtimeapi.org/api/timezone/'
customTimezones = ['Africa/Accra', 'America/Belize', 'Antarctica/Davis', 'Asia/Baghdad', 'Australia/Eucla',
                   'Europe/Zurich']

app = Flask(__name__)

# INITIALIAZE LOGGER

logging.basicConfig(filename="std.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()

# INITIALIZE REDIS CLIENT

redis_client = Redis(
    host='localhost',
    port='6379')


def get_redis_client():
    global redis_client
    if not redis_client:
        # get credentials from environment variables
        redis_client = Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            db=os.getenv('REDIS_DB'),
            password=os.getenv('REDIS_PASSWORD')
        )
    assert redis_client.ping()  # check if connection is successful
    return redis_client


# REDIS FUNCTION TO CHECK IF AN IP ADRESS CONNECTS MORE THAN ONCE IN A 5-SECOND LAPSE

def rate_per_five_seconds(function, count, remote_ip):
    client = get_redis_client()
    key = remote_ip
    if int(client.incr(key)) > count:
        response = 0
    else:
        response = function

    if client.ttl(key) == -1:  # timeout is not set
        client.expire(key, 5)  # expire in 4 seconds

    return response


# FUNCTION TO CONNECT TO THE WORLD TIME API AND GET ONE CITY
# LRU_CACHE IMPLEMENTED TO CACHE THE OUTPUT REQUEST

@lru_cache(maxsize=16)
def get_city_datetime(url):
    global RequestElapsedTime, starting_time, customTimezones, base_timezone_url

    r = requests.get(base_timezone_url + url)
    cityRequest = r.json()
    cityUtcTime = cityRequest['utc_datetime']

    return cityUtcTime


# FUNCTION TO RETRIEVE A LIST OF CITIES
def get_cities():
    timezoneArray = {}
    for url in customTimezones:
        timezoneArray[url] = get_city_datetime(url)

    citiesArray = {}
    citiesArray = json.dumps(timezoneArray)

    return citiesArray


# FLASK ROUTES

# JUST THE HOME
@app.route('/')
def home():
    return "Timezones"


# MAIN ENTRYPOINT /TIMES
@app.route('/times/', methods=['GET'])
def times():
    # REQUESTS THE IP ADDRESS OF THE END USER
    request_ip = request.remote_addr

    # STARTS THE TIME COUNTER TO LOG THE API TIME RESPONSE
    StartingTime = time.time()

    # GETS ALL THE CITIES TIMEZONES, ONCE CREQUEST EVERY 5 SECONDS
    worldtimes = rate_per_five_seconds(get_cities(), 1, request_ip)  # example: 1 request per 5 seconds
    # print(get_cities.cache_info())

    # ENDS THE TIME COUNTER TO GET THE API REQUEST TOTAL TIME
    EndingTime = time.time()
    ElapsedTime = timedelta(seconds=EndingTime - StartingTime).microseconds

    # LOGS THE API REQUEST TIME
    logger.warning(request_ip + " - - /times request response: " + str(ElapsedTime) + "ms")

    if worldtimes == 0:
        result = "Number of Requests Exceeded.Try again in 5 seconds."
    else:
        result = worldtimes

    return result


@app.route('/times/city/<string:continent>/<string:city>', methods=['GET'])
def get_city(continent: str, city: str):
    # REQUESTS THE IP ADDRESS OF THE END USER
    request_ip = request.remote_addr
    geolocation = continent + '/' + city

    # GETS THE CITY'S UTC TIME
    output = rate_per_five_seconds(get_city_datetime(geolocation), 1, request_ip)  # example: 1 request per 5 seconds

    if output == 0:
        result = "Number of Requests Exceeded.Try again in 5 seconds."
    else:
        timezoneArray = {geolocation: output}

        result = {}

        result = json.dumps(timezoneArray)

    return result


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="4242")

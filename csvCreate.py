
import csv
import openmeteo_requests
import requests_cache
import pandas as pd
import urllib.parse
from retry_requests import retry

# takes a coordinate(lat, long) and a date range(inclusive, inclusive) and creates a CSV with all relevant information(yield, quarterly avg stddev min max for temp, rain sum, sunshine duration
#def csvCreate(coordinate, dateRange):

#takes a quarters worth of weather data in the form of a pandas dataframe and produces an array of avg stddev min max for the sets of data in the form
# ((avg stddev min max of temp), (avg stddev min max of rain sum), (avg stddev min max of sunshine duration))
url = "https://archive-api.open-meteo.com/v1/archive"
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)
def process(data, variables):
    returnVal = []
    for i in range(3):
        returnVal.append([data.mean()[variables[i]], data.std()[variables[i]], data.min()[variables[i]], data.max()[variables[i]]])
    return returnVal

def CreateYear(year, county, state, writer, nass, lat, long):
    call = 'source_desc=SURVEY' + \
    '&sector_desc=CROPS' + \
    '&commodity_desc=SOYBEANS' + \
    '&statisticcat_desc=YIELD' + \
    '&unit_desc=' + urllib.parse.quote('BU / ACRE') + \
    f'&state_alpha={state}' + \
    f'&county_name={county}' + \
    f'&year={year}' + \
    '&format=CSV'
    q1params = {
        "latitude": lat,
        "longitude": long,
        "start_date": f"{year}-03-08",
        "end_date": f"{year}-05-22",
        "daily": ["temperature_2m_mean", "precipitation_sum", "sunshine_duration"],
    }
    q2params = {
        "latitude": lat,
        "longitude": long,
        "start_date": f"{year}-03-08",
        "end_date": f"{year}-05-22",
        "daily": ["temperature_2m_mean", "precipitation_sum", "sunshine_duration"],
    }
    q3params = {
        "latitude": lat,
        "longitude": long,
        "start_date": f"{year}-03-08",
        "end_date": f"{year}-05-22",
        "daily": ["temperature_2m_mean", "precipitation_sum", "sunshine_duration"],
    }
    q4params = {
        "latitude": lat,
        "longitude": long,
        "start_date": f"{year}-03-08",
        "end_date": f"{year}-05-22",
        "daily": ["temperature_2m_mean", "precipitation_sum", "sunshine_duration"],
    }
    val = nass.get_data(call)
    q1 = openmeteo.weather_api(url, params=q1params)[0].Daily()



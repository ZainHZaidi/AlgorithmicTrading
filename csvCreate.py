import csv
import openmeteo_requests
import requests_cache
import pandas as pd
import urllib.parse
import time
from retry_requests import retry
from c_usda_quick_stats import c_usda_quick_stats

# takes a quarters worth of weather data in the form of a pandas dataframe
# and produces an array of data in the form
# ((avg, stddev, min, max (temp)), (avg, stddev, min, max (rain sum)), (avg, stddev, min, max (sunshine duration))


def process(data, variables):
    returnVal = []
    for i in range(3):
        returnVal.append([data.get(variables[i]).mean(), data.get(variables[i]).std(),
                          data.get(variables[i]).min(), data.get(variables[i]).max()])
    return returnVal


def create_year(year, county, state, nass, long, lat):
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://archive-api.open-meteo.com/v1/archive"
    # all the calls for the apis: call is for NASS, q1-4params is for openmeteo
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
        "start_date": f"{year}-01-01",
        "end_date": f"{year}-03-31",
        "daily": ["temperature_2m_mean", "precipitation_sum", "sunshine_duration"],
    }
    q2params = {
        "latitude": lat,
        "longitude": long,
        "start_date": f"{year}-04-01",
        "end_date": f"{year}-06-30",
        "daily": ["temperature_2m_mean", "precipitation_sum", "sunshine_duration"],
    }
    q3params = {
        "latitude": lat,
        "longitude": long,
        "start_date": f"{year}-07-01",
        "end_date": f"{year}-09-30",
        "daily": ["temperature_2m_mean", "precipitation_sum", "sunshine_duration"],
    }
    q4params = {
        "latitude": lat,
        "longitude": long,
        "start_date": f"{year}-10-01",
        "end_date": f"{year}-12-31",
        "daily": ["temperature_2m_mean", "precipitation_sum", "sunshine_duration"],
    }
    val = nass.get_data(call) # yield value in BU/ACRE
    row = [year, val]
    params = [q1params, q2params, q3params, q4params]
    for param in params:
        daily = openmeteo.weather_api(url, params=param)[0].Daily()
        daily_data = {"date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        )}
        temperature_mean = daily.Variables(0).ValuesAsNumpy()
        rain_sum = daily.Variables(1).ValuesAsNumpy()
        sunshine_duration = daily.Variables(2).ValuesAsNumpy()
        daily_data["temperature_mean"] = temperature_mean
        daily_data["rain_sum"] = rain_sum
        daily_data["sunshine_duration"] = sunshine_duration
        k = pd.DataFrame(data=daily_data)
        dvs = process(k, ["temperature_mean", "rain_sum", "sunshine_duration"])
        for x in dvs:
            for z in x:
                row.append(z)
    return row

cat1 = ["q1","q2","q3","q4"]
cat2 = ["temperature", "rainSum", "SSdur"]
cat3 = ["mean","std","min","max"]
emp = ["year", "yield"]
for x in cat1:
    for j in cat2:
        for z in cat3:
            emp.append(x + "_" + j + "_" + z)

def csv_create(county, state, lat, long, y1, y2, emp):
    with open(f'{state}_{county}.csv', 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, quotechar = ",")
        writer.writerow(emp)
        for i in range(y1, y2 + 1):
            writer.writerow(create_year(i, county, state, c_usda_quick_stats(), long, lat))
            print(state + "_" + county, (i-y1)/(y2-y1+1))




df = pd.read_csv("states.csv")
for i in range(22, len(df)):
    initial = time.time()
    csv_create(df.loc[i]["county"], df.loc[i]["state"], df.loc[i]["lat"], df.loc[i]["long"], 1970, 2022, emp)
    print(time.time()-initial)

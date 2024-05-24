import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://archive-api.open-meteo.com/v1/archive"
# call parameters, latitude, longitude, fully inclusive date, then daily, set of daily variables to call from api
params = {
	"latitude": 38.5816,
	"longitude": -121.4944,
	"start_date": "1999-05-08",
	"end_date": "1999-05-22",
	"daily": ["temperature_2m_mean", "precipitation_sum"],
}
responses = openmeteo.weather_api(url, params=params)


response = responses[0]


# Process hourly data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_temperature_2m = daily.Variables(0).ValuesAsNumpy()
rain_sum = daily.Variables(1).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}
print(daily_data)
daily_data["temperature_2m"] = daily_temperature_2m
daily_data["rain_sum"] = rain_sum
print(daily.Variables(0).ValuesAsNumpy())
hourly_dataframe = pd.DataFrame(data = daily_data)
print(hourly_dataframe)

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
	"latitude":  39.2059,
	"longitude": -85.8977,
	"start_date": "2000-01-01",
	"end_date": "2000-03-31",
	"timezone": "America/New_York",
	"daily": ["temperature_2m_mean", "precipitation_sum", "sunshine_duration"],
}
responses = openmeteo.weather_api(url, params=params)


response = responses[0]


# Process hourly data. The order of variables needs to be the same as requested.
daily = response.Daily()
temperature_mean = daily.Variables(0).ValuesAsNumpy()
rain_sum = daily.Variables(1).ValuesAsNumpy()
sunshine_duration = daily.Variables(2).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}

daily_data["temperature_mean"] = temperature_mean
daily_data["rain_sum"] = rain_sum
daily_data["sunshine_duration"] = sunshine_duration

hourly_dataframe = pd.DataFrame(data = daily_data)
vars = ["temperature_mean", "rain_sum", "sunshine_duration"]

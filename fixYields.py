import os
import time
import urllib
import pandas as pd
from c_usda_quick_stats import c_usda_quick_stats
nass = c_usda_quick_stats()
for file in os.listdir("states"):
    yields = dict()
    state = file.split("_")[0]
    county = file.split("_")[-1].split(".")[0]
    call = 'source_desc=SURVEY' + \
           '&sector_desc=CROPS' + \
           '&commodity_desc=SOYBEANS' + \
           '&statisticcat_desc=YIELD' + \
           '&unit_desc=' + urllib.parse.quote('BU / ACRE') + \
           f'&state_alpha={state}' + \
           f'&county_name={county}' + \
           '&format=CSV'
    val = nass.get_data(call)[:-1]
    for x in val:
        yields[x.split(",")[-9][1:-1]] = x.split(",")[-2][1:-1]
    df = pd.read_csv("States/" + file)
    addYields = []
    for i in range(df["year"].iloc[0], df["year"].iloc[-1]+1):
        try:
            addYields.append(yields[str(i)])
        except:
            addYields.append(-1)
    print(len(df), len(addYields), state, county)
    df["yield"] = addYields
    df.to_csv("newStates/"+state+"_"+county+".csv")
    time.sleep(10)
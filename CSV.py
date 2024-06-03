import pandas as pd
import csv
sc = set()
allCounty = pd.read_csv("State-County-Lat-Long.csv", on_bad_lines='skip')
soybeanCounty = pd.read_csv("AcresPlanted.csv")

abbrev = {
    "alabama": "AL",
    "alaska": "AK",
    "arizona": "AZ",
    "arkansas": "AR",
    "california": "CA",
    "colorado": "CO",
    "connecticut": "CT",
    "delaware": "DE",
    "florida": "FL",
    "georgia": "GA",
    "hawaii": "HI",
    "idaho": "ID",
    "illinois": "IL",
    "indiana": "IN",
    "iowa": "IA",
    "kansas": "KS",
    "kentucky": "KY",
    "louisiana": "LA",
    "maine": "ME",
    "maryland": "MD",
    "massachusetts": "MA",
    "michigan": "MI",
    "minnesota": "MN",
    "mississippi": "MS",
    "missouri": "MO",
    "montana": "MT",
    "nebraska": "NE",
    "nevada": "NV",
    "new hampshire": "NH",
    "new jersey": "NJ",
    "new mexico": "NM",
    "new york": "NY",
    "north carolina": "NC",
    "north dakota": "ND",
    "ohio": "OH",
    "oklahoma": "OK",
    "oregon": "OR",
    "pennsylvania": "PA",
    "rhode island": "RI",
    "south carolina": "SC",
    "south dakota": "SD",
    "tennessee": "TN",
    "texas": "TX",
    "utah": "UT",
    "vermont": "VT",
    "virginia": "VA",
    "washington": "WA",
    "west virginia": "WV",
    "wisconsin": "WI",
    "wyoming": "WY",
}
allCounty["county"] = allCounty["county"].str.upper()



with open("states.csv", "w", newline="\n") as file:
    writer = csv.writer(file, quotechar=",")
    writer.writerow(("state", "county", "lat", "long"))
    for i in range(len(soybeanCounty)):
        ser = allCounty.loc[(allCounty["county"] == soybeanCounty["County"][i]) & (
                    allCounty['state'] == abbrev[soybeanCounty["State"][i].lower()])]
        sc.add((ser["state"].iloc[0], soybeanCounty["County"][i], float(ser["lat"].iloc[0]), float(ser["lon"].iloc[0])))
    writer.writerows(sc)

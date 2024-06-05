import pandas as pd
import os

header = "year,yield,q2_temperature_mean,q2_temperature_std,q2_temperature_min,q2_temperature_max,q2_rainSum_mean," \
         "q2_rainSum_std,q2_rainSum_min,q2_rainSum_max,q2_SSdur_mean,q2_SSdur_std,q2_SSdur_min,q2_SSdur_max," \
         "q3_temperature_mean,q3_temperature_std,q3_temperature_min,q3_temperature_max,q3_rainSum_mean," \
         "q3_rainSum_std,q3_rainSum_min,q3_rainSum_max,q3_SSdur_mean,q3_SSdur_std,q3_SSdur_min,q3_SSdur_max".split(",")
z = []
for file in os.listdir("newnewStates"):
    df = pd.read_csv("newnewStates/" + file)
    df = df[df["yield"] != -1]
    df= df.drop(["year"], axis=1)
    z.append(df)
sum = pd.concat(z)

sum.to_csv("sum.csv", index=0)

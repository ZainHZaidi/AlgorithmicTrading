import os
import time
import urllib
import pandas as pd

cat1 = ["q1","q4"]
cat2 = ["temperature", "rainSum", "SSdur"]
cat3 = ["mean","std","min","max"]
emp = []
for x in cat1:
    for j in cat2:
        for z in cat3:
            emp.append(x + "_" + j + "_" + z)
for file in os.listdir("newStates"):
    df = pd.read_csv("newStates/" + file)

    if emp[0] in df.columns:
        df = df.drop(emp, axis=1)
    df = df[df.year >= 2000]
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.to_csv("newnewStates/" + file, index=False)

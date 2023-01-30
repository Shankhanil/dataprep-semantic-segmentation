import pandas as pd
import json

data = pd.read_csv('kv.csv')

dict = {}
for index, row in data.iterrows():
    dict[ int(row.k) ] = int(row.v)


print(dict)

with open("labelmap.json", "w") as fp:
    json.dump(dict,fp) 
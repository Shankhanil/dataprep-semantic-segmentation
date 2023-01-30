import json

with open('/home/shankhanil/work/3dclothgen/panel-stats/DATA_PREP/DATASET/version1/class_mapping.json') as json_file:
    data = json.load(json_file)

# data = data[0]
# print(data)
for d in data:
    # data[k] +=1
    # print(d["trainId"])
    d["trainId"] += 1

print(data)


# print(data)
json.dump(data, 'class_mapping_2.json')
from pycocotools.coco import COCO
import pandas as pd
import json
from glob import glob 
import numpy as np

ann = 15
cat = 'Legging'
# gender = 'Female'

json_file = "coco_dataset/batch_1/Female/bodies/task_bodies-2022_08_20_07_37_25-coco 1.0/annotations/instances_default.json"
coco_json = COCO(json_file)
cat_dict = {}
label_count = {}
area_count = {}
cat_len = len(list(coco_json.getCatIds()))

for cat_id in range(1, cat_len + 1):
    name = coco_json.loadCats(ids=cat_id)[0]["name"]
    id = coco_json.loadCats(ids=cat_id)[0]["id"]
    cat_dict[name] = id
    label_count[id] = 0
    area_count[id] = 0

print(len(list(label_count.values())))

# batches 1-2-3
# json_dir = sorted(glob('coco_dataset/batch_{}/*/*/*coco 1.0/annotations/instances_default.json'.format(ann)))

# batch13-15
json_dir = sorted(glob('coco_dataset/batch_{}/*/*/*/annotations/instances_default.json'.format(ann)))

# batch 5-6-7-12-14
# json_dir = sorted(glob('coco_dataset/batch_{}/*/*/*coco 1/annotations/instances_default.json'.format(ann)))

# batch 4,8
# json_dir = sorted(glob('coco_dataset/batch_{}/*coco 1/annotations/instances_default.json'.format(ann)))
print(json_dir)

for json_file in json_dir:
    
    coco_json = COCO(json_file)
    lent = len(coco_json.getAnnIds())

    for i in range(1, lent + 1):

        if (coco_json.loadAnns(ids=i)):
            cat  = coco_json.loadAnns(ids=i)[0]["category_id"]
            area_c = coco_json.loadAnns(ids=i)[0]["area"]
            label_count[cat] += 1
            area_count[cat] += area_c



col0 = list(cat_dict.values())
col1 = list(cat_dict.keys())
col2 = list(label_count.values())
col3 = list(area_count.values())

print(len(col0), len(col1), len(col2), len(col3))

df = pd.DataFrame(
    {'index': col0,
    'label_name': col1,
    'label_counts': col2,
    'area_counts': col3
    })

pth = 'coco_dataset/stats_ann{}.csv'.format(ann)
df.to_csv(pth, index=False)


# import pandas as pd
# from glob import glob
# import numpy as np





# df = pd.read_csv("coco_dataset/stats_ann1.csv")
# print(df.shape)

# if df[df['labels'] == '_background_'].empty:
#     print("No drop")
# else:
#     a = int(df[df['labels'] == '_background_'].index[0])
#     b = int(df[df['labels'] == 'TRIM_C_PLACKET_OVER'].index[0])
#     df.drop(df.index[[a, b]], inplace=True)
#     print('Droped rows')

# label_list = list(df['labels'])
# cnt_list = [0] * len(label_list)
# area_list = [0] * len(label_list)

# csvlist = sorted(glob("coco_dataset/*.csv"))
# csvlist = csvlist[1:]

# for f in csvlist:
#     df = pd.read_csv(f)
#     if df[df['labels'] == '_background_'].empty:
#         continue
#     else:
#         a = int(df[df['labels'] == '_background_'].index[0])
#         b = int(df[df['labels'] == 'TRIM_C_PLACKET_OVER'].index[0])
#         df.drop(df.index[[a, b]], inplace=True)

#     cnt_list = np.add(cnt_list, list(df['count']))
#     area_list = np.add(area_list, list(df['area']))

# print(*zip(label_list, cnt_list))

# overall_stats = pd.DataFrame(
#     {'labels': label_list,
#      'count': cnt_list,
#      'area': area_list
#     })

# overall_stats.to_csv('overall_stats_ann5.csv', index=False)

import cv2
import numpy as np
import pandas as pd
from glob import glob
from PIL import Image
import time
from tqdm import tqdm


path = "VERIFIED_DATASET/Batch4_8Aug/batch4_cardigans/SegmentationClass/*"
with open("VERIFIED_DATASET/Batch4_8Aug/batch4_asymmetric_draped_skirts/labelmap.txt", "r") as f:
    data = f.read()
    data_list = data.split("\n")
    f.close()

data_list = data_list[1:]
data_dict = {}

# df = pd.read_csv("panel_agg_Final.csv")
c = 0
for i in data_list:

    if len(i.split(':')) == 4:
        val = i.split(':')[0]
        raw_val = i.split(':')[1].split(',')
        rgb_val = [int(j) for j in raw_val]
        if val == "background":
            val = "_background_"

        # id = df.loc[df['panel_name'] == val]["new_id"].values[0]
        lis = []
        lis.append(rgb_val)
        lis.append(c)
        c += 1
        # lis.append(id)
        data_dict[val] = lis
# 
# print(data_dict)

dir_img = sorted(glob(path))
size = 512
count = 0
check = list(range(0, 455))
# check.append(65535)

kd = {}
for j in range(0, 455):
    kd[str(j)] = 0

for d in tqdm(dir_img):
    count += 1
    lab = cv2.imread(d)
    output = np.zeros_like(lab, dtype=np.uint16)+ 65535
    unique = np.unique(lab.reshape(-1, lab.shape[2]), axis=0)

    for obj_id in unique:
        obj_id =[int(j) for j in obj_id]
        for ik, (k, v) in enumerate(data_dict.items()):
            if v[0][::-1] == obj_id:
                kd[str(ik)] += 1
                output[lab==obj_id] = v[1]
                if obj_id == [201, 108, 47]:
                    print(k, v)

    # if count == 500:
    #     print(kd)

print(kd)
print(sum(kd.values()))
# new = pd.DataFrame([kd])
# new.to_csv("stats.csv", index=False)


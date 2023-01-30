import cv2
import numpy as np
import pandas as pd
from glob import glob
from PIL import Image
import time
from tqdm import tqdm
import json

# batch = "Batch4_8Aug"

# path = "merge_data/raw_annotation/*"
# with open("VERIFIED_DATASET/Batch4_8Aug/batch4_asymmetric_draped_skirts/labelmap.txt", "r") as f:
#     data = f.read()
#     data_list = data.split("\n")
#     f.close()

# data_list = data_list[1:]
# data_dict = {}

# print(data_list)


# code with pixel value

df = pd.read_csv("panel_agg_Final.csv")

# for i in data_list:

#     if len(i.split(':')) == 4:
#         val = i.split(':')[0]
#         raw_val = i.split(':')[1].split(',')
#         rgb_val = [int(j) for j in raw_val]
#         if val == "background":
#             val = "_background_"

#         id = df.loc[df['panel_name'] == val]["new_id"].values[0]
#         lis = []
#         lis.append(rgb_val)
#         lis.append(id)
#         data_dict[val] = lis

with open('labelmap.json') as json_file:
    data_dict = json.load(json_file)

path = 'replaced-batches/batch_1/Female/bodies/task_bodies-2022_08_20_07_37_25-coco 1.0/annotations/*'
dir_img = sorted(glob(path))
size = 512
count = 0
check = list(range(0, 160))
check.append(65535)


# print(dir_img)

# for d in tqdm(dir_img):
for d in dir_img:
    count += 1
    # lab = cv2.imread(d)
    lab = cv2.imread('replaced-batches/batch_1/Female/bodies/task_bodies-2022_08_20_07_37_25-coco 1.0/images/16348567_31810417.jpg')
    
    output = np.zeros_like(lab, dtype=np.uint16) + 65535
    unique = np.unique(lab.reshape(-1, lab.shape[2]), axis=0)
    # print(unique)

    for obj_id in unique:
        obj_id =[int(j) for j in obj_id]
        # print(obj_id)
        for k, v in data_dict.items():
            print(v, obj_id)
            # if v[0][::-1] == obj_id:
            if v == obj_id:
                output[lab==obj_id] = v[1]
                if obj_id == [59, 71, 21]:
                    print(k, v)


# for px_id in unique:
#     val = dic_val[str(px_id)]
#     coco_output[coco_output==px_id] = val




#     output = output[:, :, 0]

#     for i in list(np.unique(output)):
#         if i not in check:
#             print(d)

#     # output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
#     height, width = output.shape

#     if height > width:
#         new_w = size
#         new_h = int(size * (height/ width))
#         output = cv2.resize(output, (new_w, new_h), interpolation = cv2.INTER_NEAREST)

#     if height < width:
#         new_h = size
#         new_w = int(size * (width / height))
#         output = cv2.resize(output, (new_w, new_h), interpolation = cv2.INTER_NEAREST)

#     load_img = "merge_data/image/{}.jpg".format(d.split("/")[-1].split(".")[0])
#     img = cv2.imread(load_img)
#     height, width, _ = img.shape

#     if height > width:
#         new_w = size
#         new_h = int(size * (height/ width))
#         img = cv2.resize(img, (new_w, new_h), interpolation = cv2.INTER_CUBIC)

#     if height < width:
#         new_h = size
#         new_w = int(size * (width / height))
#         img = cv2.resize(img, (new_w, new_h), interpolation = cv2.INTER_CUBIC)
    
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     PILim = Image.fromarray(img)
#     save_pth = "data/image/{}.jpg".format(str(count).zfill(8))
#     PILim.save(save_pth)

#     PILmask = Image.fromarray(output)
#     save_pth = "data/mask/{}.tif".format(str(count).zfill(8))
    
#     PILmask.save(save_pth)




import numpy as np
import pandas as pd


filepaths = [f'coco_dataset/stats_ann{i}.csv' for i in range(1,16)]


res = np.zeros((455,2), dtype=np.int64)

# res2 = np.ones((455,2), dtype=np.int64)

# print(res + res2)
# print(res)
# print(filepaths)

for f in filepaths:
    pass
    # print(f)
    data1 = pd.read_csv(f)
    vals = data1[['label_counts', 'area_counts']].to_numpy(dtype=np.int64)
    res += vals

print(res)  

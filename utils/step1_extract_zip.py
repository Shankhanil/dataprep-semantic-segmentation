import zipfile
from glob import glob
import os

# zip_fil = 'VERIFIED_DATASET/Batch4_8Aug.zip'
# with zipfile.ZipFile(zip_fil, 'r') as zip_ref:
#     zip_ref.extractall('/home/bigthinx/Tarun/Indika_3d_Annotation/FINAL_DATA/')

# dir_zip = glob('/home/bigthinx/Tarun/Indika_3d_Annotation/FINAL_DATA/VERIFIED_DATASET/Batch11/*.zip')
# for d in dir_zip:
#     with zipfile.ZipFile(d, 'r') as zip_ref:
#         sav_pth = ''.join(d.split('.')[0])
#         os.makedirs(sav_pth, exist_ok=True)
#         zip_ref.extractall(sav_pth)

# zip_fil = "Batch 6"
zip_fil = "batch_7"


dir_zip = glob('replaced-batches/{}/*/*/*coco 1.0.zip'.format(zip_fil))
#  coco_dataset/Batch_15/Batch 15/Others/task_others 1.1-2022_09_08_11_52_30-segmentation mask 1.1.zip
for d in dir_zip:
    with zipfile.ZipFile(d, 'r') as zip_ref:
        sav_pth = ''.join(d.split('.')[0])
        os.makedirs(sav_pth, exist_ok=True)
        zip_ref.extractall(sav_pth)


# get images from segmentation mask
dir_zip = glob('replaced-batches/{}/*/*/*segmentation mask 1.1.zip'.format(zip_fil))
#  coco_dataset/Batch_15/Batch 15/Others/task_others 1.1-2022_09_08_11_52_30-segmentation mask 1.1.zip
for d in dir_zip:
    with zipfile.ZipFile(d, 'r') as zip_ref:
        sav_pth = ''.join(d.split('.')[0])
        os.makedirs(sav_pth, exist_ok=True)
        zip_ref.extractall(sav_pth)
from glob import glob 
import shutil
import numpy as np
import cv2
from PIL import Image


batch = "Batch 5"


dir_img = glob('replaced-batches/{}/*/*/*segmentation mask 1/JPEGImages/*.jpg'.format(batch))
# dir_seg = glob('{}/*/*/*segmentation mask 1/SegmentationClass/*.png'.format(batch))
print(len(dir_img))
# print(len(dir_seg))

for im in dir_img:
    # shutil.copy2(im, "/home/bigthinx/Tarun/Indika_3d_Annotation/FINAL_DATA/merge_data/image")
    shutil.copy2(im, "replaced-batches/Batch 5/*/*/*coco 1/images")

# for seg in dir_seg:
#     shutil.copy2(seg, "/home/bigthinx/Tarun/Indika_3d_Annotation/FINAL_DATA/merge_data/raw_annotation/")

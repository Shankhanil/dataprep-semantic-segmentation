from itertools import count
import json
import os
from pickletools import uint8
import cv2
import numpy as np
import pandas as pd
from glob import glob
from PIL import Image
import time
from tqdm import tqdm
import matplotlib
matplotlib.use('Agg')
import requests
from pycocotools.coco import COCO
import matplotlib.pyplot as plt
import shutil

# global counter
def main(root, counter):

    # load dictionary
    with open('labelmap.json') as json_file:
        data_dict = json.load(json_file)



    coco_annotation_file_path = os.path.join(root, "annotations/instances_default.json")
    # coco_annotation_file_path = annotation_file


    coco_annotation = COCO(annotation_file=coco_annotation_file_path)
    img_ids = coco_annotation.getImgIds()
    print(img_ids)

    for img_id in img_ids:

        img_info = coco_annotation.loadImgs([img_id])[0]
        img_file_name = img_info["file_name"]

        ann_ids = coco_annotation.getAnnIds(imgIds=[img_id], iscrowd=None)
        anns = coco_annotation.loadAnns(ann_ids)
        # print(f"Annotations for Image ID {img_id}:")
        # print(anns)
        pth = os.path.join(os.path.join(root, "images"), img_file_name)
        # pth = images_folder
        img = cv2.imread(pth)
        lit = []

        for i in range(len(anns)):
            lit.append(anns[i]['category_id'])
        
        if img is not None:
            anns_img = np.zeros(img.shape[:2], dtype = np.int16)

            for ann in anns:
                anns_img = np.maximum(anns_img,coco_annotation.annToMask(ann)*ann['category_id'])

            PILim = Image.fromarray(anns_img).convert('L')
            save_pth_img =os.path.join('final-dataset/image', f'{str(counter).zfill(6)}.jpg')
            save_pth_mask = os.path.join('final-dataset/mask', f'{str(counter).zfill(6)}.tif')
            
            # print(save_pth_img, save_pth_mask)

            cv2.imwrite(save_pth_img, img)
            PILim.save(save_pth_mask)
            counter += 1
    return counter



if __name__ == "__main__":

    # get list of src folders
    cocodict = {}
    root = "replaced-batches/batch_7"
    alldirs = os.walk(root)

    annotation_dir, images_dir = "", ""

    for d in alldirs:   
        for _d in d[1]:
            # for others
            if 'coco 1' in _d:
                cocodict[d[0]] = _d
    
    keys = cocodict.keys()

    finaldirs = []
    for k in keys:
        coco_dir = os.path.join(k, cocodict[k])
        finaldirs.append(coco_dir)




    # for batch 4,8,9, 10, 11
    # finaldirs = []
    # for d in alldirs:
    #     # print(d[1])
    #     if 'images' in d[1] and 'annotations' in d[1]:
    #         finaldirs.append(d[0])
    # print(finaldirs)
    

    # uncomment this section to run
    # last count = 10742
    # counter = 11942
    # print(finaldirs)
    # for d in finaldirs:
    #     counter = main(d, counter)
    # print(f'next ID = {counter}')
    # print(counter)




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



def main():

    coco_annotation_file_path = "replaced-batches/batch_1/Female/bodies/task_bodies-2022_08_20_07_37_25-coco 1.0/annotations/instances_default.json"

    coco_annotation = COCO(annotation_file=coco_annotation_file_path)

    # Category IDs.
    cat_ids = coco_annotation.getCatIds()
    print(f"Number of Unique Categories: {len(cat_ids)}")
    
    # print("Category IDs:")
    # print(cat_ids)  # The IDs are not necessarily consecutive.


    # # All categories.
    cats = coco_annotation.loadCats(cat_ids)
    cat_names = [cat["name"] for cat in cats]
    # print("Categories Names:")
    # print(cat_names)

    # # Category ID -> Category Name.
    query_id = cat_ids[2]
    query_annotation = coco_annotation.loadCats([query_id])[0]
    query_name = query_annotation["name"]
    print("Category ID -> Category Name:")
    print(
        f"Category ID: {query_id}, Category Name: {query_name}"
    )

    # # Category Name -> Category ID.
    query_name = cat_names[230]
    query_id = coco_annotation.getCatIds(catNms=[query_name])[0]
    print("Category Name -> ID:")
    print(f"Category Name: {query_name}, Category ID: {query_id}")

    # # Get the ID of all the images containing the object of the category.
    img_ids = coco_annotation.getImgIds(catIds=[query_id])
    # img_ids = coco_annotation.getImgIds()
    print(f"Number of Images Containing {query_name}: {len(img_ids)}")

    # data_ann = coco_annotation.getAnnIds(imgIds=1)
    # print(data_ann)
    # # Pick one image.
    print(img_ids)
    # exit(0)
    img_id = 2#img_ids[1]
    img_info = coco_annotation.loadImgs([img_id])[0]
    img_file_name = img_info["file_name"]
    # img_url = img_info["coco_url"]
    print(
        f"Image ID: {img_id}, File Name: {img_file_name}"
    )

    # Get all the annotations for the specified image.
    ann_ids = coco_annotation.getAnnIds(imgIds=[img_id], iscrowd=None)
    anns = coco_annotation.loadAnns(ann_ids)
    print(f"Annotations for Image ID {img_id}:")
    # print(anns)

    # # Use URL to load image.
    pth = os.path.join("replaced-batches/batch_1/Female/bodies/task_bodies-2022_08_20_07_37_25-coco 1.0/images", img_file_name)
    print(f'Loading image from {pth}')
    img = cv2.imread(pth)
    print(img.shape)
    print(len(anns))
    lit = []
    for i in range(len(anns)):
        lit.append(anns[i]['category_id'])

    print(len(lit))
    print(len(set(lit)))
    anns_img = np.zeros(img.shape[:2], dtype = np.int16)

    # anns_img = np.zeros_like(img.shape[:2], dtype=np.uint16) #+ 65535
    for ann in anns:
        anns_img = np.maximum(anns_img,coco_annotation.annToMask(ann)*ann['category_id'])

    # mask = coco_annotation.annToMask(anns[0])
    # for i in range(len(anns)):
    #     mask += coco_annotation.annToMask(anns[i])

    # plt.imshow(mask)
    # plt.savefig("test.png")
    # anns_img = anns_img.astype(np.int16) 

    print(anns_img.dtype)
    print(type(anns_img))
    print(anns_img.shape)
    print(np.unique(anns_img))
    print(len(np.unique(anns_img)))

    # anns_img = anns_img.astype(np.uint16) 
    cv2.imwrite("md.png", anns_img)
    # anns_img = anns_img.astype(np.uint16) 
    # anns_img = np.asarray(anns_img), dtype=np.uint16)
    # img = cv2.cvtColor(anns_img, cv2.COLOR_BGR2GRAY)
    PILim = Image.fromarray(anns_img).convert('L')
    save_pth = os.path.join('final-dataset/mask', f'{img_file_name}.tif')
    PILim.save(save_pth)

    # t = coco_annotation.annToMask(ann)*ann['category_id']
    # print(type(t))
    # print(t.dtype)
    # cv2.imwrite("md.png", t)
    # im = cv2.imread("md.png")
    # print(im.shape)
    # print(np.unique(im))

if __name__ == "__main__":

    main()
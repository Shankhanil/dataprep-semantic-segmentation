import os
import logging
from pycocotools.coco import COCO
import cv2
import numpy as np
import config
from PIL import Image

class CustomFormatter(logging.Formatter):

    # green = "\x1b[32;20m"
    green = "\u001b[32;1m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        # logging.DEBUG: green + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def generate_mask(root, logger, counter):
    coco_annotation_file_path = os.path.join(root, "annotations/instances_default.json")
    # coco_annotation_file_path = annotation_file

    data_dict = config.labelmap

    coco_annotation = COCO(annotation_file=coco_annotation_file_path)
    img_ids = coco_annotation.getImgIds()
    logger.debug(f'total img ids = {img_ids}')

    for img_id in img_ids:
        logger.critical(f'img id = {img_id}')
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
            # anns_img = np.zeros(img.shape[:2], dtype = np.int16)
            unique = np.unique(anns_img)

            for ann in anns:
                anns_img = np.maximum(anns_img,coco_annotation.annToMask(ann)*ann['category_id'])
                logger.debug( np.unique(anns_img) )
                # break
            unique = np.unique(anns_img)

            # logger.debug(f'\n\nUnique IDs {unique}')
            
            # create updated panel label
            for px_id in unique:
                val = data_dict[str(px_id)]
                anns_img[anns_img==px_id] = val
            
            unique = np.unique(anns_img)
            logger.debug(unique)
           
            # logger.debug(f'image size = {anns_img.shape}')

            # image resize
            height, width, _ = img.shape

            if height > width:
                new_w = config.SIZE
                new_h = int(config.SIZE * (height/ width))
                img = cv2.resize(img, (new_w, new_h), interpolation = cv2.INTER_NEAREST)

            if height < width:
                new_h = config.SIZE
                new_w = int(config.SIZE * (width / height))
                img = cv2.resize(img, (new_w, new_h), interpolation = cv2.INTER_NEAREST)


            # mask resize
            height, width = anns_img.shape

            if height > width:
                new_w = config.SIZE
                new_h = int(config.SIZE * (height/ width))
                anns_img = cv2.resize(anns_img, (new_w, new_h), interpolation = cv2.INTER_NEAREST)

            if height < width:
                new_h = config.SIZE
                new_w = int(config.SIZE * (width / height))
                anns_img = cv2.resize(anns_img, (new_w, new_h), interpolation = cv2.INTER_NEAREST)

            PILim = Image.fromarray(anns_img).convert('L')
            save_pth_img =os.path.join( config.DATASET_PATH, 'image', f'{str(counter).zfill(6)}.jpg')
            save_pth_mask = os.path.join(config.DATASET_PATH, 'mask', f'{str(counter).zfill(6)}.tif')
            
            logger.info(f'image size = {anns_img.shape}')

            cv2.imwrite(save_pth_img, img)
            PILim.save(save_pth_mask)
            assert os.path.isfile( os.path.join( config.DATASET_PATH, 'image', f'{str(counter).zfill(6)}.jpg') ) and os.path.isfile(os.path.join(config.DATASET_PATH, 'mask', f'{str(counter).zfill(6)}.tif') )
            # assert 65535 in np.unique(anns_img)
            counter += 1
        # break
        # break
    return counter


def count_files(dir_path):
    count = 0
    for path in os.listdir(dir_path):
    # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count


# root = 
# generate_mask(root, logger, counter)
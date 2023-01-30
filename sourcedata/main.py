# from tabnanny import check
# from typing import final

import argparse
import random
from time import sleep
import zipfile

import numpy as np
import config
import os
from tqdm import tqdm
from glob import glob
from utils import CustomFormatter, count_files, generate_mask
import shutil
import logging
from datetime import datetime
from dateutil import tz
from pyfiglet import Figlet
from sklearn.model_selection import train_test_split

def unzip(batch):
    streamlogger.info('unzipping files')
    batch_structure = config.batch_structure_metadata[str(batch)]
    cocozip_string = batch_structure.format( config.batch_name_metadata[str(batch)] ) + config.suffix_map['cocozip']
    segzip_string = batch_structure.format( config.batch_name_metadata[str(batch)] ) + config.suffix_map['segzip']

    # coco zip
    dir_zip = glob(cocozip_string)
    
    for d in dir_zip:
        with zipfile.ZipFile(d, 'r') as zip_ref:
            sav_pth = ''.join(d.split('.')[0])
            os.makedirs(sav_pth, exist_ok=True)
            zip_ref.extractall(sav_pth)

    # seg zip
    dir_zip = glob(segzip_string)
    for d in dir_zip:
        with zipfile.ZipFile(d, 'r') as zip_ref:
            sav_pth = ''.join(d.split('.')[0])
            os.makedirs(sav_pth, exist_ok=True)
            zip_ref.extractall(sav_pth)
    pass

def create_img_folder(missing_img_folders):
    if missing_img_folders != {}:
        for seg_folder in missing_img_folders.keys():
            streamlogger.info(f'Attempting to copy images from {seg_folder} to {missing_img_folders[seg_folder]}')
            shutil.copytree(seg_folder, missing_img_folders[seg_folder])
            streamlogger.info(f'\nSuccessfully transferred {count_files(seg_folder)} files to {missing_img_folders[seg_folder]}')
            assert count_files(seg_folder) == count_files(missing_img_folders[seg_folder])

# step1 check if all batches have annotation and image folder
def check_folder_structure(batch):
    streamlogger.info('Checking folder structure before generating dataset')

    path_to_batch = os.path.join(config.RAW_DATA_ROOT, config.batch_name_metadata[str(batch)])
    batch_structure = config.batch_structure_metadata[str(batch)]


    # search_string_images = os.path.join(config.ROOT, batch_structure.format( config.batch_name_metadata[str(batch)] ) + config.suffix_map['images'])
    # search_string_seg = os.path.join(config.ROOT, batch_structure.format( config.batch_name_metadata[str(batch)] ) + config.suffix_map['seg_jpeg'])

    search_string_images = batch_structure.format( config.batch_name_metadata[str(batch)] ) + config.suffix_map['images']
    search_string_seg = batch_structure.format( config.batch_name_metadata[str(batch)] ) + config.suffix_map['seg_jpeg']

    img_folder = glob(search_string_images)
    seg_folder = glob(search_string_seg)
    
    # logger.critical(search_string_images)
    # logger.critical(len(img_folder))

    # logger.info(search_string_seg)
    # logger.info(len(seg_folder))
    # return None
    missing_img_folders = {}
    
    try:
        assert len(img_folder) == len(seg_folder)
                
    except Exception as e:
        streamlogger.critical('some image folders need to be generated')
        streamlogger.critical(f'total img folders = {len(img_folder)}. total seg folder = {len(seg_folder)}')

        for _seg_folder in tqdm(seg_folder):
            _img_folder = '-'.join(_seg_folder.split('-')[:-1])+ "-coco 1.0/images"
            annotation_folder = '-'.join(_seg_folder.split('-')[:-1])+ "-coco 1.0/annotations"
            
            # annotation folder must exist
            try:
                # logger.debug( folder )
                assert os.path.exists(annotation_folder)
            except:
                filelogger.critical( f'Annotation folder {annotation_folder} DNE' )
                # raise AssertionError
                return False
            
            # check if image path exists, if not, copy JPEG imgs to image folder
            try:
                assert os.path.exists(_img_folder)
                assert count_files(_seg_folder) == count_files(_img_folder)
                streamlogger.info(f'{_img_folder} exists, with {count_files(_img_folder)} files')
            except:
                missing_img_folders[_seg_folder] = _img_folder
        
        streamlogger.warning( f'Total no. of missing img folders = {len(missing_img_folders.keys())}' )
        create_img_folder(missing_img_folders)
        # assert len(img_folder) == len(seg_folder)
    finally:
        streamlogger.info(f'Folder check completed for Batch  {batch}')
    
    return True


# step3 generate raw img and mask tif
def generate_dataset(batch):

    ignore = []

    streamlogger.info('Generating dataset......')
    folder_structure = config.batch_structure_metadata[str(batch)]
    batch_name = config.batch_name_metadata[str(batch)]

    # if folder_structure == "replaced-batches/{}/*/*/":
    root = os.path.join( folder_structure.format(batch_name), config.suffix_map['coco'] )


    img_folder = glob( root )
    assert img_folder != []
    allfolders = True

    for folder in img_folder:
        if not os.path.isfile(folder):
            allfolders = False
            try:
                assert os.path.exists( os.path.join( folder, 'images' ) )
            except:
                streamlogger.critical( f'This is step 2. {folder} still does not have images folder. Skipping...' )
                ignore.append(folder)
                # if folder in config.exceptions.keys():
                #     exp_img_folder = config.exceptions[folder]
                #     logger.critical(f'Images are in {exp_img_folder}. Total images are {count_files(exp_img_folder)}')
                    
                #     os.makedirs(os.path.join( folder, 'images' ))
                # else:
                #     return False
            finally:
                if folder not in ignore:
                    try:
                        assert os.path.exists( os.path.join( folder, 'annotations' ) )
                    except:
                        streamlogger.critical(f'Annotation folder DNE for {folder}')
                        raise AssertionError
                    finally:
                        _f = os.path.join( folder, 'images' )
                        streamlogger.debug(f'Looking at {_f} with {count_files(_f)} files')

                        # generate mask and tiff
                        config.COUNTER = generate_mask(root=folder, logger=streamlogger, counter=config.COUNTER)

    # elif folder_structure == "replaced-batches/{}/":
    #     pass
    # else:
    #     raise AssertionError
    try:
        assert not allfolders
        streamlogger.debug('Dataset generated successfully')
    except:
        streamlogger.critical(f'No folders exist in batch {batch}')


def split_dataset( split_ratio = 0.2 ):

    if not os.path.exists(config.SPLIT_DATASET_PATH):

        streamlogger.info('Creating Split dataset path')
        os.makedirs( config.SPLIT_DATASET_PATH )
        pass
  
    if not os.path.exists(os.path.join(config.SPLIT_DATASET_PATH, 'image/train')):
        os.makedirs( os.path.join(config.SPLIT_DATASET_PATH, 'image/train') )
        pass
    
    if not os.path.exists(os.path.join(config.SPLIT_DATASET_PATH, 'image/test')):
        os.makedirs( os.path.join(config.SPLIT_DATASET_PATH, 'image/test') )
        pass
    
    if not os.path.exists(os.path.join(config.SPLIT_DATASET_PATH, 'mask/train')):
        os.makedirs( os.path.join(config.SPLIT_DATASET_PATH, 'mask/train') )
        pass
    
    if not os.path.exists(os.path.join(config.SPLIT_DATASET_PATH, 'mask/test')):
        os.makedirs( os.path.join(config.SPLIT_DATASET_PATH, 'mask/test') )
        pass
    
    
    img_path = glob(os.path.join( config.DATASET_PATH, 'image/*' ))

    img_path = [i.split('.')[0] for i in img_path]
    streamlogger.info(f'{len(img_path)}')
    random.shuffle(img_path)
    data = np.array(img_path)

    x_train, x_test = train_test_split(data,test_size=split_ratio)

    streamlogger.info(f' train size =  {len(x_train)}, test size = {len(x_test)}')

    for i, file in enumerate(x_train):
        im = file + '.jpg'
        msk = file.replace('image', 'mask') + '.tif'

        # im_sav = "dataset/images/train/"  + 'pannel_train_' + str(i).zfill(8) + '.jpg'
        # msk_sav = "dataset/mask/train/" + 'pannel_train_' + str(i).zfill(8) + '.tif'

        im_sav = os.path.join(config.SPLIT_DATASET_PATH, 'image/train',  'pannel_train_' + str(i).zfill(8) + '.jpg')
        msk_sav =os.path.join(config.SPLIT_DATASET_PATH, 'mask/train' ,  'pannel_train_' + str(i).zfill(8) + '.tif')


        shutil.copy(im, im_sav)
        shutil.copy(msk, msk_sav)

    for i, file in enumerate(x_test):
        im = file + '.jpg'
        msk = file.replace('image', 'mask') + '.tif'
        
        im_sav = os.path.join(config.SPLIT_DATASET_PATH, 'image/test',  'pannel_test_' + str(i).zfill(8) + '.jpg')
        msk_sav =os.path.join(config.SPLIT_DATASET_PATH, 'mask/test' ,  'pannel_test_' + str(i).zfill(8) + '.tif')
        shutil.copy(im, im_sav)
        shutil.copy(msk, msk_sav)
    
    assert count_files(os.path.join(config.SPLIT_DATASET_PATH, 'image/train'))  == len(x_train) 
    assert count_files(os.path.join(config.SPLIT_DATASET_PATH, 'mask/train'))  == len(x_train)
    assert count_files(os.path.join(config.SPLIT_DATASET_PATH, 'image/test'))  == len(x_test) 
    assert count_files(os.path.join(config.SPLIT_DATASET_PATH, 'mask/test'))  == len(x_test)
    streamlogger.info('Train test split successful')

def parser():
    parser = argparse.ArgumentParser(description='Data preparation pipeline for cloth segmentation (3D CLOTH GENERATION PIPELINE).')
    parser.add_argument('--task', type=str,required=True, choices=['generate', 'split', 'debug'], help='Give the task')
    # parser.add_argument('--batch', type=int, default=0, help='Any specific batch to process?')
    parser.add_argument('--batch', type=int, nargs='+', default=0, help='Any specific batch to process? in list format')
    args = parser.parse_args()
    return args



if __name__ == "__main__": 

    streamlogger = logging.getLogger("Data prep pipeline")
    streamlogger.setLevel(logging.DEBUG)

    filelogger = logging.getLogger("Data prep pipeline")
    filelogger.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    logfile = os.path.join( config.LOG_FILE_PATH, datetime.now(tz=tz.gettz()).strftime("%Y-%m-%d-%H-%M") )
    ch = logging.StreamHandler()
    fh = logging.FileHandler(logfile)
    
    
    ch.setLevel(logging.DEBUG)
    fh.setLevel(logging.DEBUG)

    ch.setFormatter(CustomFormatter())
    # fh.setFormatter(CustomFormatter())

    streamlogger.addHandler(ch)
    filelogger.addHandler(fh)

    heading = Figlet(font = 'slant')

    opts = parser()

    # print(opts.task)
    if opts.task == 'debug':
        generate_mask( root='//home/shankhanil/work/3dclothgen/panel-stats/DATA_PREP/replaced-batches/batch_4/task_blazers-2022_08_03_15_09_32-coco 1', logger=streamlogger, counter=1 )
    if opts.task == 'generate':
        if opts.batch != 0:
            batchlist = opts.batch
        else:
            batchlist = range(1, config.MAX_BATCH+1)
            # init_batch = 1
            # final_batch = config.MAX_BATCH+1

        streamlogger.info(f'Handling these batches = {batchlist}')
        # exit(0)
        # for batch in range(init_batch, final_batch):
        for batch in batchlist:

            print(heading.renderText(f'Batch {batch}'))

            unzip(batch=batch)
            if check_folder_structure( batch ):
                if not os.path.exists(config.DATASET_PATH):
                    os.makedirs(config.DATASET_PATH)

                if not os.path.exists( os.path.join(config.DATASET_PATH, 'image') ):
                    os.makedirs(os.path.join(config.DATASET_PATH, 'image'))

                if not os.path.exists( os.path.join(config.DATASET_PATH, 'mask') ):
                    os.makedirs(os.path.join(config.DATASET_PATH, 'mask'))
                
                generate_dataset( batch )
                streamlogger.critical(f'counter = {config.COUNTER}')
                sleep(1)
            else:
                streamlogger.critical(f'Some errors with batch {batch}')

    if opts.task == 'split':
        split_dataset()
        
    # batch = 1
    # print(heading.renderText(f'Batch {batch}'))

    # for batch in range(1, config.MAX_BATCH+1):

    #     print(heading.renderText(f'Batch {batch}'))

    #     unzip(batch=batch)
    #     if check_folder_structure( batch ):
    #         if not os.path.exists(config.DATASET_PATH):
    #             os.makedirs(config.DATASET_PATH)

    #         if not os.path.exists( os.path.join(config.DATASET_PATH, 'image') ):
    #             os.makedirs(os.path.join(config.DATASET_PATH, 'image'))

    #         if not os.path.exists( os.path.join(config.DATASET_PATH, 'mask') ):
    #             os.makedirs(os.path.join(config.DATASET_PATH, 'mask'))
            
    #         generate_dataset( batch )
    #         streamlogger.critical(f'counter = {config.COUNTER}')
    #         sleep(1)
    #     else:
    #         streamlogger.critical(f'Some errors with batch {batch}')
    # pass
    # split_dataset()

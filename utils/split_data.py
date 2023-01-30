from glob import glob 
import random
from sklearn.model_selection import train_test_split
import numpy as np
import shutil

dir_pth = glob("final-dataset-test_2/image/*")

dir_pth = [i.split('.')[0] for i in dir_pth]
print(len(dir_pth))
random.shuffle(dir_pth)
data = np.array(dir_pth)

x_train ,x_test = train_test_split(data,test_size=0.2)


print(len(x_train), len(x_test))

for i, file in enumerate(x_train):

    im = file + '.jpg'
    msk = file.replace('image', 'mask') + '.tif'

    im_sav = "dataset/images/train/"  + 'pannel_train_' + str(i).zfill(8) + '.jpg'
    msk_sav = "dataset/mask/train/" + 'pannel_train_' + str(i).zfill(8) + '.tif'
    shutil.copy(im, im_sav)
    shutil.copy(msk, msk_sav)

for i, file in enumerate(x_test):
    im = file + '.jpg'
    msk = file.replace('image', 'mask') + '.tif'
    im_sav = "dataset/images/test/"  +  'pannel_test_' +  str(i).zfill(8) + '.jpg'
    msk_sav = "dataset/mask/test/" + 'pannel_test_' + str(i).zfill(8) + '.tif'
    shutil.copy(im, im_sav)
    shutil.copy(msk, msk_sav)
# exit()
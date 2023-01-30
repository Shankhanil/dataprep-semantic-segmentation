import os

from numpy import save
import cv2
from PIL import Image


def resize(pth, imgtype):
    img = cv2.imread(pth)

    size = 512
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width, _ = img.shape

    if height > width:
        new_w = size
        new_h = int(size * (height/ width))
        img = cv2.resize(img, (new_w, new_h), interpolation = cv2.INTER_NEAREST)

    if height < width:
        new_h = size
        new_w = int(size * (width / height))
        img = cv2.resize(img, (new_w, new_h), interpolation = cv2.INTER_NEAREST)
    
    pthsplit = pth.split('/')
    new_root = f'{pthsplit[0]}_2'
    save_path = os.path.join( new_root , '/'.join(pthsplit[1:]) )
    
    print(save_path)

    if imgtype == 'tif':
        PILim = Image.fromarray(img).convert('L')
        PILim.save(save_path)
        print(f'successfully saved at {save_path}')
    elif imgtype == 'jpg':
        cv2.imwrite(save_path, img)
        print(f'successfully saved at {save_path}')



    return img.shape


if __name__ == '__main__':

    # pth = 'final-dataset-test/mask/000001.tif'

    # d = 
    root = 'final-dataset-test'
    paths = [p for p in os.walk(root)]
    # print(paths[1][2])
    
    # images
    _pth, files = paths[1][0], paths[1][2]
    for f in files:
        pth = os.path.join(_pth, f)
        print(f'resizing {pth}')
        resize(pth=pth, imgtype='jpg')
    
    # mask
    # images
    _pth, files = paths[2][0], paths[2][2]
    for f in files:
        pth = os.path.join(_pth, f)
        print(f'resizing {pth}')
        resize(pth=pth, imgtype='tif')

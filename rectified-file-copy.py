from email.mime import image
from itertools import count
import os
import shutil

def count_files(dir_path):
    count = 0
    for path in os.listdir(dir_path):
    # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count


if __name__ == "__main__":
    finaldirs = []
    root = "replaced-batches/batch_7"
    # batch = "Batch 5"

    # currdir = os.path.join(root, batch)
    # alldirs = os.walk(currdir)
    alldirs = os.walk(root)

    currdir = ""

    cocodict, segdict = {}, {}

    annotation_dir, images_dir = "", ""
    for d in alldirs:
        for _d in d[1]:
            if 'coco 1' in _d:
                cocodict[d[0]] = _d
            if 'segmentation' in _d:
                segdict[d[0]] = _d

    keys = cocodict.keys()
    print(len(keys)) 
    print(len(segdict.keys()))
    
    assert len(keys) == len(segdict.keys())

    assert cocodict.keys() == segdict.keys()
    
    for k in keys:
        coco_dir = os.path.join(os.path.join(k, cocodict[k]), 'images')
        seg_dir = os.path.join(os.path.join(k, segdict[k]), 'JPEGImages')
        
        if not os.path.exists( coco_dir ):
            os.makedirs(coco_dir)
        
        assert os.path.exists(coco_dir) and os.path.exists(seg_dir)

        try:
            if os.path.exists( coco_dir ):
                shutil.rmtree(coco_dir)
            shutil.copytree(seg_dir, coco_dir)
            print(f'\nSuccessfully transferred {count_files(seg_dir)} files to {coco_dir}')
            assert count_files(seg_dir) == count_files(coco_dir)


        except Exception as e:
            print(f'\n\nsome error occured {e}')
            print(f'source {seg_dir}\ndest {coco_dir}')


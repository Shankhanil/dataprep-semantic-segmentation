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


finaldirs = []
root = "replaced-batches/Batch 5"
# batch = "Batch 5"

# currdir = os.path.join(root, batch)
# alldirs = os.walk(currdir)
alldirs = os.walk(root)

currdir = ""

annotation_dir, images_dir = "", ""
for d in alldirs:
    if 'annotations' in d[1]:
        # dont add annotations to path already, because we need to create images folder
        currdir1 = '/'.join(annotation_dir.split('/')[:-1])
        annotation_dir = d[0]
    
    elif 'JPEGImages' in d[1]:
        currdir2 = '/'.join(d[0].split('/')[:-1])
        images_dir = os.path.join(d[0], 'JPEGImages')
        if images_dir not in finaldirs:
            finaldirs.append(images_dir)
            pass
    
    if annotation_dir!= "" and images_dir!="":
        # print(currdir2)
        try:
            assert currdir1 == currdir2
        except:
            print(currdir1, currdir2)
    # if annotation_dir!= "" and images_dir!="":
    #     assert root in annotation_dir and root in images_dir
    #     dst = os.path.join(annotation_dir, 'images')


    #     # remove tree if not exists
    #     if os.path.exists( dst ):
    #         shutil.rmtree(dst)
    #     shutil.copytree(images_dir, dst)
        
    #     print(f'copied {count_files(images_dir)} files from {images_dir} ')
    #     assert count_files(os.path.join(annotation_dir, 'images')) == count_files(images_dir)
    #     # print(annotation_dir, images_dir, count_files(images_dir))
    
import os


root = 'final-dataset/image'
counter = 0
max_counter = 3040
directory = os.fsencode(root)
    
for file in os.listdir(directory):
    counter +=1
    filename = os.fsdecode(file)
    os.rename(os.path.join(root, filename), os.path.join(root, str(counter).zfill(6)+".jpg"))


print(counter)

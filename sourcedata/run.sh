rm -f -r /home/shankhanil/work/3dclothgen/panel-stats/DATA_PREP/dataset_dump/*
python data-prep-pipeline/main.py --task generate_dataset --batch 4 8 9 10 11
# python data-prep-pipeline/main.py --task generate_dataset
# python data-prep-pipeline/main.py --task generate_dataset --batch 8
# python data-prep-pipeline/main.py --task generate_dataset --batch 9
# python data-prep-pipeline/main.py --task generate_dataset --batch 10
# python data-prep-pipeline/main.py --task generate_dataset --batch 11

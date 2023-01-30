import json

ROOT = '/media/shankhanil/2.T.B HDD/DATA_PREP/sourcedata'
RAW_DATA_ROOT = '/media/shankhanil/2.T.B HDD/DATA_PREP/sourcedata/replaced-batches'
METADATA_PATH = '/media/shankhanil/2.T.B HDD/DATA_PREP/sourcedata/metadata.json'
BATCH_METADATA_PATH = '/media/shankhanil/2.T.B HDD/DATA_PREP/sourcedata/batch-metadata.json'
# LABELMAP_PATH = '/home/shankhanil/work/3dclothgen/panel-stats/DATA_PREP/data-prep-pipeline/labelmap.json'
LABELMAP_PATH = '/media/shankhanil/2.T.B HDD/DATA_PREP/sourcedata/new_labelmap.json'


DATASET_PATH = '/media/shankhanil/2.T.B HDD/DATA_PREP/sourcedata/data'
SPLIT_DATASET_PATH = '/media/shankhanil/2.T.B HDD/DATA_PREP/sourcedata/data_split'

MAX_BATCH = 11


# image size for mask and raw-image
SIZE = 512
COUNTER = 1

LOG_FILE_PATH = '/media/shankhanil/2.T.B HDD/DATA_PREP/sourcedata/data-prep-pipeline/logs'

# load metadata dictionary
with open(METADATA_PATH) as json_file:
    metadata = json.load(json_file)

# load labelmap dictionary
with open(LABELMAP_PATH) as json_file:
    labelmap = json.load(json_file)


# load raw batch names metadata
with open(BATCH_METADATA_PATH) as json_file:
    dict = json.load(json_file)
    batch_name_metadata = dict[ metadata['batch_names'] ]
    batch_structure_metadata = dict[ metadata['batch_folder_structure'] ]
    suffix_map = dict[ metadata['suffix'] ]
    exceptions = dict[ metadata['exceptions'] ]


# # load batch folder-structures metadata
# with open(BATCH_METADATA_PATH) as json_file:
#     dict = json.load(json_file)

# with open(BATCH_METADATA_PATH) as json_file:
#     dict = json.load(json_file)


    

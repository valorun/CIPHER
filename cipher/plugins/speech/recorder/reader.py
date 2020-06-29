import json
from os.path import join
from .constants import DATASET_PATH

def get_labels():
    """
    Get unique labels ordered by their index in the file listing all classes.
    """
    with open(join(DATASET_PATH, 'classes.json'), 'r') as filename:
        return list(dict.fromkeys(json.load(filename).values()))
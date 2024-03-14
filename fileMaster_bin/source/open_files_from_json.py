from .bed_class import BedFile
from .table_class import TableFile
from .file_class import Source
from documantation_createor import create_documantation
import json
import os

NO_JSON_MSG = 'The file {path} does not have documantation json.'

JSON_EXTENSION = '.json'

CLASS_CONTRUCTOR_DICT = {
    'table': TableFile,
    'bed': BedFile,
    'source': Source}




def json_to_object(path, class_type):
    with open(path, 'r') as file:
        data = json.load(file)
    return CLASS_CONTRUCTOR_DICT[class_type](data)



def open_file(path):
    """
    open a file from a given path
    """
    if not path.endswith(JSON_EXTENSION):
        json_path = path.split('.')[0] + JSON_EXTENSION
        if os.path.exists(json_path):
            path = json_path
        else:
            print(NO_JSON_MSG.format(path=path))
            make_json = input("Create json file?(y/n)") == 'y'
            if make_json:
                return create_documantation(path)
    with open(path, 'r') as file:
        data = json.load(file)
    file_key = data['file_data']['file_type']
   
    return CLASS_CONTRUCTOR_DICT[file_key].from_json(path)

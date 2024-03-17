from abc import ABC
from typing import List, Optional
from pydantic import BaseModel, field_validator, Field
from typing_extensions import Annotated
from datetime import datetime
import os
import json



class File(ABC):
        _class_data_key = 'file_data'
        

        def __init__(self, path: str =None, 
                    description: str = None, 
                    sources_list: List[dict] = None ,
                    date: str  = None,
                    file_type: str = None, 
                    additional_data:dict =  {},
                    name = '',
                    **kwargs):
            """
            Initializes a File instance.

            Args:
                name (str): The name of the file.
                path (str): The path of the file.
                description (str): The description of the file.
                source (dict): Information about the file source (e.g., database, publication, etc.).
                date (str): The date and time when the file was created. Defaults in subclasse set to None.
            """
            # print("=======File======")
            # for k,v in kwargs.items():
            #     print(k,v)
            # print('len', len(kwargs))

            if 'file_data' in kwargs:
                self.file_data = self.FileData(**kwargs['file_data'])
            else:
                self.file_data = self.FileData(path = path,
                                    description = description,
                                    sources_list = sources_list,
                                    date = date,
                                    file_type = file_type,
                                    name = name,
                                    additional_data = additional_data)



        def get_sources(self):
            return self.file_data.sources_list

        def get_path(self):
            return self.file_data.path

        def get_data(self):
            data = {}
            for key, value in vars(self).items():
                if 'data' in key:
                    data[key] = value.dict()
            return data
        

        def __str__(self):
            return str(self.get_data())
        

        def to_json(self, path: str):
            """
            Saves the file to a JSON file.
            Args: path (str): The path of the JSON file.
            """
            with open(path, 'w') as file:
                data = self.get_data()
                json.dump(data, file, indent='\t')
                print(f"File saved to {path}.")

        def save_json(self):
            """
            Saves the file obect into a json
            """
            path = self.file_data.path.split('.')[0] + '.json'
            self.to_json(path)
            return path

        def as_source(self):
            return Source(file_type =  self.file_data.file_type,
                          path= self.file_data.path,
                          name = self.file_data.name,
                          description = self.file_data.description)
        

        def get_additional_data_dict(self) -> dict:
            if self.file_data.additional_data is None:
                self.file_data.additional_data = {}
            return self.file_data.additional_data


        def __update_additional_data(self, key, data_id, data: dict):
                key_dict =  self.get_additional_data_dict().pop(key)
                if key_dict is None:
                    print(f"Key does not exist in file  additional data.\n \
                           Creating new record- {key}.")
                    cur_key_dict = {}
                else:
                    cur_key_dict = key_dict
                cur_key_dict[data_id] = data
                self.get_additional_data_dict().update({key: cur_key_dict})



        def add_additional_data(self,key, data_id, data: dict, force=False):
            if  key  in self.get_additional_data_dict().keys():
                key_dict = self.file_data.additional_data[key]
                if data_id in key_dict and not force:
                    to_replace = input(f"Key {data_id} already exists in {key} dile data. \
                                    Do you want to replace it? (y/n)")
                    if not to_replace.lower() == 'y':
                        return
            self.__update_additional_data(key, data_id, data)
            self.save_json()
            

        def get_additional_data(self, key):
            if key not in self.file_data.additional_data:
               print(f"Key {key} does not exist in {self.file_data.name} file data.")
               return None
            return self.file_data.additional_data[key]


        ##### class methods ####


        # @classmethod
 
        @classmethod
        def from_json(cls,path: str):
            """
            Creates a instance from a JSON file.
            Args: path (str): The path of the JSON file.
            Returns: File: The File instance.
            """
            data = cls.__open_json(path)
            all_args =  {}
            for key, value in data.items():
                all_args.update(value)
            # file_path = data['file_data']['path']
            # assert os.path.exists(file_path), f"File {file_path} does not exist."
            return cls(**all_args)
        

        @classmethod
        def __open_json(cls, path: str):
            """
            Reads JSON data from a file and returns the parsed data.
            Args:
                path (str): The path of the JSON file.
            Returns:
                dict: Parsed JSON data.
            """
            with open(path, 'r') as file:
                data = json.load(file)
            return data
    
        @classmethod
        def get_class_data(cls, data_dict:dict):
            return data_dict[cls.class_data_key]
    
        class FileData(BaseModel):
            """
            The base class for all files.
            Abstract class, cannot be instantiated.

            Attributes:
                name (str): The name of the file.
                path (str): The path of the file.
                description (str): The description of the file.
                source (dict): Information about the file source (e.g., database, publication, etc.).
                date (str): The date and time when the log file was created.
            """

            path: str
            file_type: str
            description: str
            sources_list: Optional[List[dict]] = []
            date: Optional[str] = None
            name: Annotated[str, Field(validate_default=True)] = ""
            additional_data: dict = {}
            
            @field_validator('name')
            @classmethod
            def set_name(cls, value, values) -> str:
                if len(value):
                    return value
                print(values)
                if os.path.exists(values.data['path']):
                    return os.path.basename(values.data['path'])
                return values.data['path']
        

            @field_validator('date')
            def set_date(cls, value):
                """
                Validator to set the default creation date if not provided.

                Args:
                    value (str): The date value provided.

                Returns:
                    str: The date value or the current date if not provided.
                """
                if value != None and is_valid_date_format(value):
                    return value
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"Date not in correct format: {value}. Setting to current date: {date}.")
                return date

            @field_validator('path')
            @classmethod
            def name_must_contain_space(cls, path: str) -> str:
                """
                Field validator to ensure the file exists.
                Args: path (str): The file path.
                Returns: str: The validated file path.
                """
                if not os.path.exists(path):
                    print(f"WARNING: File {path} does not exist.\n ignore if this is not a file")
                return path
    


def is_valid_date_format(date_string):
    """
    Checks if the given date string is in the format "%Y-%m-%d" or "%Y-%m-%d %H:%M:%S".

    Args:
        date_string (str): The date string to be checked.

    Returns:
        bool: True if the date string is in the correct format, False otherwise.
    """
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        try:
            datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False
        



class Source(File):


        def __init__(self, file_type: str, path: str, description: str, date: str = None, sources_list=[], name = ''):
            super().__init__(path = path, description = description, sources_list =sources_list, file_type=file_type, date = date, name = name)


